"""
Agent Module for World Modeling
"""
from typing import Dict, List, Any

class Agent:
    """Models agent behavior in simulated environments."""
    
    def __init__(self):
        self.actions = []
        self.state = {}
        
    def plan_actions(self, scenario: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan actions based on scenario.
        
        Args:
            scenario: Dictionary containing scenario information
            
        Returns:
            List of planned actions
        """
        # Extract scenario details
        environment = scenario.get("environment", {})
        objectives = scenario.get("objectives", [])
        
        # Plan actions for each objective
        planned_actions = []
        for objective in objectives:
            action = self._create_action_for_objective(objective, environment)
            if action:
                planned_actions.append(action)
                
        # Sort by priority
        planned_actions.sort(key=lambda x: self._get_priority_value(x.get("priority", "low")))
        
        self.actions.extend(planned_actions)
        return planned_actions
        
    def _create_action_for_objective(self, objective: str, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Create an action to achieve an objective.
        
        Args:
            objective: Objective string
            environment: Environment dictionary
            
        Returns:
            Dict containing action details
        """
        action = {
            "type": "analyze",
            "priority": "medium",
            "expected_impact": {
                "positive": [],
                "negative": []
            }
        }
        
        if objective == "optimize_performance":
            action.update({
                "type": "optimize",
                "priority": "high",
                "target": "system_performance",
                "expected_impact": {
                    "positive": ["response_time", "throughput"],
                    "negative": ["resource_usage"]
                }
            })
        elif objective == "maintain_stability":
            action.update({
                "type": "monitor",
                "priority": "critical",
                "target": "system_stability",
                "expected_impact": {
                    "positive": ["reliability", "consistency"],
                    "negative": ["flexibility"]
                }
            })
            
        return action
        
    def _get_priority_value(self, priority: str) -> int:
        """Convert priority string to numeric value.
        
        Args:
            priority: Priority string
            
        Returns:
            Integer priority value
        """
        priority_map = {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3
        }
        return priority_map.get(priority.lower(), 4) 