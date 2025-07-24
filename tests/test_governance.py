"""
Test Governance Components
"""
import unittest
from unittest.mock import MagicMock
from governance.ethics_checker_v2 import EthicsCheckerV2
from governance.constitutional_circuit_breaker import ConstitutionalCircuitBreaker
from governance.constitution import GovernanceLogger

class TestGovernance(unittest.TestCase):
    def setUp(self):
        self.logger = GovernanceLogger()
        self.ethics_checker = EthicsCheckerV2()
        self.circuit_breaker = ConstitutionalCircuitBreaker()

    def test_ethics_checker(self):
        """Test ethics evaluation functionality"""
        action = {
            "type": "code_generation",
            "content": "Generate a greeting message",
            "context": {"purpose": "user_request"}
        }
        result = self.ethics_checker.evaluate_action(action)
        self.assertIsInstance(result, dict)
        self.assertIn("is_ethical", result)
        self.assertIn("reasoning", result)

    def test_circuit_breaker(self):
        """Test constitutional circuit breaker"""
        violation = {
            "type": "unauthorized_action",
            "severity": "high",
            "details": "Attempted system modification"
        }
        result = self.circuit_breaker.check_violation(violation)
        self.assertIsInstance(result, dict)
        self.assertIn("should_break", result)
        self.assertIn("reason", result)

    def test_governance_logging(self):
        """Test governance action logging"""
        action = {
            "type": "policy_enforcement",
            "result": "action_blocked",
            "reason": "violates_ethical_guidelines"
        }
        log_entry = self.logger.log_action(action)
        self.assertIn("timestamp", log_entry)
        self.assertIn("action_type", log_entry)
        self.assertIn("result", log_entry)

if __name__ == "__main__":
    unittest.main() 