"""
Core Supervisor Module
"""
from typing import Dict, Any, Callable
import threading
import time

class SupervisorCore:
    """Core supervisor class that manages system components and their health."""
    
    def __init__(self):
        """Initialize supervisor core."""
        self.components: Dict[str, Dict[str, Any]] = {}
        self.supervision_thread = None
        self.running = False
        self.check_interval = 5  # seconds
    
    def register_component(self, name: str, config: Dict[str, Any]) -> None:
        """Register a new component for supervision.
        
        Args:
            name: Component identifier
            config: Component configuration including type and health check
        """
        if not isinstance(config, dict) or "type" not in config or "health_check" not in config:
            raise ValueError("Component config must include 'type' and 'health_check'")
            
        if not callable(config["health_check"]):
            raise ValueError("health_check must be callable")
            
        self.components[name] = {
            "config": config,
            "status": "registered",
            "last_check": time.time(),
            "failures": 0
        }
    
    def _supervision_loop(self) -> None:
        """Main supervision loop that checks component health."""
        while self.running:
            for name, component in self.components.items():
                try:
                    health_ok = component["config"]["health_check"]()
                    component["status"] = "healthy" if health_ok else "unhealthy"
                    component["last_check"] = time.time()
                    if not health_ok:
                        component["failures"] += 1
                    else:
                        component["failures"] = 0
                except Exception as e:
                    component["status"] = "error"
                    component["last_error"] = str(e)
                    component["failures"] += 1
            
            time.sleep(self.check_interval)
    
    def start_supervision(self) -> None:
        """Start the supervision thread."""
        if self.supervision_thread and self.supervision_thread.is_alive():
            return
            
        self.running = True
        self.supervision_thread = threading.Thread(
            target=self._supervision_loop,
            daemon=True
        )
        self.supervision_thread.start()
    
    def stop_supervision(self) -> None:
        """Stop the supervision thread."""
        self.running = False
        if self.supervision_thread:
            self.supervision_thread.join(timeout=self.check_interval + 1)
    
    def get_component_status(self, name: str) -> Dict[str, Any]:
        """Get status of a specific component.
        
        Args:
            name: Component identifier
            
        Returns:
            Dict containing component status information
        """
        if name not in self.components:
            raise KeyError(f"Component {name} not found")
            
        component = self.components[name]
        return {
            "status": component["status"],
            "last_check": component["last_check"],
            "failures": component["failures"],
            "type": component["config"]["type"]
        }
    
    def get_all_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered components.
        
        Returns:
            Dict mapping component names to their status information
        """
        return {
            name: self.get_component_status(name)
            for name in self.components
        } 