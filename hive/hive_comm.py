from typing import Any, Dict, List

class HiveComm:
    """
    Simulates basic inter-node messaging in the Hive.
    """
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []

    def send_message(self, from_node: str, to_node: str, content: Any):
        """Send a message from one node to another (stub)."""
        msg = {"from": from_node, "to": to_node, "content": content}
        self.messages.append(msg)

    def receive_messages(self, node_id: str) -> List[Dict[str, Any]]:
        """Retrieve all messages for a given node (stub)."""
        msgs = [m for m in self.messages if m["to"] == node_id]
        # Optionally remove delivered messages
        self.messages = [m for m in self.messages if m["to"] != node_id]
        return msgs 