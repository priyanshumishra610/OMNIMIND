import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

class EpisodicMemory:
    """
    Stores and retrieves episodic memory snapshots in JSONL or SQLite.
    """
    def __init__(self, path: str = "memory/episodic_memory.jsonl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path

    def store_memory(self, data: Dict[str, Any]) -> str:
        """
        Stores a memory snapshot and returns its unique ID.
        """
        memory_id = str(uuid.uuid4())
        data = dict(data)
        data["id"] = memory_id
        data["timestamp"] = data.get("timestamp") or datetime.utcnow().isoformat()
        with open(self.path, "a") as f:
            f.write(json.dumps(data) + "\n")
        return memory_id

    def get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a memory snapshot by its unique ID.
        """
        for mem in self.get_all_memories():
            if mem.get("id") == memory_id:
                return mem
        return None

    def get_all_memories(self) -> List[Dict[str, Any]]:
        """
        Returns all stored memory snapshots.
        """
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r") as f:
            return [json.loads(line) for line in f if line.strip()] 