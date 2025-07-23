import unittest
from world_model.meta_simulator import MetaSimulator

class TestMetaSimulator(unittest.TestCase):
    def setUp(self):
        self.sim = MetaSimulator({"dummy": True})

    def test_simulate(self):
        result = self.sim.simulate("Test scenario")
        self.assertIn("Simulated", result)

    def test_predict_outcomes(self):
        outcomes = self.sim.predict_outcomes("Test scenario")
        self.assertIsInstance(outcomes, list)
        self.assertGreater(len(outcomes), 0)

    def test_feed_to_planner(self):
        result = self.sim.feed_to_planner("Best action")
        self.assertIn("Fed to planner", result)

if __name__ == "__main__":
    unittest.main() 