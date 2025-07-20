import os
import json
import threading
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib

class ShieldLogger:
    """
    Logs all OMNI-SHIELD actions and hashes logs for immutability.
    Thread-safe and configurable via environment variables.
    """
    def __init__(self, log_path: Optional[str] = None):
        self.log_path = log_path or os.getenv("SHIELD_LOG", "logs/shield_actions.jsonl")
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log(self, action: str, data: Dict[str, Any], extra: Optional[Dict[str, Any]] = None) -> str:
        """
        Logs a shield action/decision.
        Args:
            action (str): Action or decision type.
            data (dict): The data involved in the action.
            extra (dict, optional): Additional metadata.
        Returns:
            str: SHA256 hash of the log entry (for immutability verification).
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "data": data,
            "extra": extra or {}
        }
        entry_json = json.dumps(entry, sort_keys=True)
        entry_hash = hashlib.sha256(entry_json.encode("utf-8")).hexdigest()
        entry["hash"] = entry_hash
        with self._lock, open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
        return entry_hash 