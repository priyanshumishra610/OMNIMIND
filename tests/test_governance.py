"""
Test Governance Components
"""
import unittest
from governance.ethics_checker_v2 import EthicsCheckerV2
from governance.constitutional_circuit_breaker import ConstitutionalCircuitBreaker
from governance.omni_ledger import OmniLedger
from pipelines.sovereign_governance_pipeline import sovereign_governance_step

class TestGovernance(unittest.TestCase):
    def test_ethics_checker(self):
        checker = EthicsCheckerV2()
        res = checker.evaluate("dilemma")
        self.assertIn("Evaluated dilemma", res)

    def test_circuit_breaker(self):
        breaker = ConstitutionalCircuitBreaker()
        breaker.check_violation("unlawful action")
        res = breaker.trigger_break()
        self.assertIn("Circuit break", res)

    def test_ledger(self):
        ledger = OmniLedger()
        entry = ledger.log_action("act", lawful=True)
        self.assertIn("action", entry)

    def test_pipeline(self):
        result = sovereign_governance_step()
        self.assertIn("dilemma", result)
        self.assertIn("violation", result)
        self.assertIn("log", result)
        self.assertIn("circuit", result)

if __name__ == "__main__":
    unittest.main() 