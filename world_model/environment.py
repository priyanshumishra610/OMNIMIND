"""
Environment Module for World Modeling
"""
from typing import Dict, List, Any
from datetime import datetime

class Environment:
    """Manages simulated environment state and variables."""
    
    def __init__(self):
        self.environments = []
        self.current_env = None
        
    def generate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a new environment based on configuration.
        
        Args:
            config: Dictionary containing environment configuration
            
        Returns:
            Dict containing generated environment
        """
        # Create environment record
        env_record = {
            "id": f"env_{len(self.environments)}",
            "timestamp": datetime.utcnow().isoformat(),
            "config": config,
            "state": self._initialize_state(config)
        }
        
        # Set up variables
        env_record["variables"] = self._setup_variables(config.get("variables", []))
        
        # Apply constraints
        env_record["constraints"] = self._apply_constraints(config.get("constraints", {}))
        
        self.environments.append(env_record)
        self.current_env = env_record
        return env_record
        
    def _initialize_state(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize environment state.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dict containing initial state
        """
        state = {
            "complexity": config.get("complexity", "medium"),
            "stability": 1.0,
            "resources": {}
        }
        
        # Set up resource states
        if config.get("constraints", {}).get("resources") == "limited":
            state["resources"] = {
                "memory": 0.8,
                "cpu": 0.7,
                "storage": 0.9
            }
        else:
            state["resources"] = {
                "memory": 1.0,
                "cpu": 1.0,
                "storage": 1.0
            }
            
        return state
        
    def _setup_variables(self, variables: List[str]) -> Dict[str, Any]:
        """Set up environment variables.
        
        Args:
            variables: List of variable names
            
        Returns:
            Dict containing variable configurations
        """
        var_config = {}
        
        for var in variables:
            var_config[var] = {
                "current_value": 0.5,  # Default starting value
                "min_value": 0.0,
                "max_value": 1.0,
                "dependencies": []
            }
            
            # Add specific configurations
            if var == "code_quality":
                var_config[var]["dependencies"] = ["system_load"]
            elif var == "system_load":
                var_config[var]["dependencies"] = ["user_satisfaction"]
            elif var == "user_satisfaction":
                var_config[var]["current_value"] = 0.7  # Start with good satisfaction
                
        return var_config
        
    def _apply_constraints(self, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment constraints.
        
        Args:
            constraints: Dictionary of constraints
            
        Returns:
            Dict containing applied constraints
        """
        applied = {}
        
        for constraint_type, value in constraints.items():
            if constraint_type == "resources":
                applied["resource_limits"] = {
                    "enabled": value == "limited",
                    "recovery_rate": 0.1 if value == "limited" else 0.5
                }
            elif constraint_type == "time":
                applied["time_constraints"] = {
                    "enabled": value == "bounded",
                    "max_steps": 100 if value == "bounded" else float("inf")
                }
                
        return applied 