import threading
import time
from typing import Callable, Optional

class Watchdog:
    """
    Monitors the health of the autonomous loop and restarts it if stuck.
    Thread-safe and modular for integration with AutoLoop and FastAPI.
    """
    def __init__(self, check_fn: Callable[[], bool], restart_fn: Callable[[], None], interval: float = 5.0, max_failures: int = 3):
        self.check_fn = check_fn
        self.restart_fn = restart_fn
        self.interval = interval
        self.max_failures = max_failures
        self._fail_count = 0
        self._stop_event = threading.Event()
        self._thread = None
        self.status = "stopped"

    def start(self):
        """Start the watchdog in a background thread."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self.status = "running"

    def stop(self):
        """Stop the watchdog."""
        self._stop_event.set()
        self.status = "stopped"

    def _run(self):
        while not self._stop_event.is_set():
            try:
                healthy = self.check_fn()
                if healthy:
                    self._fail_count = 0
                else:
                    self._fail_count += 1
                    if self._fail_count >= self.max_failures:
                        self.restart_fn()
                        self._fail_count = 0
                self.status = "running"
            except Exception:
                self.status = "error"
            time.sleep(self.interval)

    def get_status(self) -> str:
        return self.status 