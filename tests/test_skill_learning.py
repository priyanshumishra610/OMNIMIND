import unittest
from genesis import skill_learning

class TestSkillLearning(unittest.TestCase):
    def test_learn(self):
        sl = skill_learning.SkillLearning(config={"dummy": True})
        self.assertEqual(sl.learn(), "Skill learned")

if __name__ == "__main__":
    unittest.main() 