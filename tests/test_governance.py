"""
Test Governance Components
"""
import unittest
from governance.constitution import Constitution
from governance.vote_engine import VoteEngine
from governance.rollback_guard import RollbackGuard

class TestGovernance(unittest.TestCase):
    def setUp(self):
        self.constitution = Constitution({"dummy": True})
        self.vote = VoteEngine({"dummy": True})
        self.guard = RollbackGuard({"dummy": True})
        
    def test_constitution(self):
        result = self.constitution.verify_alignment("test_action")
        self.assertIn("Alignment verified", result)
        
    def test_voting(self):
        prop_id = self.vote.propose("test_proposal")
        vote_result = self.vote.vote(prop_id, True)
        ratify_result = self.vote.ratify(prop_id)
        self.assertIn("Vote cast", vote_result)
        self.assertIn("Ratified", ratify_result)
        
    def test_rollback(self):
        checkpoint = self.guard.checkpoint()
        drift = self.guard.detect_drift()
        rollback = self.guard.rollback("test_checkpoint")
        self.assertEqual(checkpoint, "Checkpoint created")
        self.assertEqual(drift, "Drift analysis complete")
        self.assertIn("Rolled back", rollback)

if __name__ == "__main__":
    unittest.main() 