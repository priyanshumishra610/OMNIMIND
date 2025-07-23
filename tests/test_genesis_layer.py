import unittest
from genesis import skill_learning, continual_learning, governance, alignment, zk_reasoner, explainability

class TestGenesisLayer(unittest.TestCase):
    def test_all(self):
        self.assertEqual(skill_learning.SkillLearning().learn(), "Skill learned")
        self.assertEqual(continual_learning.ContinualLearning().update(), "Knowledge updated")
        self.assertEqual(governance.Governance().resolve(), "Conflict resolved")
        self.assertEqual(alignment.Alignment().align(), "Alignment updated")
        self.assertEqual(zk_reasoner.ZKReasoner().prove(), "Proof generated")
        self.assertEqual(explainability.Explainability().explain(), "Explanation generated")

if __name__ == "__main__":
    unittest.main() 