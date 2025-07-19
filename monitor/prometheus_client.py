"""
Prometheus Client for OMNIMIND

Handles Prometheus monitoring and metrics collection.
"""

from typing import Dict, Any, Optional
import logging
import time

logger = logging.getLogger(__name__)


class PrometheusClient:
    """Prometheus client for OMNIMIND monitoring."""
    
    def __init__(self, metrics_port: int = 9090):
        self.metrics_port = metrics_port
        self.metrics = {}
        self.start_time = time.time()
    
    def record_metric(self, metric_name: str, value: float, 
                     labels: Dict[str, str] = None):
        """Record a metric value."""
        try:
            if metric_name not in self.metrics:
                self.metrics[metric_name] = []
            
            metric_record = {
                "value": value,
                "timestamp": time.time(),
                "labels": labels or {}
            }
            
            self.metrics[metric_name].append(metric_record)
            logger.debug(f"Recorded metric: {metric_name} = {value}")
            
        except Exception as e:
            logger.error(f"Error recording metric {metric_name}: {e}")
    
    def increment_counter(self, counter_name: str, 
                         labels: Dict[str, str] = None):
        """Increment a counter metric."""
        current_value = self.get_counter_value(counter_name)
        self.record_metric(counter_name, current_value + 1, labels)
    
    def get_counter_value(self, counter_name: str) -> float:
        """Get current value of a counter."""
        if counter_name not in self.metrics:
            return 0.0
        
        records = self.metrics[counter_name]
        if not records:
            return 0.0
        
        return records[-1]["value"]
    
    def get_metric_history(self, metric_name: str) -> list:
        """Get history of a metric."""
        return self.metrics.get(metric_name, []).copy()
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all current metrics."""
        current_metrics = {}
        
        for metric_name, records in self.metrics.items():
            if records:
                current_metrics[metric_name] = {
                    "current_value": records[-1]["value"],
                    "total_records": len(records),
                    "last_updated": records[-1]["timestamp"]
                }
        
        return current_metrics
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        uptime = time.time() - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "total_metrics": len(self.metrics),
            "total_records": sum(len(records) for records in self.metrics.values()),
            "start_time": self.start_time
        } 