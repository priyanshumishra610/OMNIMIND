import threading
import uuid
from typing import List, Dict, Any, Optional

class TaskManager:
    """
    Manages the task queue, subtasks, retries, and task lineage for OMNIMIND Supervisor.
    Thread-safe and modular for integration with SupervisorCore.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.tasks = {}  # task_id -> task dict
        self.queue = []  # list of task_ids
        self.failed_tasks = set()
        self.lineage = {}  # task_id -> parent_id

    def add_task(self, task: Dict[str, Any], parent_id: Optional[str] = None) -> str:
        """Add a new task to the queue. Returns the task_id."""
        with self._lock:
            task_id = str(uuid.uuid4())
            task["task_id"] = task_id
            task["status"] = "pending"
            task["retries"] = 0
            self.tasks[task_id] = task
            self.queue.append(task_id)
            if parent_id:
                self.lineage[task_id] = parent_id
            return task_id

    def dispatch_tasks(self, agents: List[Any]) -> None:
        """Dispatch tasks to available agents in parallel."""
        with self._lock:
            for agent in agents:
                if self.queue:
                    task_id = self.queue.pop(0)
                    task = self.tasks[task_id]
                    try:
                        agent.handle_task(task)
                        task["status"] = "completed"
                    except Exception as e:
                        task["status"] = "failed"
                        task["error"] = str(e)
                        self.failed_tasks.add(task_id)
                        # Retry logic
                        if task["retries"] < 3:
                            task["retries"] += 1
                            self.queue.append(task_id)

    def active_task_count(self) -> int:
        """Return the number of active (pending or running) tasks."""
        with self._lock:
            return sum(1 for t in self.tasks.values() if t["status"] in ("pending", "running"))

    def has_failed_tasks(self) -> bool:
        """Return True if there are failed tasks."""
        with self._lock:
            return bool(self.failed_tasks)

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a task by ID."""
        with self._lock:
            return self.tasks.get(task_id)

    def get_lineage(self, task_id: str) -> List[str]:
        """Return the lineage (ancestry) of a task."""
        lineage = []
        current = task_id
        with self._lock:
            while current in self.lineage:
                parent = self.lineage[current]
                lineage.append(parent)
                current = parent
        return lineage 