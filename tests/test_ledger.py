"""
Tests for ImmutableLedger — SentraAGI Phase 21: The Final Sovereign Trials
"""

import pytest
import tempfile
import os
from immutable.ledger import ImmutableLedger


class TestImmutableLedger:
    """Test cases for ImmutableLedger."""

    def test_instantiation(self):
        """Test ImmutableLedger instantiation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "test_ledger.json")
            ledger = ImmutableLedger(ledger_path)
            assert ledger.ledger_path == ledger_path
            assert len(ledger.entries) == 0

    def test_append_entry(self):
        """Test appending entries to the ledger."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "test_ledger.json")
            ledger = ImmutableLedger(ledger_path)
            
            # Append first entry
            data1 = {"event": "test1", "data": "value1"}
            hash1 = ledger.append_entry(data1)
            assert len(ledger.entries) == 1
            assert ledger.entries[0]["data"] == data1
            assert ledger.entries[0]["hash"] == hash1
            
            # Append second entry
            data2 = {"event": "test2", "data": "value2"}
            hash2 = ledger.append_entry(data2)
            assert len(ledger.entries) == 2
            assert ledger.entries[1]["data"] == data2
            assert ledger.entries[1]["hash"] == hash2
            assert ledger.entries[1]["prev_hash"] == hash1

    def test_verify_integrity(self):
        """Test ledger integrity verification."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "test_ledger.json")
            ledger = ImmutableLedger(ledger_path)
            
            # Empty ledger should be valid
            assert ledger.verify_integrity() == True
            
            # Add entries and verify
            ledger.append_entry({"event": "test1"})
            ledger.append_entry({"event": "test2"})
            ledger.append_entry({"event": "test3"})
            
            assert ledger.verify_integrity() == True

    def test_ledger_persistence(self):
        """Test that ledger persists across instantiations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "test_ledger.json")
            
            # Create ledger and add entries
            ledger1 = ImmutableLedger(ledger_path)
            ledger1.append_entry({"event": "persistence_test"})
            ledger1.append_entry({"event": "persistence_test2"})
            
            # Create new ledger instance
            ledger2 = ImmutableLedger(ledger_path)
            assert len(ledger2.entries) == 2
            assert ledger2.entries[0]["data"]["event"] == "persistence_test"
            assert ledger2.entries[1]["data"]["event"] == "persistence_test2"

    def test_full_loop_proof(self):
        """Test complete ledger workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "test_ledger.json")
            ledger = ImmutableLedger(ledger_path)
            
            # Simulate a complete workflow
            entries = [
                {"event": "swarm_vote", "result": "approved"},
                {"event": "mutation", "type": "belief_update"},
                {"event": "rollback", "reason": "contradiction_detected"},
                {"event": "audit", "status": "passed"}
            ]
            
            hashes = []
            for entry in entries:
                hash_val = ledger.append_entry(entry)
                hashes.append(hash_val)
            
            # Verify integrity
            assert ledger.verify_integrity() == True
            
            # Verify chain structure
            assert len(ledger.entries) == 4
            assert len(hashes) == 4
            
            # Verify each entry has correct prev_hash
            for i, entry in enumerate(ledger.entries):
                if i == 0:
                    assert entry["prev_hash"] == "0" * 64
                else:
                    assert entry["prev_hash"] == hashes[i-1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 