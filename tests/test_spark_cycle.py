import unittest
from pipelines.spark_cycle import spark_cycle_step

class TestSparkCycle(unittest.TestCase):
    def test_spark_cycle(self):
        result = spark_cycle_step()
        self.assertIn("thought", result)
        self.assertIn("reflection", result)
        self.assertIn("sim_result", result)
        self.assertIn("mutation", result)
        self.assertIn("dream_log", result)
        self.assertIn("sense", result)

if __name__ == "__main__":
    unittest.main() 