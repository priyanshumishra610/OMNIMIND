from typing import Dict, List, Any

class HiveRegistry:
    """
    Tracks AgentNodes and tasks in the Hive.
    """
    def __init__(self):
        self.nodes: Dict[str, Any] = {}
        self.tasks: Dict[str, Any] = {}

    def register_node(self, node_id: str, node: Any):
        """Register a new node in the registry."""
        self.nodes[node_id] = node

    def unregister_node(self, node_id: str):
        """Remove a node from the registry."""
        if node_id in self.nodes:
            del self.nodes[node_id]

    def register_task(self, task_id: str, task: Any):
        """Register a new task in the registry."""
        self.tasks[task_id] = task

    def update_task(self, task_id: str, status: str):
        """Update the status of a task (stub)."""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status

    def get_nodes(self) -> List[str]:
        """Return a list of node IDs."""
        return list(self.nodes.keys())

    def get_tasks(self) -> List[str]:
        """Return a list of task IDs."""
        return list(self.tasks.keys()) 