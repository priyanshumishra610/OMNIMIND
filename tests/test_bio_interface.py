"""
Test BCI Adapter
"""
import unittest
from bio_interface.bci_adapter import BCIAdapter

class TestBCIAdapter(unittest.TestCase):
    def setUp(self):
        self.bci = BCIAdapter({"dummy": True})
        
    def test_read_eeg(self):
        result = self.bci.read_eeg()
        self.assertEqual(result, "EEG signal processed")
        
    def test_detect_emotion(self):
        result = self.bci.detect_emotion()
        self.assertEqual(result, "Emotion state detected")
        
    def test_biofeedback(self):
        result = self.bci.get_biofeedback()
        self.assertEqual(result, "Biofeedback collected")

if __name__ == "__main__":
    unittest.main() 