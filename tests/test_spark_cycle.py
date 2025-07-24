"""
Test Spark Cycle Components
"""
import unittest
from unittest.mock import MagicMock
from dreamscape.dreamscape import DreamscapeEngine
from dreamscape.dream_logger import DreamLogger
from simulator.simulator import SimulationEngine

class TestSparkCycle(unittest.TestCase):
    def setUp(self):
        self.dream_engine = DreamscapeEngine()
        self.dream_logger = DreamLogger()
        self.sim_engine = SimulationEngine()

    def test_dream_generation(self):
        """Test dream scenario generation"""
        context = {
            "recent_experiences": ["code_review", "bug_fix", "user_interaction"],
            "emotional_state": "focused",
            "current_goals": ["improve_code_quality"]
        }
        dream = self.dream_engine.generate_dream(context)
        self.assertIsInstance(dream, dict)
        self.assertIn("scenario", dream)
        self.assertIn("themes", dream)
        self.assertIn("expected_outcomes", dream)

    def test_dream_logging(self):
        """Test dream logging and retrieval"""
        dream_data = {
            "type": "improvement_scenario",
            "content": "Refactor error handling",
            "insights": ["centralize error processing", "improve user feedback"]
        }
        log_entry = self.dream_logger.log_dream(dream_data)
        self.assertIn("timestamp", log_entry)
        self.assertIn("dream_id", log_entry)
        self.assertIn("content", log_entry)

    def test_scenario_simulation(self):
        """Test scenario simulation and outcome analysis"""
        scenario = {
            "type": "process_optimization",
            "initial_state": {"efficiency": 0.7, "error_rate": 0.3},
            "proposed_changes": ["parallel_processing", "error_caching"]
        }
        simulation = self.sim_engine.run_simulation(scenario)
        self.assertIsInstance(simulation, dict)
        self.assertIn("final_state", simulation)
        self.assertIn("improvements", simulation)
        self.assertIn("risks", simulation)

if __name__ == "__main__":
    unittest.main() 