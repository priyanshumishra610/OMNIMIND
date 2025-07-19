"""
Base Agent for OMNIMIND

Base class for all agents in the multi-agent swarm system.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all OMNIMIND agents."""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.memory = []
        self.confidence = 0.5
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results."""
        pass
    
    def add_to_memory(self, item: Dict[str, Any]):
        """Add item to agent's memory."""
        self.memory.append(item)
        if len(self.memory) > 100:  # Limit memory size
            self.memory.pop(0)
    
    def get_memory(self) -> List[Dict[str, Any]]:
        """Get agent's memory."""
        return self.memory.copy()
    
    def update_confidence(self, confidence: float):
        """Update agent's confidence level."""
        self.confidence = max(0.0, min(1.0, confidence))
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information."""
        return {
            "name": self.name,
            "role": self.role,
            "confidence": self.confidence,
            "memory_size": len(self.memory)
        } 