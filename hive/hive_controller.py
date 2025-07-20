from typing import List, Any, Optional

class HiveController:
    """
    Controls the Hive: spawns AgentNodes and assigns tasks.
    """
    def __init__(self):
        self.nodes: List[Any] = []
        self.tasks: List[Any] = []

    def spawn_node(self, node: Any):
        """Add a new AgentNode to the hive."""
        self.nodes.append(node)

    def assign_task(self, task: Any, node: Optional[Any] = None):
        """Assign a task to a node (stub)."""
        if node:
            # Placeholder for actual assignment logic
            pass
        else:
            # Assign to first available node (stub)
            if self.nodes:
                pass
        self.tasks.append(task)

    def get_nodes(self) -> List[Any]:
        """Return the list of nodes."""
        return self.nodes

    def get_tasks(self) -> List[Any]:
        """Return the list of tasks."""
        return self.tasks 