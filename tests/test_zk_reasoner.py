import unittest
from genesis import zk_reasoner

class TestZKReasoner(unittest.TestCase):
    def test_prove(self):
        zk = zk_reasoner.ZKReasoner(config={"dummy": True})
        self.assertEqual(zk.prove(), "Proof generated")

if __name__ == "__main__":
    unittest.main() 