"""
Full Integration Tests for Phase 21 — SentraAGI The Final Sovereign Trials
Test complete workflow: Immutable Ledger → NeuroForge → Omega → Oversight → Distributed Swarm → Rollback → Immutable Proof
"""

import pytest
import tempfile
import os
import time
from immutable.ledger import ImmutableLedger
from pipelines.ledger_pipeline import LedgerPipeline
from omega.self_audit import SelfAudit
from memory.forgetter import Forgetter, ForgettingReceipt
from governance.oversight_console import OversightConsole
from pipelines.oversight_pipeline import OversightPipeline
from arena.distributed_swarm import DistributedSwarm
from proof.proof_of_continuity import ProofOfContinuity


class TestFinalTrialsIntegration:
    """Integration tests for Phase 21 Final Sovereign Trials."""

    def test_immutable_ledger_integration(self):
        """Test ImmutableLedger integration with all components."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "integration_ledger.json")
            ledger = ImmutableLedger(ledger_path)
            
            # Test ledger operations
            entry1 = ledger.append_entry({"event": "integration_test", "component": "ledger"})
            entry2 = ledger.append_entry({"event": "integration_test", "component": "pipeline"})
            
            assert ledger.verify_integrity() == True
            assert len(ledger.entries) == 2

    def test_ledger_pipeline_integration(self):
        """Test LedgerPipeline integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "pipeline_ledger.json")
            pipeline = LedgerPipeline(ledger_path)
            
            # Test logging state changes
            hash1 = pipeline.log_state_change("TestModule", {"event": "test1"})
            hash2 = pipeline.log_state_change("TestModule", {"event": "test2"})
            
            assert pipeline.verify_ledger() == True
            assert hash1 != hash2

    def test_self_audit_integration(self):
        """Test SelfAudit integration."""
        audit = SelfAudit(audit_interval=1)
        
        # Run multiple audits
        reports = []
        for i in range(3):
            report = audit.run_audit()
            reports.append(report)
            time.sleep(0.1)
        
        # Verify all reports are valid
        for report in reports:
            assert isinstance(report.overall_integrity, bool)
            assert report.timestamp > 0

    def test_forgetter_integration(self):
        """Test Forgetter integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "forgetter_ledger.json")
            ledger_pipeline = LedgerPipeline(ledger_path)
            forgetter = Forgetter(ledger_pipeline=ledger_pipeline)
            
            # Test forgetting operations
            receipt = forgetter.forget_stale_data(threshold=0.5)
            assert isinstance(receipt, ForgettingReceipt)
            
            stats = forgetter.get_forgetting_stats()
            assert isinstance(stats, dict)

    def test_oversight_console_integration(self):
        """Test OversightConsole integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "oversight_ledger.json")
            ledger_pipeline = LedgerPipeline(ledger_path)
            console = OversightConsole(ledger_pipeline)
            
            # Test inspection
            result = console.inspect("test_target", {"category": "test"})
            assert result["target"] == "test_target"
            
            # Test quorum vote
            vote_id = console.create_quorum_vote("Test change", 2)
            console.approve_change(vote_id, "user1", True)
            console.approve_change(vote_id, "user2", True)
            
            vote = console.quorum_votes[vote_id]
            assert vote.status == "approved"

    def test_oversight_pipeline_integration(self):
        """Test OversightPipeline integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "oversight_pipeline_ledger.json")
            ledger_pipeline = LedgerPipeline(ledger_path)
            pipeline = OversightPipeline(ledger_pipeline)
            
            # Register dummy hooks
            def dummy_hook():
                return {"status": "healthy", "timestamp": time.time()}
            
            pipeline.register_kernel_hook("test_hook", dummy_hook)
            
            # Test monitoring
            state = pipeline.monitor_kernel_state()
            assert "test_hook" in state
            
            # Test dashboard
            dashboard = pipeline.get_oversight_dashboard()
            assert "console_stats" in dashboard
            assert "kernel_state" in dashboard

    def test_distributed_swarm_integration(self):
        """Test DistributedSwarm integration."""
        swarm = DistributedSwarm("node_1")
        
        # Add nodes
        swarm.add_node("node_2", ["shard_a", "shard_b"])
        swarm.add_node("node_3", ["shard_c", "shard_d"])
        
        # Start node
        swarm.start_node(["shard_e", "shard_f"])
        
        # Test consensus
        conflict_data = {"type": "integration_test", "data": "A vs B"}
        result = swarm.resolve_conflict(conflict_data)
        
        assert result.success == True
        assert result.participating_nodes == 3
        
        # Get status
        status = swarm.get_swarm_status()
        assert status["total_nodes"] == 3
        assert status["active_nodes"] == 3
        
        # Stop node
        swarm.stop_node()

    def test_proof_of_continuity_integration(self):
        """Test ProofOfContinuity integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proof_path = os.path.join(tmpdir, "integration_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            # Add mutations representing integration test
            proof_gen.add_mutation("Phase 21", "integration", "Immutable Ledger test")
            proof_gen.add_mutation("Phase 21", "integration", "Self Audit test")
            proof_gen.add_mutation("Phase 21", "integration", "Forgetter test")
            proof_gen.add_mutation("Phase 21", "integration", "Oversight test")
            proof_gen.add_mutation("Phase 21", "integration", "Distributed Swarm test")
            
            # Generate and export proof
            proof = proof_gen.generate_proof()
            assert proof.total_mutations == 5
            assert proof.chain_integrity == True
            
            # Export to both formats
            json_path = proof_gen.export_proof("json")
            md_path = proof_gen.export_proof("markdown")
            
            assert os.path.exists(json_path)
            assert os.path.exists(md_path)

    def test_full_sovereign_loop(self):
        """Test complete sovereign loop: Ledger → NeuroForge → Omega → Oversight → Swarm → Rollback → Proof."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Initialize all components
            ledger_path = os.path.join(tmpdir, "sovereign_ledger.json")
            ledger_pipeline = LedgerPipeline(ledger_path)
            
            proof_path = os.path.join(tmpdir, "sovereign_proof.json")
            proof_gen = ProofOfContinuity(proof_path)
            
            # 1. Immutable Ledger
            ledger_hash1 = ledger_pipeline.log_state_change("SovereignLoop", {"step": "ledger_init"})
            
            # 2. Self Audit
            audit = SelfAudit()
            audit_report = audit.run_audit()
            ledger_hash2 = ledger_pipeline.log_state_change("SelfAudit", {
                "integrity": audit_report.overall_integrity,
                "contradictions": len(audit_report.contradictions)
            })
            
            # 3. Memory Pruning
            forgetter = Forgetter(ledger_pipeline=ledger_pipeline)
            forget_receipt = forgetter.forget_stale_data()
            ledger_hash3 = ledger_pipeline.log_state_change("Forgetter", {
                "forgotten_shards": len(forget_receipt.shard_ids)
            })
            
            # 4. Oversight Console
            console = OversightConsole(ledger_pipeline)
            inspection = console.inspect("sovereign_state", {"phase": "21"})
            vote_id = console.create_quorum_vote("Sovereign mutation", 2)
            console.approve_change(vote_id, "user1", True)
            console.approve_change(vote_id, "user2", True)
            ledger_hash4 = ledger_pipeline.log_state_change("Oversight", {
                "inspection_target": inspection["target"],
                "vote_status": console.quorum_votes[vote_id].status
            })
            
            # 5. Distributed Swarm
            swarm = DistributedSwarm("sovereign_node")
            swarm.add_node("node_2", ["shard_sovereign"])
            swarm.start_node(["shard_main"])
            conflict_result = swarm.resolve_conflict({"type": "sovereign_test"})
            ledger_hash5 = ledger_pipeline.log_state_change("DistributedSwarm", {
                "consensus_success": conflict_result.success,
                "participating_nodes": conflict_result.participating_nodes
            })
            
            # 6. Emergency Rollback (simulate)
            console.shutdown("Integration test completion")
            ledger_hash6 = ledger_pipeline.log_state_change("EmergencyRollback", {
                "reason": "integration_test",
                "emergency_mode": console.emergency_mode
            })
            
            # 7. Immutable Proof
            proof_gen.add_mutation("Phase 21", "sovereign_loop", "Complete sovereign loop test", {
                "ledger_hashes": [ledger_hash1, ledger_hash2, ledger_hash3, ledger_hash4, ledger_hash5, ledger_hash6],
                "audit_integrity": audit_report.overall_integrity,
                "forgotten_shards": len(forget_receipt.shard_ids),
                "consensus_success": conflict_result.success,
                "emergency_triggered": console.emergency_mode
            })
            
            # Verify final state
            final_proof = proof_gen.generate_proof()
            assert final_proof.chain_integrity == True
            assert final_proof.total_mutations >= 1
            
            # Verify ledger integrity
            assert ledger_pipeline.verify_ledger() == True
            
            # Export final proof
            final_json = proof_gen.export_proof("json")
            final_md = proof_gen.export_proof("markdown")
            
            assert os.path.exists(final_json)
            assert os.path.exists(final_md)
            
            # Cleanup
            swarm.stop_node()

    def test_error_handling_and_recovery(self):
        """Test error handling and recovery mechanisms."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "error_ledger.json")
            ledger_pipeline = LedgerPipeline(ledger_path)
            
            # Test ledger with invalid data
            try:
                ledger_pipeline.log_state_change("ErrorTest", {"invalid": "data"})
                assert True  # Should not raise exception
            except Exception as e:
                pytest.fail(f"Ledger should handle invalid data gracefully: {e}")
            
            # Test audit with errors
            audit = SelfAudit()
            try:
                report = audit.run_audit()
                assert isinstance(report.overall_integrity, bool)
            except Exception as e:
                pytest.fail(f"Audit should handle errors gracefully: {e}")
            
            # Test swarm with network issues
            swarm = DistributedSwarm("error_node")
            try:
                swarm.sync_state("nonexistent_node")
                assert True  # Should handle gracefully
            except Exception as e:
                pytest.fail(f"Swarm should handle network errors gracefully: {e}")

    def test_performance_and_scalability(self):
        """Test performance and scalability of integrated components."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = os.path.join(tmpdir, "perf_ledger.json")
            ledger_pipeline = LedgerPipeline(ledger_path)
            
            # Test multiple rapid operations
            start_time = time.time()
            
            for i in range(100):
                ledger_pipeline.log_state_change("PerfTest", {"iteration": i})
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Should complete 100 operations in reasonable time
            assert duration < 10.0  # Less than 10 seconds
            
            # Verify ledger integrity after rapid operations
            assert ledger_pipeline.verify_ledger() == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 