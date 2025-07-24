"""
Predictor Module for World Modeling
"""
from typing import Dict, List, Any

class Predictor:
    """Predicts consequences of actions in simulated environments."""
    
    def __init__(self):
        self.predictions = []
        self.impact_weights = {
            "refactor": {"code_quality": 0.8, "technical_debt": -0.6},
            "optimize": {"system_performance": 0.7, "resource_usage": 0.4}
        }
        
    def predict_consequences(self, action_sequence: List[Dict[str, Any]], current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Predict consequences of an action sequence.
        
        Args:
            action_sequence: List of action dictionaries
            current_state: Dictionary of current state
            
        Returns:
            Dict containing prediction results
        """
        # Initialize prediction
        prediction = {
            "future_states": [current_state.copy()],
            "risks": [],
            "opportunities": []
        }
        
        # Process each action
        for action in action_sequence:
            next_state = self._compute_next_state(prediction["future_states"][-1], action)
            prediction["future_states"].append(next_state)
            
            # Analyze changes
            changes = self._analyze_state_changes(
                prediction["future_states"][-2],
                next_state
            )
            
            # Identify risks and opportunities
            risks, opportunities = self._evaluate_changes(changes)
            prediction["risks"].extend(risks)
            prediction["opportunities"].extend(opportunities)
            
        self.predictions.append(prediction)
        return prediction
        
    def _compute_next_state(self, current_state: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
        """Compute next state based on action.
        
        Args:
            current_state: Current state dictionary
            action: Action dictionary
            
        Returns:
            Dict containing next state
        """
        next_state = current_state.copy()
        
        # Apply action impacts
        action_type = action.get("type", "").lower()
        if action_type in self.impact_weights:
            for metric, weight in self.impact_weights[action_type].items():
                if metric in next_state:
                    next_state[metric] = max(0.0, min(1.0, next_state[metric] + weight * 0.1))
                    
        return next_state
        
    def _analyze_state_changes(self, before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, float]:
        """Analyze changes between states.
        
        Args:
            before: State before action
            after: State after action
            
        Returns:
            Dict mapping metrics to change values
        """
        changes = {}
        
        for metric in before:
            if metric in after:
                changes[metric] = after[metric] - before[metric]
                
        return changes
        
    def _evaluate_changes(self, changes: Dict[str, float]) -> tuple:
        """Evaluate changes to identify risks and opportunities.
        
        Args:
            changes: Dictionary of metric changes
            
        Returns:
            Tuple of (risks, opportunities) lists
        """
        risks = []
        opportunities = []
        
        for metric, change in changes.items():
            if change > 0.2:
                opportunities.append({
                    "type": "significant_improvement",
                    "metric": metric,
                    "magnitude": change
                })
            elif change < -0.2:
                risks.append({
                    "type": "significant_degradation",
                    "metric": metric,
                    "magnitude": abs(change)
                })
            elif -0.1 <= change <= 0.1:
                risks.append({
                    "type": "insufficient_impact",
                    "metric": metric,
                    "magnitude": abs(change)
                })
                
        return risks, opportunities 