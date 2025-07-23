import unittest
from governance.self_regulator import SelfRegulator

class TestSelfRegulator(unittest.TestCase):
    def setUp(self):
        self.reg = SelfRegulator({"dummy": True})

    def test_guardrail(self):
        result = self.reg.guardrail("mutation")
        self.assertIn("Guardrail checked", result)

    def test_vote_on_edit(self):
        result = self.reg.vote_on_edit("edit")
        self.assertIn("Voted on edit", result)

    def test_tie_to_constitution(self):
        result = self.reg.tie_to_constitution("action")
        self.assertIn("Tied to constitution", result)

if __name__ == "__main__":
    unittest.main() 