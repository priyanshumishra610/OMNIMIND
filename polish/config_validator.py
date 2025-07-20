import os
from typing import Dict, Any, List

class ConfigValidator:
    """
    Validates .env and runtime settings for OMNIMIND.
    Modular and future-proof for integration with CI/CD and release scripts.
    """
    def __init__(self, env_path: str = ".env"):
        self.env_path = env_path
        self.errors: List[str] = []

    def validate_env(self) -> bool:
        """
        Validate the .env file for required keys (stub).
        Returns True if valid, False otherwise.
        """
        # Placeholder for actual validation logic
        if not os.path.exists(self.env_path):
            self.errors.append(f"Missing {self.env_path}")
            return False
        return True

    def validate_runtime(self, config: Dict[str, Any]) -> bool:
        """
        Validate runtime settings (stub).
        Returns True if valid, False otherwise.
        """
        # Placeholder for actual runtime validation logic
        return True

    def get_errors(self) -> List[str]:
        """Return all validation errors."""
        return self.errors 