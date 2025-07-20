import threading
from typing import Dict, Any, Optional

class InterruptHandler:
    """
    Handles task interruptions: pause, kill, reroute, or resume tasks for OMNIMIND Supervisor.
    Thread-safe and modular for integration with SupervisorCore and FastAPI.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.interrupts = {}  # task_id -> interrupt_type

    def check_interrupts(self, task_manager) -> None:
        """Check for interrupts and apply them to tasks."""
        with self._lock:
            for task_id, interrupt_type in list(self.interrupts.items()):
                task = task_manager.get_task(task_id)
                if not task:
                    continue
                if interrupt_type == "pause":
                    task["status"] = "paused"
                elif interrupt_type == "kill":
                    task["status"] = "killed"
                elif interrupt_type == "reroute":
                    task["status"] = "pending"
                # Remove interrupt after handling
                del self.interrupts[task_id]

    def handle_command(self, command: str, params: Dict[str, Any], task_manager) -> Dict[str, Any]:
        """
        Handle a control command (pause, resume, kill, reroute) for tasks.
        Args:
            command (str): The control command.
            params (dict): Parameters, e.g., task_id.
            task_manager: The TaskManager instance.
        Returns:
            dict: Result of the operation.
        """
        task_id = params.get("task_id")
        with self._lock:
            if command == "pause" and task_id:
                self.interrupts[task_id] = "pause"
                return {"status": "paused", "task_id": task_id}
            elif command == "resume" and task_id:
                task = task_manager.get_task(task_id)
                if task and task["status"] == "paused":
                    task["status"] = "pending"
                    return {"status": "resumed", "task_id": task_id}
                return {"status": "not_paused", "task_id": task_id}
            elif command == "kill" and task_id:
                self.interrupts[task_id] = "kill"
                return {"status": "killed", "task_id": task_id}
            elif command == "reroute" and task_id:
                self.interrupts[task_id] = "reroute"
                return {"status": "rerouted", "task_id": task_id}
            else:
                return {"status": "unknown_command", "command": command, "params": params} 