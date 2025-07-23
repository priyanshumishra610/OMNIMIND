import unittest
from multi_modal.virtual_senses import VirtualSenses

class TestVirtualSenses(unittest.TestCase):
    def setUp(self):
        self.senses = VirtualSenses({"dummy": True})

    def test_simulate_sense(self):
        result = self.senses.simulate_sense("taste")
        self.assertIn("Simulated sense", result)

    def test_feed_reasoner(self):
        result = self.senses.feed_reasoner("data")
        self.assertIn("Fed to reasoner", result)

if __name__ == "__main__":
    unittest.main() 