import os
import json
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

class EpisodicManager:
    """
    Manages episodic memory: logs, retrieves, and prunes session episodes.
    Stores each episode as a JSONL entry for hashable, auditable logs.
    Configurable via environment variables.
    Thread-safe for concurrent access.
    """
    def __init__(self, log_path: Optional[str] = None, retention_days: Optional[int] = None):
        """
        Args:
            log_path (str): Path to the episodic memory log file (JSONL).
            retention_days (int): Number of days to retain episodes before pruning.
        """
        self.log_path = log_path or os.getenv("EPISODIC_MEMORY_LOG", "memory/episodic_memory.jsonl")
        self.retention_days = retention_days or int(os.getenv("EPISODIC_MEMORY_RETENTION_DAYS", "30"))
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_session(self, session_id: str, user_query: str, agent_thoughts: str, feedback: Optional[str] = None, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Logs a session episode to episodic memory.
        Args:
            session_id (str): Unique session identifier.
            user_query (str): The user's query or input.
            agent_thoughts (str): Agent's internal thoughts or reasoning.
            feedback (str, optional): User or system feedback.
            extra (dict, optional): Any additional metadata.
        """
        episode = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "session_id": session_id,
            "user_query": user_query,
            "agent_thoughts": agent_thoughts,
            "feedback": feedback,
            "extra": extra or {}
        }
        with self._lock, open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(episode, sort_keys=True) + "\n")

    def retrieve_sessions(self, session_id: Optional[str] = None, since: Optional[datetime] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieves session episodes, optionally filtered by session_id and/or time.
        Args:
            session_id (str, optional): Filter by session ID.
            since (datetime, optional): Only return episodes after this time.
            limit (int, optional): Max number of episodes to return (most recent first).
        Returns:
            List[Dict]: List of episode dicts.
        """
        episodes = []
        with self._lock:
            if not os.path.exists(self.log_path):
                return []
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        ep = json.loads(line)
                        if session_id and ep.get("session_id") != session_id:
                            continue
                        if since:
                            ep_time = datetime.fromisoformat(ep["timestamp"].replace("Z", ""))
                            if ep_time < since:
                                continue
                        episodes.append(ep)
                    except Exception:
                        continue
        episodes.sort(key=lambda x: x["timestamp"], reverse=True)
        if limit:
            episodes = episodes[:limit]
        return episodes

    def prune_sessions(self) -> int:
        """
        Prunes episodes older than the retention period.
        Returns:
            int: Number of episodes removed.
        """
        cutoff = datetime.utcnow() - timedelta(days=self.retention_days)
        kept, removed = [], 0
        with self._lock:
            if not os.path.exists(self.log_path):
                return 0
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        ep = json.loads(line)
                        ep_time = datetime.fromisoformat(ep["timestamp"].replace("Z", ""))
                        if ep_time >= cutoff:
                            kept.append(ep)
                        else:
                            removed += 1
                    except Exception:
                        continue
            with open(self.log_path, "w", encoding="utf-8") as f:
                for ep in kept:
                    f.write(json.dumps(ep, sort_keys=True) + "\n")
        return removed 