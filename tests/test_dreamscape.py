"""
Test Dreamscape Engine
"""
import unittest
from dreamscape.dreamscape import DreamscapeEngine

class TestDreamscape(unittest.TestCase):
    def setUp(self):
        self.engine = DreamscapeEngine()
        
    def test_dream_generation(self):
        """Test dream generation functionality."""
        context = {
            "recent_experiences": ["code_review", "bug_fix", "user_interaction"],
            "emotional_state": "focused",
            "current_goals": ["improve_code_quality"]
        }
        
        dream = self.engine.generate_dream(context)
        self.assertIsInstance(dream, dict)
        self.assertIn("scenario", dream)
        self.assertIn("themes", dream)
        self.assertIn("expected_outcomes", dream)
        
        # Check scenario
        scenario = dream["scenario"]
        self.assertEqual(scenario["type"], "improvement")
        self.assertIn("code_quality", scenario["focus_areas"])
        
        # Check themes
        self.assertIn("quality_improvement", dream["themes"])
        
        # Check outcomes
        outcomes = dream["expected_outcomes"]
        self.assertTrue(any(o["area"] == "code_quality" for o in outcomes))
        
    def test_scenario_creation(self):
        """Test scenario creation functionality."""
        experiences = ["code_review", "bug_fix"]
        emotional_state = "focused"
        
        scenario = self.engine._create_scenario(experiences, emotional_state)
        self.assertEqual(scenario["emotional_tone"], "focused")
        self.assertIn("code_quality", scenario["focus_areas"])
        self.assertIn("reliability", scenario["focus_areas"])
        
    def test_theme_identification(self):
        """Test theme identification functionality."""
        scenario = {
            "type": "improvement",
            "focus_areas": ["code_quality", "reliability"],
            "emotional_tone": "focused"
        }
        goals = ["improve_code_quality"]
        
        themes = self.engine._identify_themes(scenario, goals)
        self.assertIn("quality_improvement", themes)
        self.assertIn("system_stability", themes)

if __name__ == "__main__":
    unittest.main() 