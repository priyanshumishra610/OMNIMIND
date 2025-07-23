"""
Test Neuroplasticity Engine
"""
import unittest
from neuroplasticity.neuroplasticity_engine import NeuroplasticityEngine

class TestNeuroplasticity(unittest.TestCase):
    def setUp(self):
        self.engine = NeuroplasticityEngine({"dummy": True})
        
    def test_rewire(self):
        result = self.engine.rewire("test_pattern")
        self.assertIn("Rewired", result)
        
    def test_prune(self):
        result = self.engine.prune()
        self.assertEqual(result, "Pruned inactive pathways")

if __name__ == "__main__":
    unittest.main() 