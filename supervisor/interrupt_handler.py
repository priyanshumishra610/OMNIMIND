"""
Interrupt Handler Module
"""
from typing import Dict, Any

class InterruptHandler:
    """Handles task interrupts and control commands."""
    
    def __init__(self):
        """Initialize interrupt handler."""
        self.pending_interrupts: Dict[str, Dict[str, Any]] = {}
    
    def handle_command(self, command: str, params: Dict[str, Any], task_manager: Any) -> None:
        """Handle a control command for a task.
        
        Args:
            command: Command type (pause, resume, kill, reroute)
            params: Command parameters including task_id
            task_manager: TaskManager instance
        """
        task_id = params.get("task_id")
        if not task_id:
            raise ValueError("task_id required in command parameters")
            
        task = task_manager.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
            
        if command == "pause":
            self.pending_interrupts[task_id] = {
                "type": "pause",
                "applied": False
            }
        elif command == "resume":
            if task_id in self.pending_interrupts:
                del self.pending_interrupts[task_id]
            task_manager.update_task(task_id, {"status": "pending"})
        elif command == "kill":
            self.pending_interrupts[task_id] = {
                "type": "kill",
                "applied": False
            }
        elif command == "reroute":
            self.pending_interrupts[task_id] = {
                "type": "reroute",
                "applied": False
            }
        else:
            raise ValueError(f"Unknown command: {command}")
    
    def check_interrupts(self, task_manager: Any) -> None:
        """Apply pending interrupts to tasks.
        
        Args:
            task_manager: TaskManager instance
        """
        for task_id, interrupt in list(self.pending_interrupts.items()):
            if not interrupt["applied"]:
                task = task_manager.get_task(task_id)
                if not task:
                    del self.pending_interrupts[task_id]
                    continue
                    
                if interrupt["type"] == "pause":
                    task_manager.update_task(task_id, {"status": "paused"})
                elif interrupt["type"] == "kill":
                    task_manager.update_task(task_id, {"status": "killed"})
                elif interrupt["type"] == "reroute":
                    task_manager.update_task(task_id, {"status": "pending"})
                    
                interrupt["applied"] = True
    
    def has_pending_interrupts(self) -> bool:
        """Check if there are any pending interrupts.
        
        Returns:
            Boolean indicating if there are pending interrupts
        """
        return any(not interrupt["applied"] for interrupt in self.pending_interrupts.values()) 