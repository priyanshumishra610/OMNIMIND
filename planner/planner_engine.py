import threading
from typing import List, Dict, Any, Optional

class PlannerEngine:
    """
    Plans, decomposes, and orders tasks/subtasks from goals.
    Thread-safe and modular for integration with the task loop and agents.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.plans = {}  # goal_id -> plan dict

    def plan_goal(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decompose a goal into an ordered plan of tasks/subtasks.
        Args:
            goal (dict): The goal to plan for.
        Returns:
            dict: Plan with ordered tasks/subtasks.
        """
        with self._lock:
            # Simple heuristic: split by sentences or use metadata['tasks'] if present
            description = goal.get("description", "")
            tasks = []
            if "tasks" in goal.get("metadata", {}):
                tasks = [
                    {"task_id": f"{goal['goal_id']}_t{i+1}", "description": t, "status": "pending"}
                    for i, t in enumerate(goal["metadata"]["tasks"])
                ]
            else:
                # Naive split: each sentence is a task
                for i, sent in enumerate(description.split(".")):
                    sent = sent.strip()
                    if sent:
                        tasks.append({
                            "task_id": f"{goal['goal_id']}_t{i+1}",
                            "description": sent,
                            "status": "pending"
                        })
            plan = {
                "goal_id": goal["goal_id"],
                "tasks": tasks,
                "created_at": goal.get("created_at"),
                "status": "planned"
            }
            self.plans[goal["goal_id"]] = plan
            return plan

    def get_plan(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the plan for a given goal ID.
        """
        with self._lock:
            return self.plans.get(goal_id)

    def update_task_status(self, goal_id: str, task_id: str, status: str) -> bool:
        """
        Update the status of a specific task in a plan.
        """
        with self._lock:
            plan = self.plans.get(goal_id)
            if not plan:
                return False
            for task in plan["tasks"]:
                if task["task_id"] == task_id:
                    task["status"] = status
                    return True
            return False

    def list_plans(self) -> List[Dict[str, Any]]:
        """
        List all current plans.
        """
        with self._lock:
            return list(self.plans.values()) 