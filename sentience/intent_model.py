"""
Intent Model Module
------------------
Manages goal stack, priorities, and urgencies for the agent.
Configurable via environment variables or config.py.
"""
import os
from typing import List, Dict, Any, Optional

try:
    from .config import INTENT_CONFIG
except ImportError:
    INTENT_CONFIG = {
        'max_goals': int(os.environ.get('INTENT_MAX_GOALS', 5)),
        'priority_mode': os.environ.get('INTENT_PRIORITY_MODE', 'fifo'),
    }

class IntentModel:
    """
    Manages goal stack, priorities, and urgencies for the agent.
    Designed for ZenML pipeline integration.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or INTENT_CONFIG
        self.goals = []

    def add_goal(self, goal: str, urgency: float = 0.5) -> None:
        """
        Adds a new goal to the stack.
        Args:
            goal (str): The goal description.
            urgency (float): Urgency level (0-1).
        """
        if len(self.goals) < self.config['max_goals']:
            self.goals.append({'goal': goal, 'urgency': urgency})

    def get_goals(self) -> List[Dict[str, Any]]:
        """
        Returns the current goal stack.
        Returns:
            list: List of goals with urgency.
        """
        return self.goals.copy()

    def prioritize(self) -> List[Dict[str, Any]]:
        """
        Returns the goals sorted by urgency or configured mode.
        Returns:
            list: Prioritized goals.
        """
        if self.config['priority_mode'] == 'urgency':
            return sorted(self.goals, key=lambda g: g['urgency'], reverse=True)
        return self.goals.copy() 