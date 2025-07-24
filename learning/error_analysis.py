"""
Error Analysis Module
"""
from typing import Dict, Any

class ErrorAnalyzer:
    """Analyzes errors and suggests corrective actions."""
    
    def __init__(self):
        self.error_history = []
        
    def analyze(self, error: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze an error and suggest corrections.
        
        Args:
            error: Dictionary containing error information
            
        Returns:
            Dict containing analysis results
        """
        # Record error
        self.error_history.append({
            "type": error.get("type"),
            "context": error.get("context"),
            "impact": error.get("impact")
        })
        
        # Analyze root cause
        root_cause = self._identify_root_cause(error)
        
        # Determine corrective action
        corrective_action = self._determine_corrective_action(root_cause)
        
        return {
            "root_cause": root_cause,
            "corrective_action": corrective_action,
            "similar_errors": self._find_similar_errors(error)
        }
        
    def _identify_root_cause(self, error: Dict[str, Any]) -> Dict[str, Any]:
        """Identify the root cause of an error.
        
        Args:
            error: Error dictionary
            
        Returns:
            Dict containing root cause analysis
        """
        cause = {
            "category": "unknown",
            "confidence": 0.0,
            "factors": []
        }
        
        if error.get("type") == "response_failure":
            cause.update({
                "category": "comprehension",
                "confidence": 0.8,
                "factors": ["input_parsing", "context_understanding"]
            })
        elif "misunderstood" in error.get("context", "").lower():
            cause.update({
                "category": "communication",
                "confidence": 0.7,
                "factors": ["clarity", "ambiguity"]
            })
            
        return cause
        
    def _determine_corrective_action(self, root_cause: Dict[str, Any]) -> Dict[str, Any]:
        """Determine appropriate corrective action.
        
        Args:
            root_cause: Root cause dictionary
            
        Returns:
            Dict containing corrective action
        """
        action = {
            "type": "investigation",
            "priority": "medium",
            "steps": []
        }
        
        if root_cause["category"] == "comprehension":
            action.update({
                "type": "enhancement",
                "priority": "high",
                "steps": [
                    "improve_input_validation",
                    "enhance_context_processing"
                ]
            })
        elif root_cause["category"] == "communication":
            action.update({
                "type": "clarification",
                "priority": "high",
                "steps": [
                    "request_clarification",
                    "validate_understanding"
                ]
            })
            
        return action
        
    def _find_similar_errors(self, error: Dict[str, Any]) -> list:
        """Find similar errors in history.
        
        Args:
            error: Current error dictionary
            
        Returns:
            List of similar errors
        """
        similar = []
        
        for past_error in self.error_history[:-1]:  # Exclude current error
            if past_error["type"] == error.get("type"):
                similar.append(past_error)
                
        return similar 