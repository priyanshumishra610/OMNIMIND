"""
Task Scheduler Module
"""
from typing import Dict, List, Any, Callable, Tuple
import time
import heapq

class Scheduler:
    """Manages task scheduling and watchdog timers."""
    
    def __init__(self):
        """Initialize scheduler."""
        self.scheduled_tasks: List[Tuple[float, Dict[str, Any]]] = []
        self.watchdogs: List[Tuple[Callable[[], bool], Callable[[], None]]] = []
    
    def schedule_task(self, task: Dict[str, Any], delay: float) -> None:
        """Schedule a task for future execution.
        
        Args:
            task: Task configuration and metadata
            delay: Delay in seconds before execution
        """
        execution_time = time.time() + delay
        heapq.heappush(self.scheduled_tasks, (execution_time, task))
    
    def check_and_schedule(self, task_manager: Any) -> None:
        """Check for tasks that are ready to be scheduled.
        
        Args:
            task_manager: TaskManager instance to add tasks to
        """
        current_time = time.time()
        
        while self.scheduled_tasks and self.scheduled_tasks[0][0] <= current_time:
            _, task = heapq.heappop(self.scheduled_tasks)
            task_manager.add_task(task)
    
    def add_watchdog(self, condition: Callable[[], bool], action: Callable[[], None]) -> None:
        """Add a watchdog timer with condition and action.
        
        Args:
            condition: Function that returns True when watchdog should trigger
            action: Function to call when watchdog triggers
        """
        self.watchdogs.append((condition, action))
    
    def _run_watchdogs(self) -> None:
        """Run all registered watchdog timers."""
        for condition, action in self.watchdogs:
            try:
                # If condition returns False, trigger the action
                if not condition():
                    action()
            except Exception as e:
                print(f"Watchdog error: {str(e)}")  # Use logger in production
    
    def get_next_execution(self) -> float:
        """Get timestamp of next scheduled task.
        
        Returns:
            Float timestamp or -1 if no tasks scheduled
        """
        if not self.scheduled_tasks:
            return -1
        return self.scheduled_tasks[0][0] 