"""
Life Loop Module
----------------
Manages virtual energy, sleep, and 'dream' cycles for the agent.
Configurable via environment variables or config.py.
"""
import os
from typing import Dict, Any, Optional

try:
    from .config import LIFE_LOOP_CONFIG
except ImportError:
    LIFE_LOOP_CONFIG = {
        'energy_decay': float(os.environ.get('LIFE_LOOP_ENERGY_DECAY', 0.01)),
        'sleep_threshold': float(os.environ.get('LIFE_LOOP_SLEEP_THRESHOLD', 0.2)),
        'dream_mode': os.environ.get('LIFE_LOOP_DREAM_MODE', 'on'),
    }

class LifeLoop:
    """
    Virtual energy/sleep/'dream' cycle manager for the agent.
    Designed for ZenML pipeline integration.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or LIFE_LOOP_CONFIG
        self.energy = 1.0
        self.sleeping = False
        self.dreams = []

    def step(self, activity: str = "idle") -> None:
        """
        Advances the life loop by one step, updating energy and sleep state.
        Args:
            activity (str): Current activity (affects energy decay).
        """
        # Stub: Replace with real logic
        decay = self.config['energy_decay'] * (2 if activity == 'active' else 1)
        self.energy = max(0.0, self.energy - decay)
        if self.energy < self.config['sleep_threshold']:
            self.sleeping = True
            if self.config['dream_mode'] == 'on':
                self.dreams.append('Dreamed...')
        else:
            self.sleeping = False

    def get_state(self) -> Dict[str, Any]:
        """
        Returns the current life loop state.
        Returns:
            dict: State including energy, sleeping, and dreams.
        """
        return {'energy': self.energy, 'sleeping': self.sleeping, 'dreams': self.dreams.copy()} 