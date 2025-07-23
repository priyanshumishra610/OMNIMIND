import unittest
from omega.omega_inner_voice import OmegaInnerVoice

class TestInnerVoice(unittest.TestCase):
    def setUp(self):
        self.voice = OmegaInnerVoice({"dummy": True})

    def test_think(self):
        result = self.voice.think("Test thought")
        self.assertIn("Thinking", result)

    def test_reflect(self):
        result = self.voice.reflect()
        self.assertIn("Meta-reflection", result)

    def test_store_meta_reflection(self):
        result = self.voice.store_meta_reflection("Reflection")
        self.assertIn("Stored", result)

if __name__ == "__main__":
    unittest.main() 