from typing import Dict, Any

class PermissionManager:
    """
    Enforces fine-grained permission scopes for OMNI-SHIELD.
    Modular and future-proof for integration with sandbox and agents.
    """
    def __init__(self):
        self.permissions: Dict[str, Any] = {}

    def set_permission(self, entity: str, scope: str, allowed: bool):
        """Set permission for an entity and scope."""
        self.permissions[(entity, scope)] = allowed

    def check_permission(self, entity: str, scope: str) -> bool:
        """Check if an entity has permission for a scope."""
        return self.permissions.get((entity, scope), False)

    def revoke_permission(self, entity: str, scope: str):
        """Revoke permission for an entity and scope."""
        if (entity, scope) in self.permissions:
            del self.permissions[(entity, scope)] 