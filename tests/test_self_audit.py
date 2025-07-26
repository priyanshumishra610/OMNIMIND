"""
Tests for SelfAudit — SentraAGI Phase 21: The Final Sovereign Trials
"""

import pytest
import time
from omega.self_audit import SelfAudit, IntegrityReport


class TestSelfAudit:
    """Test cases for SelfAudit."""

    def test_instantiation(self):
        """Test SelfAudit instantiation."""
        audit = SelfAudit()
        assert audit.audit_interval == 300
        assert audit.last_audit == 0

    def test_instantiation_custom_interval(self):
        """Test SelfAudit instantiation with custom interval."""
        audit = SelfAudit(audit_interval=60)
        assert audit.audit_interval == 60

    def test_run_audit(self):
        """Test running an audit."""
        audit = SelfAudit()
        report = audit.run_audit()
        
        assert isinstance(report, IntegrityReport)
        assert report.timestamp > 0
        assert isinstance(report.contradictions, list)
        assert isinstance(report.broken_loops, list)
        assert isinstance(report.state_drifts, list)
        assert isinstance(report.overall_integrity, bool)
        assert isinstance(report.recommendations, list)

    def test_audit_integrity_passing(self):
        """Test audit when integrity passes."""
        audit = SelfAudit()
        report = audit.run_audit()
        
        # With no actual contradictions, integrity should pass
        assert report.overall_integrity == True
        assert len(report.contradictions) == 0
        assert len(report.broken_loops) == 0
        assert len(report.state_drifts) == 0

    def test_audit_timestamp(self):
        """Test that audit timestamp is recent."""
        audit = SelfAudit()
        before_time = time.time()
        report = audit.run_audit()
        after_time = time.time()
        
        assert before_time <= report.timestamp <= after_time

    def test_daemon_control(self):
        """Test daemon start/stop methods."""
        audit = SelfAudit()
        
        # These methods should not raise exceptions
        audit.start_daemon()
        audit.stop_daemon()

    def test_check_contradictions(self):
        """Test contradiction checking method."""
        audit = SelfAudit()
        contradictions = audit._check_contradictions()
        
        assert isinstance(contradictions, list)

    def test_check_broken_loops(self):
        """Test broken loop checking method."""
        audit = SelfAudit()
        broken_loops = audit._check_broken_loops()
        
        assert isinstance(broken_loops, list)

    def test_check_state_drifts(self):
        """Test state drift checking method."""
        audit = SelfAudit()
        state_drifts = audit._check_state_drifts()
        
        assert isinstance(state_drifts, list)

    def test_full_loop_proof(self):
        """Test complete audit workflow."""
        audit = SelfAudit(audit_interval=1)
        
        # Run multiple audits
        reports = []
        for i in range(3):
            report = audit.run_audit()
            reports.append(report)
            time.sleep(0.1)  # Small delay between audits
        
        # Verify all reports are valid
        for report in reports:
            assert isinstance(report, IntegrityReport)
            assert report.timestamp > 0
            assert isinstance(report.overall_integrity, bool)
        
        # Verify timestamps are increasing
        for i in range(1, len(reports)):
            assert reports[i].timestamp > reports[i-1].timestamp


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 