import threading
import time
from typing import Dict, Any

class HiveMonitor:
    """
    Monitors AgentNodes in the Hive. Receives heartbeats and detects dead nodes.
    """
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self.heartbeats: Dict[str, float] = {}
        self._lock = threading.Lock()

    def receive_heartbeat(self, node_id: str):
        """Receive a heartbeat from a node."""
        with self._lock:
            self.heartbeats[node_id] = time.time()

    def detect_dead_nodes(self) -> Dict[str, Any]:
        """Detect nodes that have not sent a heartbeat within the timeout."""
        now = time.time()
        dead = []
        with self._lock:
            for node_id, last in self.heartbeats.items():
                if now - last > self.timeout:
                    dead.append(node_id)
        return {"dead_nodes": dead}

    def get_heartbeats(self) -> Dict[str, float]:
        """Return the last heartbeat times for all nodes."""
        with self._lock:
            return dict(self.heartbeats) 