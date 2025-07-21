"""
Sensors Module
--------------
Simulates pseudo-sensors (time, fatigue, etc.) for the agent.
Configurable via environment variables or config.py.
"""
import os
import time
from typing import Dict, Any, Optional

try:
    from .config import SENSORS_CONFIG
except ImportError:
    SENSORS_CONFIG = {
        'fatigue_rate': float(os.environ.get('SENSORS_FATIGUE_RATE', 0.01)),
    }

class Sensors:
    """
    Simulates agent sensors (time, fatigue, etc.).
    Designed for ZenML pipeline integration.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or SENSORS_CONFIG
        self.start_time = time.time()
        self.fatigue = 0.0

    def read(self) -> Dict[str, Any]:
        """
        Reads current sensor values.
        Returns:
            dict: Sensor readings (time, fatigue, etc.).
        """
        elapsed = time.time() - self.start_time
        self.fatigue = min(1.0, self.fatigue + self.config['fatigue_rate'] * elapsed)
        return {
            'elapsed_time': elapsed,
            'fatigue': self.fatigue
        } 