import time
from typing import Callable, Dict, Any

class PerformanceTuner:
    """
    Benchmarks end-to-end latency for OMNIMIND pipelines and APIs.
    Modular and future-proof for integration with CI/CD and release scripts.
    """
    def __init__(self):
        self.results = []

    def benchmark(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Benchmark a function call and record latency.
        Args:
            func (Callable): The function to benchmark.
            *args, **kwargs: Arguments to pass to the function.
        Returns:
            dict: Latency and result.
        """
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        latency = end - start
        record = {"latency": latency, "result": result}
        self.results.append(record)
        return record

    def get_results(self):
        """Return all benchmark results."""
        return self.results 