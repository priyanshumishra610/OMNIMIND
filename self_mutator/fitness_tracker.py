import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FitnessTracker:
    """
    Measures pipeline performance: accuracy, latency, consensus, feedback.
    """

    def __init__(self):
        self.history = []

    def evaluate(self, metrics: Dict[str, Any]) -> float:
        """
        Compute a fitness score from metrics.
        Example: weighted sum of accuracy, consensus, and latency.
        """
        accuracy = metrics.get("accuracy", 0.5)
        consensus = metrics.get("consensus", 0.5)
        latency = metrics.get("latency", 1.0)
        feedback = metrics.get("feedback", 0.5)
        # Lower latency is better, so invert
        score = 0.4 * accuracy + 0.3 * consensus + 0.2 * feedback + 0.1 * (1.0 - min(latency, 1.0))
        logger.info(f"Evaluated fitness: {score:.3f} for metrics: {metrics}")
        self.history.append((metrics, score))
        return score 