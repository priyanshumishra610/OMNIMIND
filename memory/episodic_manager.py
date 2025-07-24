"""
Episodic Memory Manager Module
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os

class EpisodicManager:
    """Manages episodic memory storage and retrieval."""
    
    def __init__(self, log_path: str, retention_days: int = 30):
        self.log_path = log_path
        self.retention_days = retention_days
        self.sessions = []
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
    def log_session(self, session_id: str, user_query: str, 
                   response: str, status: str, metadata: Dict[str, Any]) -> None:
        """Log a session to episodic memory.
        
        Args:
            session_id: Unique session identifier
            user_query: User's query
            response: System response
            status: Session status
            metadata: Additional session metadata
        """
        session = {
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "user_query": user_query,
            "response": response,
            "status": status,
            "metadata": metadata
        }
        
        self.sessions.append(session)
        
        # Write to log file
        with open(self.log_path, "a") as f:
            f.write(json.dumps(session) + "\n")
            
    def retrieve_sessions(self, session_id: Optional[str] = None,
                        start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Retrieve sessions from episodic memory.
        
        Args:
            session_id: Optional session ID to filter by
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            List of matching session records
        """
        filtered = self.sessions
        
        if session_id:
            filtered = [s for s in filtered if s["session_id"] == session_id]
            
        if start_date:
            filtered = [s for s in filtered if datetime.fromisoformat(s["timestamp"]) >= start_date]
            
        if end_date:
            filtered = [s for s in filtered if datetime.fromisoformat(s["timestamp"]) <= end_date]
            
        return filtered
        
    def prune_sessions(self) -> int:
        """Prune old sessions beyond retention period.
        
        Returns:
            Number of sessions pruned
        """
        if self.retention_days < 0:
            return 0
            
        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
        original_count = len(self.sessions)
        
        # Remove old sessions
        self.sessions = [
            s for s in self.sessions
            if datetime.fromisoformat(s["timestamp"]) > cutoff_date
        ]
        
        # Count pruned sessions
        pruned_count = original_count - len(self.sessions)
        
        # Rewrite log file with remaining sessions
        if pruned_count > 0:
            with open(self.log_path, "w") as f:
                for session in self.sessions:
                    f.write(json.dumps(session) + "\n")
                    
        return pruned_count 