import unittest
from dreamscape.dream_logger import DreamLogger

class TestDreamLogger(unittest.TestCase):
    def setUp(self):
        self.logger = DreamLogger({"dummy": True})

    def test_generate_pseudo_dreams(self):
        result = self.logger.generate_pseudo_dreams()
        self.assertIn("Pseudo-dream", result)

    def test_replay_memories(self):
        result = self.logger.replay_memories()
        self.assertIn("Memories replayed", result)

    def test_propose_ideas(self):
        result = self.logger.propose_ideas()
        self.assertIn("Ideas proposed", result)

if __name__ == "__main__":
    unittest.main() 