import threading
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

class GoalManager:
    """
    Manages CRUD operations for goals, tracks status and history.
    Thread-safe and modular for integration with task loop and FastAPI.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.goals = {}  # goal_id -> goal dict
        self.history = []  # List of (timestamp, action, goal_id, details)

    def create_goal(self, description: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Create a new goal and return its ID."""
        with self._lock:
            goal_id = str(uuid.uuid4())
            goal = {
                "goal_id": goal_id,
                "description": description,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "metadata": metadata or {},
                "history": []
            }
            self.goals[goal_id] = goal
            self._log_history("create", goal_id, goal)
            return goal_id

    def get_goal(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a goal by ID."""
        with self._lock:
            return self.goals.get(goal_id)

    def list_goals(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all goals, optionally filtered by status."""
        with self._lock:
            if status:
                return [g for g in self.goals.values() if g["status"] == status]
            return list(self.goals.values())

    def update_goal(self, goal_id: str, description: Optional[str] = None, status: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update a goal's description, status, or metadata."""
        with self._lock:
            goal = self.goals.get(goal_id)
            if not goal:
                return False
            if description:
                goal["description"] = description
            if status:
                goal["status"] = status
            if metadata:
                goal["metadata"].update(metadata)
            goal["updated_at"] = datetime.utcnow().isoformat() + "Z"
            self._log_history("update", goal_id, goal)
            return True

    def delete_goal(self, goal_id: str) -> bool:
        """Delete a goal by ID."""
        with self._lock:
            if goal_id in self.goals:
                goal = self.goals.pop(goal_id)
                self._log_history("delete", goal_id, goal)
                return True
            return False

    def get_history(self, goal_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get the history of all goals or a specific goal."""
        with self._lock:
            if goal_id:
                return [h for h in self.history if h["goal_id"] == goal_id]
            return list(self.history)

    def _log_history(self, action: str, goal_id: str, details: Dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "goal_id": goal_id,
            "details": details.copy()
        }
        self.history.append(entry)
        # Also append to the goal's own history
        if goal_id in self.goals:
            self.goals[goal_id]["history"].append(entry) 