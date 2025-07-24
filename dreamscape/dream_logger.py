"""
Dream Logger Module
"""
from typing import Dict, Any
from datetime import datetime
import json
import os

class DreamLogger:
    """Logs and manages dream records."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.dreams = []
        os.makedirs(log_dir, exist_ok=True)
        
    def log_dream(self, dream_data: Dict[str, Any]) -> Dict[str, Any]:
        """Log a dream record.
        
        Args:
            dream_data: Dictionary containing dream data
            
        Returns:
            Dict containing logged dream entry
        """
        # Create log entry
        log_entry = {
            "dream_id": f"dream_{len(self.dreams)}",
            "timestamp": datetime.utcnow().isoformat(),
            "content": dream_data.get("content"),
            "type": dream_data.get("type"),
            "insights": dream_data.get("insights", [])
        }
        
        # Save to file
        log_file = os.path.join(self.log_dir, "dreams.jsonl")
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
            
        self.dreams.append(log_entry)
        return log_entry
        
    def get_dreams(self, limit: int = None, dream_type: str = None) -> list:
        """Retrieve dream records.
        
        Args:
            limit: Maximum number of records to return
            dream_type: Filter by dream type
            
        Returns:
            List of dream records
        """
        filtered = self.dreams
        
        if dream_type:
            filtered = [d for d in filtered if d.get("type") == dream_type]
            
        if limit:
            filtered = filtered[-limit:]
            
        return filtered
        
    def analyze_insights(self, dream_ids: list = None) -> Dict[str, Any]:
        """Analyze insights from dreams.
        
        Args:
            dream_ids: List of dream IDs to analyze
            
        Returns:
            Dict containing analysis results
        """
        target_dreams = self.dreams
        if dream_ids:
            target_dreams = [d for d in self.dreams if d["dream_id"] in dream_ids]
            
        all_insights = []
        for dream in target_dreams:
            all_insights.extend(dream.get("insights", []))
            
        # Count insight frequencies
        insight_counts = {}
        for insight in all_insights:
            insight_counts[insight] = insight_counts.get(insight, 0) + 1
            
        return {
            "total_dreams": len(target_dreams),
            "total_insights": len(all_insights),
            "unique_insights": len(insight_counts),
            "top_insights": sorted(
                insight_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        } 