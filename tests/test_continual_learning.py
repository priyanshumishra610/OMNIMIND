import unittest
from genesis import continual_learning

class TestContinualLearning(unittest.TestCase):
    def test_update(self):
        cl = continual_learning.ContinualLearning(config={"dummy": True})
        self.assertEqual(cl.update(), "Knowledge updated")

if __name__ == "__main__":
    unittest.main() 