import os
import json
import threading
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib

class MemoryLogger:
    """
    Logs all memory operations (create, update, delete) in JSONL format with timestamps.
    Ensures logs are hashable for the Immutable Verifier.
    Thread-safe and configurable via environment variables.
    """
    def __init__(self, log_path: Optional[str] = None):
        """
        Args:
            log_path (str): Path to the memory operation log file (JSONL).
        """
        self.log_path = log_path or os.getenv("MEMORY_OP_LOG", "logs/memory_ops.jsonl")
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log(self, operation: str, memory_type: str, data: Dict[str, Any], extra: Optional[Dict[str, Any]] = None) -> str:
        """
        Logs a memory operation.
        Args:
            operation (str): Operation type ('create', 'update', 'delete').
            memory_type (str): Type of memory (episodic, semantic, procedural).
            data (dict): The data involved in the operation.
            extra (dict, optional): Additional metadata.
        Returns:
            str: SHA256 hash of the log entry (for immutability verification).
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "operation": operation,
            "memory_type": memory_type,
            "data": data,
            "extra": extra or {}
        }
        entry_json = json.dumps(entry, sort_keys=True)
        entry_hash = hashlib.sha256(entry_json.encode("utf-8")).hexdigest()
        entry["hash"] = entry_hash
        with self._lock, open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
        return entry_hash 