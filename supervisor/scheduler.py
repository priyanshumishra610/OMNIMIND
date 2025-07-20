import threading
import time
from typing import List, Dict, Any, Optional, Callable

class Scheduler:
    """
    Handles scheduling, delays, periodic and conditional tasks, and watchdogs for OMNIMIND Supervisor.
    Thread-safe and modular for integration with SupervisorCore.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.scheduled = []  # List of (timestamp, task, condition, periodic, interval)
        self.watchdogs = []  # List of (check_fn, action_fn)

    def schedule_task(self, task: Dict[str, Any], delay: float = 0, periodic: bool = False, interval: float = 0, condition: Optional[Callable[[], bool]] = None) -> None:
        """Schedule a task with optional delay, periodicity, and condition."""
        with self._lock:
            run_at = time.time() + delay
            self.scheduled.append((run_at, task, condition, periodic, interval))

    def check_and_schedule(self, task_manager) -> None:
        """Check scheduled tasks and add them to the task manager if ready."""
        now = time.time()
        to_reschedule = []
        with self._lock:
            for entry in self.scheduled:
                run_at, task, condition, periodic, interval = entry
                if now >= run_at and (condition is None or condition()):
                    task_manager.add_task(task)
                    if periodic:
                        to_reschedule.append((now + interval, task, condition, periodic, interval))
                else:
                    to_reschedule.append(entry)
            self.scheduled = to_reschedule
        self._run_watchdogs()

    def add_watchdog(self, check_fn: Callable[[], bool], action_fn: Callable[[], None]) -> None:
        """Add a watchdog that runs check_fn and triggers action_fn if check fails."""
        with self._lock:
            self.watchdogs.append((check_fn, action_fn))

    def _run_watchdogs(self) -> None:
        """Run all watchdogs and trigger actions if checks fail."""
        with self._lock:
            for check_fn, action_fn in self.watchdogs:
                try:
                    if not check_fn():
                        action_fn()
                except Exception:
                    continue

    def scheduled_task_count(self) -> int:
        """Return the number of scheduled tasks."""
        with self._lock:
            return len(self.scheduled) 