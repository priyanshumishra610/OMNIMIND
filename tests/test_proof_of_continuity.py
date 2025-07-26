"""
Tests for ProofOfContinuity — SentraAGI Phase 21: The Final Sovereign Trials
"""

import pytest
import tempfile
import os
import time
from proof.proof_of_continuity import ProofOfContinuity, ProofEntry, ContinuityProof


class TestProofOfContinuity:
    """Test cases for ProofOfContinuity."""

    def test_instantiation(self):
        """Test ProofOfContinuity instantiation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            assert proof_gen.proof_path == proof_path
            assert len(proof_gen.entries) == 0
            assert proof_gen.genesis_hash == "0" * 64

    def test_add_mutation(self):
        """Test adding mutations to the proof chain."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            # Add first mutation
            proof_gen.add_mutation("Phase 1", "initialization", "Test mutation 1", {"key": "value1"})
            assert len(proof_gen.entries) == 1
            assert proof_gen.entries[0].phase == "Phase 1"
            assert proof_gen.entries[0].mutation_type == "initialization"
            assert proof_gen.entries[0].description == "Test mutation 1"
            assert proof_gen.entries[0].metadata["key"] == "value1"
            assert proof_gen.entries[0].parent_hash == "0" * 64
            
            # Add second mutation
            proof_gen.add_mutation("Phase 2", "evolution", "Test mutation 2", {"key": "value2"})
            assert len(proof_gen.entries) == 2
            assert proof_gen.entries[1].phase == "Phase 2"
            assert proof_gen.entries[1].parent_hash == proof_gen.entries[0].mutation_hash

    def test_add_mutation_no_metadata(self):
        """Test adding mutation without metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            proof_gen.add_mutation("Phase 1", "test", "Test mutation")
            assert len(proof_gen.entries) == 1
            assert proof_gen.entries[0].metadata == {}

    def test_generate_proof_empty(self):
        """Test generating proof with no entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            proof = proof_gen.generate_proof()
            assert isinstance(proof, ContinuityProof)
            assert proof.genesis_hash == "0" * 64
            assert proof.final_hash == "0" * 64
            assert proof.total_phases == 0
            assert proof.total_mutations == 0
            assert proof.total_rollbacks == 0
            assert proof.chain_integrity == True
            assert len(proof.entries) == 0

    def test_generate_proof_with_entries(self):
        """Test generating proof with entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            # Add mutations
            proof_gen.add_mutation("Phase 1", "initialization", "Test 1")
            proof_gen.add_mutation("Phase 2", "evolution", "Test 2")
            proof_gen.add_mutation("Phase 3", "rollback", "Test 3")
            
            proof = proof_gen.generate_proof()
            assert isinstance(proof, ContinuityProof)
            assert proof.total_phases == 3
            assert proof.total_mutations == 2  # initialization + evolution
            assert proof.total_rollbacks == 1  # rollback
            assert proof.chain_integrity == True
            assert len(proof.entries) == 3

    def test_export_proof_json(self):
        """Test exporting proof to JSON format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            # Add mutation
            proof_gen.add_mutation("Phase 1", "test", "Test mutation")
            
            # Export to JSON
            output_path = proof_gen.export_proof("json")
            assert os.path.exists(output_path)
            
            # Verify file content
            import json
            with open(output_path, 'r') as f:
                data = json.load(f)
                assert "genesis_hash" in data
                assert "final_hash" in data
                assert "total_phases" in data
                assert "entries" in data

    def test_export_proof_markdown(self):
        """Test exporting proof to Markdown format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            # Add mutation
            proof_gen.add_mutation("Phase 1", "test", "Test mutation")
            
            # Export to Markdown
            output_path = proof_gen.export_proof("markdown")
            assert os.path.exists(output_path)
            
            # Verify file content
            with open(output_path, 'r') as f:
                content = f.read()
                assert "SentraAGI Proof of Continuity" in content
                assert "Phase 1" in content
                assert "test" in content

    def test_export_proof_invalid_format(self):
        """Test exporting proof with invalid format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            with pytest.raises(ValueError):
                proof_gen.export_proof("invalid_format")

    def test_get_proof_summary(self):
        """Test getting proof summary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            # Add mutations
            proof_gen.add_mutation("Phase 1", "test1", "Test 1")
            proof_gen.add_mutation("Phase 2", "test2", "Test 2")
            
            summary = proof_gen.get_proof_summary()
            assert summary["total_entries"] == 2
            assert summary["total_phases"] == 2
            assert summary["total_mutations"] == 2
            assert summary["total_rollbacks"] == 0
            assert summary["chain_integrity"] == True
            assert "genesis_hash" in summary
            assert "final_hash" in summary

    def test_proof_entry_structure(self):
        """Test ProofEntry structure."""
        entry = ProofEntry(
            phase="Phase 1",
            timestamp=time.time(),
            mutation_type="test",
            mutation_hash="hash123",
            parent_hash="hash456",
            description="Test entry",
            metadata={"key": "value"}
        )
        
        assert entry.phase == "Phase 1"
        assert entry.mutation_type == "test"
        assert entry.mutation_hash == "hash123"
        assert entry.parent_hash == "hash456"
        assert entry.description == "Test entry"
        assert entry.metadata["key"] == "value"

    def test_continuity_proof_structure(self):
        """Test ContinuityProof structure."""
        proof = ContinuityProof(
            genesis_hash="genesis123",
            final_hash="final123",
            total_phases=3,
            total_mutations=2,
            total_rollbacks=1,
            chain_integrity=True,
            entries=[],
            generated_at=time.time()
        )
        
        assert proof.genesis_hash == "genesis123"
        assert proof.final_hash == "final123"
        assert proof.total_phases == 3
        assert proof.total_mutations == 2
        assert proof.total_rollbacks == 1
        assert proof.chain_integrity == True
        assert len(proof.entries) == 0

    def test_full_loop_proof(self):
        """Test complete proof of continuity workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "test_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            # Add mutations representing a complete journey
            mutations = [
                ("Phase 1", "initialization", "SentraAGI genesis", {"version": "1.0"}),
                ("Phase 19", "perception", "Synthetic perception expansion", {"modules": ["VirtualSenses"]}),
                ("Phase 20", "sovereignty", "Sovereign singularity core", {"components": ["OmegaReflector"]}),
                ("Phase 21", "immutability", "Final sovereign trials", {"ledger": "ImmutableLedger"}),
                ("Phase 21", "rollback", "Emergency rollback", {"reason": "contradiction_detected"})
            ]
            
            for phase, mutation_type, description, metadata in mutations:
                proof_gen.add_mutation(phase, mutation_type, description, metadata)
            
            # Generate proof
            proof = proof_gen.generate_proof()
            assert proof.total_phases == 3  # Phase 1, 19, 20, 21 (unique phases)
            assert proof.total_mutations == 4  # All except rollback
            assert proof.total_rollbacks == 1  # Only rollback
            assert proof.chain_integrity == True
            
            # Export to both formats
            json_path = proof_gen.export_proof("json")
            md_path = proof_gen.export_proof("markdown")
            
            assert os.path.exists(json_path)
            assert os.path.exists(md_path)
            
            # Get summary
            summary = proof_gen.get_proof_summary()
            assert summary["total_entries"] == 5
            assert summary["chain_integrity"] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 