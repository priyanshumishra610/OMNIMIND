"""
Immutable Verifier for OMNIMIND

Handles cryptographic proof trails and verification.
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ImmutableVerifier:
    """Handles immutable verification and proof trails."""
    
    def __init__(self, ledger_path: str = "./data/ledger"):
        self.ledger_path = ledger_path
        self.proof_chain = []
        self.verification_history = []
    
    def create_proof(self, data: Dict[str, Any], proof_type: str = "answer") -> Dict[str, Any]:
        """Create an immutable proof for data."""
        try:
            timestamp = time.time()
            
            # Create proof hash
            proof_data = {
                "data": data,
                "timestamp": timestamp,
                "proof_type": proof_type,
                "previous_hash": self._get_last_hash()
            }
            
            proof_hash = self._hash_data(proof_data)
            
            proof = {
                "proof_id": f"proof_{len(self.proof_chain) + 1}",
                "hash": proof_hash,
                "timestamp": timestamp,
                "proof_type": proof_type,
                "data": data,
                "previous_hash": proof_data["previous_hash"]
            }
            
            self.proof_chain.append(proof)
            return proof
            
        except Exception as e:
            logger.error(f"Error creating proof: {e}")
            return {"error": str(e)}
    
    def verify_proof(self, proof: Dict[str, Any]) -> Dict[str, Any]:
        """Verify a proof's integrity."""
        try:
            # Recreate proof hash
            proof_data = {
                "data": proof["data"],
                "timestamp": proof["timestamp"],
                "proof_type": proof["proof_type"],
                "previous_hash": proof["previous_hash"]
            }
            
            expected_hash = self._hash_data(proof_data)
            is_valid = expected_hash == proof["hash"]
            
            verification_result = {
                "proof_id": proof["proof_id"],
                "is_valid": is_valid,
                "expected_hash": expected_hash,
                "actual_hash": proof["hash"],
                "verified_at": time.time()
            }
            
            self.verification_history.append(verification_result)
            return verification_result
            
        except Exception as e:
            logger.error(f"Error verifying proof: {e}")
            return {"error": str(e)}
    
    def _hash_data(self, data: Dict[str, Any]) -> str:
        """Create SHA-256 hash of data."""
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def _get_last_hash(self) -> str:
        """Get the hash of the last proof in the chain."""
        if not self.proof_chain:
            return "0000000000000000000000000000000000000000000000000000000000000000"
        return self.proof_chain[-1]["hash"]
    
    def get_proof_chain(self) -> List[Dict[str, Any]]:
        """Get the entire proof chain."""
        return self.proof_chain.copy()
    
    def get_verification_history(self) -> List[Dict[str, Any]]:
        """Get verification history."""
        return self.verification_history.copy()
    
    def verify_chain_integrity(self) -> Dict[str, Any]:
        """Verify the integrity of the entire proof chain."""
        try:
            chain_valid = True
            invalid_proofs = []
            
            for i, proof in enumerate(self.proof_chain):
                verification = self.verify_proof(proof)
                if not verification.get("is_valid", False):
                    chain_valid = False
                    invalid_proofs.append(proof["proof_id"])
            
            return {
                "chain_valid": chain_valid,
                "total_proofs": len(self.proof_chain),
                "invalid_proofs": invalid_proofs
            }
        except Exception as e:
            logger.error(f"Error verifying chain integrity: {e}")
            return {"error": str(e)} 