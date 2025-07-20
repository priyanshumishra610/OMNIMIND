import threading
import time
from typing import Any, Optional

class AgentNode:
    """
    Represents a node in the Hive. Can pull/execute tasks and send heartbeats to the HiveMonitor.
    """
    def __init__(self, node_id: str, monitor: Any = None):
        self.node_id = node_id
        self.monitor = monitor
        self.current_task = None
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        """Start the agent node's main loop (stub)."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the agent node's main loop (stub)."""
        self._stop_event.set()

    def pull_task(self) -> Optional[Any]:
        """Stub: Pull a task from the controller or registry."""
        # Placeholder for actual task-pulling logic
        return None

    def execute_task(self, task: Any):
        """Stub: Execute a given task."""
        self.current_task = task
        # Placeholder for actual execution logic
        time.sleep(0.1)
        self.current_task = None

    def send_heartbeat(self):
        """Send a heartbeat to the monitor (stub)."""
        if self.monitor:
            self.monitor.receive_heartbeat(self.node_id)

    def _run(self):
        while not self._stop_event.is_set():
            task = self.pull_task()
            if task:
                self.execute_task(task)
            self.send_heartbeat()
            time.sleep(1) 