"""
Task Manager Module
"""
from typing import Dict, List, Any, Optional
import uuid
import time

class TaskManager:
    """Manages task lifecycle and dependencies."""
    
    def __init__(self):
        """Initialize task manager."""
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.task_lineage: Dict[str, List[str]] = {}
    
    def add_task(self, task_data: Dict[str, Any], parent_id: Optional[str] = None) -> str:
        """Add a new task to the manager.
        
        Args:
            task_data: Task configuration and metadata
            parent_id: Optional ID of parent task
            
        Returns:
            String task ID
        """
        task_id = str(uuid.uuid4())
        
        task = {
            "id": task_id,
            "status": "pending",
            "created_at": time.time(),
            "updated_at": time.time(),
            **task_data
        }
        
        self.tasks[task_id] = task
        
        if parent_id:
            if parent_id not in self.tasks:
                raise ValueError(f"Parent task {parent_id} not found")
            self.task_lineage[task_id] = self.get_lineage(parent_id) + [parent_id]
        else:
            self.task_lineage[task_id] = []
            
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task by ID.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task data dict or None if not found
        """
        return self.tasks.get(task_id)
    
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> None:
        """Update task data.
        
        Args:
            task_id: Task identifier
            updates: Fields to update
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
            
        self.tasks[task_id].update(updates)
        self.tasks[task_id]["updated_at"] = time.time()
    
    def get_lineage(self, task_id: str) -> List[str]:
        """Get task ancestry chain.
        
        Args:
            task_id: Task identifier
            
        Returns:
            List of ancestor task IDs
        """
        return self.task_lineage.get(task_id, [])
    
    def dispatch_tasks(self, agents: List[Any]) -> None:
        """Dispatch pending tasks to available agents.
        
        Args:
            agents: List of agent objects that can handle tasks
        """
        for task_id, task in self.tasks.items():
            if task["status"] == "pending":
                for agent in agents:
                    try:
                        agent.handle_task(task)
                        self.update_task(task_id, {
                            "status": "completed",
                            "completed_at": time.time()
                        })
                        break
                    except Exception as e:
                        self.update_task(task_id, {
                            "status": "failed",
                            "error": str(e)
                        }) 