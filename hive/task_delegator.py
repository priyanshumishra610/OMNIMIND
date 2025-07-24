"""
Task Delegation Module
"""
from typing import Dict, List, Any

class TaskDelegator:
    """Handles autonomous task delegation to swarm nodes."""
    
    def __init__(self):
        self.assignments = {}
        self.node_stats = {}
        
    def assign_tasks(self, tasks: List[Dict[str, Any]], nodes: List[Dict[str, Any]]) -> Dict[str, str]:
        """Assign tasks to nodes based on capacity and specialties.
        
        Args:
            tasks: List of task dictionaries
            nodes: List of node dictionaries
            
        Returns:
            Dict mapping task IDs to node IDs
        """
        assignments = {}
        
        # Update node stats
        for node in nodes:
            self.node_stats[node["id"]] = {
                "capacity": node.get("capacity", 1.0),
                "specialties": set(node.get("specialties", []))
            }
            
        # Sort tasks by priority
        sorted_tasks = sorted(tasks, key=lambda x: x.get("priority", "low"))
        
        # Assign tasks
        for task in sorted_tasks:
            best_node = self._find_best_node(task, nodes)
            if best_node:
                assignments[task["id"]] = best_node["id"]
                # Update node capacity
                self.node_stats[best_node["id"]]["capacity"] -= 0.1
                
        self.assignments.update(assignments)
        return assignments
        
    def _find_best_node(self, task: Dict[str, Any], nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find the best node for a given task.
        
        Args:
            task: Task dictionary
            nodes: List of node dictionaries
            
        Returns:
            Best matching node dictionary or None
        """
        best_node = None
        best_score = -1
        
        for node in nodes:
            score = self._calculate_match_score(task, node)
            if score > best_score and self.node_stats[node["id"]]["capacity"] > 0:
                best_score = score
                best_node = node
                
        return best_node
        
    def _calculate_match_score(self, task: Dict[str, Any], node: Dict[str, Any]) -> float:
        """Calculate how well a node matches a task.
        
        Args:
            task: Task dictionary
            node: Node dictionary
            
        Returns:
            Float representing match score
        """
        score = 0.0
        
        # Check specialties match
        if task.get("type") in node.get("specialties", []):
            score += 0.5
            
        # Consider node capacity
        score += self.node_stats[node["id"]]["capacity"] * 0.3
        
        # Priority bonus
        if task.get("priority") == "high" and self.node_stats[node["id"]]["capacity"] > 0.7:
            score += 0.2
            
        return score 