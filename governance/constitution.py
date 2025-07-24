"""
Governance Constitution Module
"""
import logging
import json
from datetime import datetime
from typing import Dict, Any

class GovernanceLogger:
    """Logger for governance actions and decisions."""
    
    def __init__(self):
        self.logger = logging.getLogger("governance")
        self.logger.setLevel(logging.INFO)
        
        # Create handlers if none exist
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Log a governance action.
        
        Args:
            action: Dictionary containing action details
            
        Returns:
            Dict containing the logged entry
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action_type": action.get("type"),
            "result": action.get("result"),
            "reason": action.get("reason")
        }
        
        self.logger.info(json.dumps(log_entry))
        return log_entry 