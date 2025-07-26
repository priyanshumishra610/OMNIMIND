"""
Immutable Ledger — SentraAGI Phase 21: The Final Sovereign Trials
Append-only, verifiable ledger for all critical state changes in the Kernel.
"""

import hashlib
import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ImmutableLedger:
    """
    Append-only, verifiable ledger using a chain of hashes (Merkle/Mini-Blockchain).
    Records every critical state change for audit and proof.
    """
    def __init__(self, ledger_path: str = "data/immutable_ledger.json"):
        self.ledger_path = ledger_path
        self.entries: List[Dict[str, Any]] = []
        self._load_ledger()
        logger.info(f"ImmutableLedger initialized at {self.ledger_path}")

    def _load_ledger(self):
        try:
            with open(self.ledger_path, 'r') as f:
                self.entries = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.entries = []

    def _save_ledger(self):
        with open(self.ledger_path, 'w') as f:
            json.dump(self.entries, f, indent=2)

    def _hash_entry(self, entry: Dict[str, Any], prev_hash: str) -> str:
        entry_str = json.dumps(entry, sort_keys=True) + prev_hash
        return hashlib.sha256(entry_str.encode()).hexdigest()

    def append_entry(self, data: Dict[str, Any]) -> str:
        """
        Append a new entry to the ledger. Returns the new hash.
        TODO: Integrate with Merkle tree/blockchain for distributed verification.
        """
        prev_hash = self.entries[-1]['hash'] if self.entries else '0'*64
        entry = {
            "data": data,
            "prev_hash": prev_hash
        }
        entry['hash'] = self._hash_entry(entry, prev_hash)
        self.entries.append(entry)
        self._save_ledger()
        logger.info(f"Appended entry to ledger: {entry['hash']}")
        return entry['hash']

    def verify_integrity(self) -> bool:
        """
        Verify the integrity of the entire ledger chain.
        Returns True if all hashes are valid.
        """
        prev_hash = '0'*64
        for entry in self.entries:
            expected_hash = self._hash_entry({"data": entry['data'], "prev_hash": prev_hash}, prev_hash)
            if entry['hash'] != expected_hash:
                logger.error(f"Ledger integrity check failed at entry: {entry}")
                return False
            prev_hash = entry['hash']
        logger.info("Ledger integrity verified.")
        return True

    # TODO: Add Merkle tree support for distributed verification
    # TODO: Add digital signature support for entries


def main():
    """Example usage of ImmutableLedger."""
    ledger = ImmutableLedger()
    entry_hash = ledger.append_entry({"event": "swarm_vote", "result": "approved", "timestamp": 1234567890})
    print(f"Appended entry hash: {entry_hash}")
    print(f"Ledger integrity: {ledger.verify_integrity()}")


if __name__ == "__main__":
    main() 