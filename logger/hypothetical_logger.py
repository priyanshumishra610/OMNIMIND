import os
import json
import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class HypotheticalLogger:
    """
    Logs simulation input, steps, and generated scenarios.
    Stores probability/confidence for each branch.
    """
    def __init__(self, log_path: str = "logs/hypotheticals.jsonl"):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.log_path = log_path

    def log(self, entry: Dict[str, Any]):
        entry["timestamp"] = datetime.utcnow().isoformat()
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        logger.info(f"Logged hypothetical scenario for query: {entry.get('query', '')}")

    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        if not os.path.exists(self.log_path):
            return []
        with open(self.log_path, "r") as f:
            lines = f.readlines()[-limit:]
        return [json.loads(line) for line in lines] 