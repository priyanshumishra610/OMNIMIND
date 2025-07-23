import unittest
from genesis.self_mutator import SelfMutator

class TestSelfMutator(unittest.TestCase):
    def setUp(self):
        self.mutator = SelfMutator({"dummy": True})

    def test_monitor(self):
        result = self.mutator.monitor("signal")
        self.assertIn("Signal monitored", result)

    def test_mutate(self):
        result = self.mutator.mutate()
        self.assertIn("Mutation triggered", result)

    def test_log_mutation(self):
        result = self.mutator.log_mutation("mutation")
        self.assertIn("Logged mutation", result)

if __name__ == "__main__":
    unittest.main() 