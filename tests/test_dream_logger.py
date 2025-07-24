"""
Test Dream Logger Module
"""
import unittest
import tempfile
import os
from dreamscape.dream_logger import DreamLogger

class TestDreamLogger(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.logger = DreamLogger(log_dir=self.test_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    def test_log_dream(self):
        """Test dream logging functionality."""
        dream_data = {
            "type": "improvement_scenario",
            "content": "Refactor error handling",
            "insights": ["centralize error processing", "improve user feedback"]
        }
        
        log_entry = self.logger.log_dream(dream_data)
        self.assertIsInstance(log_entry, dict)
        self.assertIn("dream_id", log_entry)
        self.assertIn("timestamp", log_entry)
        self.assertEqual(log_entry["content"], dream_data["content"])
        
        # Verify file was created
        log_file = os.path.join(self.test_dir, "dreams.jsonl")
        self.assertTrue(os.path.exists(log_file))

    def test_get_dreams(self):
        """Test dream retrieval functionality."""
        # Add test dreams
        dreams = [
            {
                "type": "improvement",
                "content": "Test dream 1",
                "insights": ["insight1"]
            },
            {
                "type": "exploration",
                "content": "Test dream 2",
                "insights": ["insight2"]
            }
        ]
        
        for dream in dreams:
            self.logger.log_dream(dream)
            
        # Test retrieval
        all_dreams = self.logger.get_dreams()
        self.assertEqual(len(all_dreams), 2)
        
        # Test filtering by type
        improvement_dreams = self.logger.get_dreams(dream_type="improvement")
        self.assertEqual(len(improvement_dreams), 1)
        self.assertEqual(improvement_dreams[0]["content"], "Test dream 1")

    def test_analyze_insights(self):
        """Test insight analysis functionality."""
        # Add test dreams with insights
        dreams = [
            {
                "type": "improvement",
                "content": "Dream 1",
                "insights": ["performance", "reliability"]
            },
            {
                "type": "exploration",
                "content": "Dream 2",
                "insights": ["performance", "scalability"]
            }
        ]
        
        for dream in dreams:
            self.logger.log_dream(dream)
            
        # Analyze insights
        analysis = self.logger.analyze_insights()
        self.assertEqual(analysis["total_dreams"], 2)
        self.assertEqual(analysis["total_insights"], 4)
        self.assertEqual(analysis["unique_insights"], 3)
        
        # Check top insights
        top_insights = dict(analysis["top_insights"])
        self.assertEqual(top_insights["performance"], 2)

if __name__ == "__main__":
    unittest.main() 