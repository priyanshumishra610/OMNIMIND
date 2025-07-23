"""
Test Quantum ZK Reasoner
"""
import unittest
from omni_shield.quantum_zk import QuantumZKReasoner

class TestQuantumZK(unittest.TestCase):
    def setUp(self):
        self.zk = QuantumZKReasoner({"dummy": True})
        
    def test_generate_proof(self):
        result = self.zk.generate_proof("test_statement")
        self.assertIn("Generated quantum-safe proof", result)
        
    def test_verify_proof(self):
        proof = self.zk.generate_proof("test")
        result = self.zk.verify_proof(proof)
        self.assertIn("Verified proof", result)

if __name__ == "__main__":
    unittest.main() 