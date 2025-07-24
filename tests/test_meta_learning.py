"""
Test Meta Learning Components
"""
import unittest
from unittest.mock import MagicMock
from learning.meta_learning import MetaLearner
from learning.error_analysis import ErrorAnalyzer
from learning.pattern_recognition import PatternRecognizer

class TestMetaLearning(unittest.TestCase):
    def setUp(self):
        self.meta_learner = MetaLearner()
        self.error_analyzer = ErrorAnalyzer()
        self.pattern_recognizer = PatternRecognizer()

    def test_meta_learning_cycle(self):
        """Test meta learning cycle with experiment tracking"""
        experiment = {
            "type": "behavior_adaptation",
            "input": "Handle user request politely",
            "context": {"previous_errors": [], "success_patterns": []}
        }
        result = self.meta_learner.run_experiment(experiment)
        self.assertIsInstance(result, dict)
        self.assertIn("learned_pattern", result)
        self.assertIn("confidence", result)

    def test_error_analysis(self):
        """Test error analysis and learning"""
        error = {
            "type": "response_failure",
            "context": "User request misunderstood",
            "impact": "moderate"
        }
        analysis = self.error_analyzer.analyze(error)
        self.assertIsInstance(analysis, dict)
        self.assertIn("root_cause", analysis)
        self.assertIn("corrective_action", analysis)

    def test_pattern_recognition(self):
        """Test pattern recognition in behavior"""
        behaviors = [
            {"action": "greet", "result": "positive"},
            {"action": "clarify", "result": "positive"},
            {"action": "assist", "result": "positive"}
        ]
        pattern = self.pattern_recognizer.identify_pattern(behaviors)
        self.assertIsInstance(pattern, dict)
        self.assertIn("pattern_type", pattern)
        self.assertIn("confidence_score", pattern)

if __name__ == "__main__":
    unittest.main() 