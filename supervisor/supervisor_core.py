import threading
from typing import List, Dict, Any, Optional
from supervisor.task_manager import TaskManager
from supervisor.scheduler import Scheduler
from supervisor.interrupt_handler import InterruptHandler
from supervisor.logs.supervisor_logger import SupervisorLogger

class SupervisorCore:
    """
    Main orchestrator for OMNIMIND Supervisor Core.
    Manages agents, tasks, plugins, pipelines, interruptions, and system health in real time.
    Thread-safe and modular for integration with FastAPI and pipelines.
    """
    def __init__(self,
                 agents: Optional[List[Any]] = None,
                 plugins: Optional[List[Any]] = None):
        self.agents = agents or []
        self.plugins = plugins or []
        self.task_manager = TaskManager()
        self.scheduler = Scheduler()
        self.interrupt_handler = InterruptHandler()
        self.logger = SupervisorLogger()
        self._lock = threading.Lock()
        self.system_state = {
            "active_agents": len(self.agents),
            "active_tasks": 0,
            "health": "green",
            "last_error": None
        }

    def register_agent(self, agent: Any) -> None:
        """Register a new agent for supervision."""
        with self._lock:
            self.agents.append(agent)
            self.system_state["active_agents"] = len(self.agents)
            self.logger.log("register_agent", {"agent": str(agent)})

    def submit_task(self, task: Dict[str, Any]) -> str:
        """Submit a new task to the task manager."""
        task_id = self.task_manager.add_task(task)
        self.logger.log("submit_task", {"task_id": task_id, "task": task})
        with self._lock:
            self.system_state["active_tasks"] = self.task_manager.active_task_count()
        return task_id

    def run(self) -> None:
        """Run the supervisor loop: monitor tasks, agents, and health in real time."""
        self.logger.log("supervisor_start", {})
        while True:
            try:
                # 1. Check for scheduled tasks
                self.scheduler.check_and_schedule(self.task_manager)
                # 2. Dispatch tasks to agents
                self.task_manager.dispatch_tasks(self.agents)
                # 3. Handle interruptions
                self.interrupt_handler.check_interrupts(self.task_manager)
                # 4. Update system state
                with self._lock:
                    self.system_state["active_tasks"] = self.task_manager.active_task_count()
                    self.system_state["health"] = self._assess_health()
                # 5. Log heartbeat
                self.logger.log("supervisor_heartbeat", self.system_state)
                # 6. Sleep or yield
                import time
                time.sleep(1)
            except Exception as e:
                with self._lock:
                    self.system_state["health"] = "red"
                    self.system_state["last_error"] = str(e)
                self.logger.log("supervisor_error", {"error": str(e)})
                break

    def get_status(self) -> Dict[str, Any]:
        """Return live system state."""
        with self._lock:
            return dict(self.system_state)

    def control(self, command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Control tasks: pause, resume, reroute, or kill."""
        result = self.interrupt_handler.handle_command(command, params or {}, self.task_manager)
        self.logger.log("supervisor_control", {"command": command, "params": params, "result": result})
        return result

    def get_metrics(self) -> Dict[str, Any]:
        """Return supervisor health and performance metrics."""
        return {
            "active_agents": len(self.agents),
            "active_tasks": self.task_manager.active_task_count(),
            "scheduled_tasks": self.scheduler.scheduled_task_count(),
            "system_health": self.system_state["health"]
        }

    def _assess_health(self) -> str:
        """Assess system health based on agent/task status."""
        if self.task_manager.has_failed_tasks():
            return "yellow"
        if self.task_manager.active_task_count() > 10:
            return "orange"
        return "green" 