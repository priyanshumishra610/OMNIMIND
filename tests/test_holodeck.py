"""
Test Holodeck UI
"""
import unittest
from ui.holodeck.holodeck import HolodeckUI

class TestHolodeck(unittest.TestCase):
    def setUp(self):
        self.holodeck = HolodeckUI({"dummy": True})
        
    def test_render(self):
        result = self.holodeck.render_scene()
        self.assertEqual(result, "Scene rendered")
        
    def test_interaction(self):
        result = self.holodeck.process_interaction("test_input")
        self.assertIn("Processed XR interaction", result)
        
    def test_metrics(self):
        result = self.holodeck.update_metrics(["metric1", "metric2"])
        self.assertIn("Updated 2 metrics", result)

if __name__ == "__main__":
    unittest.main() 