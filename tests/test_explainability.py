import unittest
from genesis import explainability

class TestExplainability(unittest.TestCase):
    def test_explain(self):
        xai = explainability.Explainability(config={"dummy": True})
        self.assertEqual(xai.explain(), "Explanation generated")

if __name__ == "__main__":
    unittest.main() 