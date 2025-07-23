import unittest
from genesis import alignment

class TestAlignment(unittest.TestCase):
    def test_align(self):
        al = alignment.Alignment(config={"dummy": True})
        self.assertEqual(al.align(), "Alignment updated")

if __name__ == "__main__":
    unittest.main() 