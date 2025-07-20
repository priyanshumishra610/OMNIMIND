import threading
import time
from typing import Any, List, Dict, Optional
from planner.goal_manager import GoalManager
from planner.planner_engine import PlannerEngine

class AutoLoop:
    """
    Autonomous loop that watches goals, runs the planner, and calls agents/plugins.
    Thread-safe and modular for integration with FastAPI and pipelines.
    """
    def __init__(self, goal_manager: GoalManager, planner: PlannerEngine, agents: Optional[List[Any]] = None, plugins: Optional[List[Any]] = None, loop_interval: float = 2.0):
        self.goal_manager = goal_manager
        self.planner = planner
        self.agents = agents or []
        self.plugins = plugins or []
        self.loop_interval = loop_interval
        self._stop_event = threading.Event()
        self._thread = None
        self.loop_status = "stopped"
        self.last_error = None

    def start(self):
        """Start the autonomous loop in a background thread."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self.loop_status = "running"

    def stop(self):
        """Stop the autonomous loop."""
        self._stop_event.set()
        self.loop_status = "stopped"

    def status(self) -> Dict[str, Any]:
        """Return the current status of the loop."""
        return {
            "status": self.loop_status,
            "thread_alive": self._thread.is_alive() if self._thread else False,
            "last_error": self.last_error
        }

    def _run_loop(self):
        while not self._stop_event.is_set():
            try:
                # 1. Get all pending goals
                pending_goals = self.goal_manager.list_goals(status="pending")
                for goal in pending_goals:
                    # 2. Plan for the goal if not already planned
                    plan = self.planner.get_plan(goal["goal_id"])
                    if not plan:
                        plan = self.planner.plan_goal(goal)
                    # 3. Execute tasks in order
                    for task in plan["tasks"]:
                        if task["status"] == "pending":
                            # Call agents/plugins to handle the task
                            handled = False
                            for agent in self.agents:
                                try:
                                    agent.handle_task(task)
                                    handled = True
                                    break
                                except Exception:
                                    continue
                            if not handled:
                                for plugin in self.plugins:
                                    try:
                                        plugin.handle_task(task)
                                        handled = True
                                        break
                                    except Exception:
                                        continue
                            if handled:
                                self.planner.update_task_status(goal["goal_id"], task["task_id"], "completed")
                            else:
                                self.planner.update_task_status(goal["goal_id"], task["task_id"], "failed")
                    # 4. Mark goal as completed if all tasks are done
                    plan = self.planner.get_plan(goal["goal_id"])
                    if all(t["status"] == "completed" for t in plan["tasks"]):
                        self.goal_manager.update_goal(goal["goal_id"], status="completed")
                self.loop_status = "running"
                self.last_error = None
            except Exception as e:
                self.loop_status = "error"
                self.last_error = str(e)
            time.sleep(self.loop_interval) 