"""
Test Hivemind Components
"""
import unittest
from hive.alien_agent import AlienAgent
from hive.hivemind_translator import HivemindTranslator

class TestHivemind(unittest.TestCase):
    def setUp(self):
        self.agent = AlienAgent({"dummy": True})
        self.translator = HivemindTranslator({"dummy": True})
        
    def test_alien_agent(self):
        result = self.agent.reason("test_input")
        self.assertIn("alien logic", result)
        
    def test_translator(self):
        result = self.translator.translate_concept("test_concept")
        self.assertIn("Swarm translation", result)
        
    def test_consensus(self):
        result = self.translator.build_consensus(["view1", "view2"])
        self.assertIn("Consensus built", result)

if __name__ == "__main__":
    unittest.main() 