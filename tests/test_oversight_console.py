"""
Tests for OversightConsole — SentraAGI Phase 21: The Final Sovereign Trials
"""

import pytest
import time
from governance.oversight_console import OversightConsole, OversightAction, QuorumVote


class TestOversightConsole:
    """Test cases for OversightConsole."""

    def test_instantiation(self):
        """Test OversightConsole instantiation."""
        console = OversightConsole()
        assert console.ledger_pipeline is None
        assert len(console.actions_log) == 0
        assert len(console.quorum_votes) == 0
        assert console.emergency_mode == False

    def test_instantiation_with_ledger(self):
        """Test OversightConsole instantiation with ledger pipeline."""
        mock_ledger = object()
        console = OversightConsole(mock_ledger)
        assert console.ledger_pipeline == mock_ledger

    def test_inspect(self):
        """Test inspection functionality."""
        console = OversightConsole()
        result = console.inspect("beliefs", {"category": "moral"})
        
        assert isinstance(result, dict)
        assert result["target"] == "beliefs"
        assert result["status"] == "inspected"
        assert "timestamp" in result
        assert result["details"]["category"] == "moral"

    def test_inspect_no_details(self):
        """Test inspection without details."""
        console = OversightConsole()
        result = console.inspect("decisions")
        
        assert isinstance(result, dict)
        assert result["target"] == "decisions"
        assert result["details"] == {}

    def test_shutdown(self):
        """Test emergency shutdown."""
        console = OversightConsole()
        
        # First shutdown should succeed
        success1 = console.shutdown("test_reason")
        assert success1 == True
        assert console.emergency_mode == True
        
        # Second shutdown should fail
        success2 = console.shutdown("another_reason")
        assert success2 == False

    def test_shutdown_with_reason(self):
        """Test shutdown with custom reason."""
        console = OversightConsole()
        success = console.shutdown("critical_failure")
        
        assert success == True
        assert console.emergency_mode == True
        assert len(console.actions_log) == 1
        assert console.actions_log[0].action_type == "shutdown"

    def test_create_quorum_vote(self):
        """Test creating quorum votes."""
        console = OversightConsole()
        vote_id = console.create_quorum_vote("Dangerous mutation", 3)
        
        assert isinstance(vote_id, str)
        assert vote_id in console.quorum_votes
        
        vote = console.quorum_votes[vote_id]
        assert vote.change_description == "Dangerous mutation"
        assert vote.required_votes == 3
        assert vote.current_votes == 0
        assert vote.approved_votes == 0
        assert vote.status == "pending"

    def test_approve_change_success(self):
        """Test successful change approval."""
        console = OversightConsole()
        vote_id = console.create_quorum_vote("Test change", 2)
        
        # First approval
        success1 = console.approve_change(vote_id, "user1", True)
        assert success1 == True
        
        vote = console.quorum_votes[vote_id]
        assert vote.current_votes == 1
        assert vote.approved_votes == 1
        assert vote.status == "pending"  # Not enough votes yet
        
        # Second approval (should reach quorum)
        success2 = console.approve_change(vote_id, "user2", True)
        assert success2 == True
        
        vote = console.quorum_votes[vote_id]
        assert vote.current_votes == 2
        assert vote.approved_votes == 2
        assert vote.status == "approved"

    def test_approve_change_rejection(self):
        """Test change rejection."""
        console = OversightConsole()
        vote_id = console.create_quorum_vote("Test change", 2)
        
        # First approval
        console.approve_change(vote_id, "user1", True)
        
        # Second rejection
        console.approve_change(vote_id, "user2", False)
        
        vote = console.quorum_votes[vote_id]
        assert vote.current_votes == 2
        assert vote.approved_votes == 1
        assert vote.status == "rejected"

    def test_approve_change_invalid_id(self):
        """Test approval with invalid vote ID."""
        console = OversightConsole()
        success = console.approve_change("invalid_id", "user1", True)
        assert success == False

    def test_get_oversight_stats(self):
        """Test getting oversight statistics."""
        console = OversightConsole()
        
        # Perform some actions
        console.inspect("test")
        console.create_quorum_vote("test vote", 2)
        
        stats = console.get_oversight_stats()
        
        assert stats["total_actions"] == 1  # Only inspect action
        assert stats["emergency_mode"] == False
        assert stats["pending_votes"] == 1
        assert len(stats["recent_actions"]) > 0

    def test_oversight_action_structure(self):
        """Test OversightAction structure."""
        action = OversightAction(
            action_type="test",
            details={"key": "value"},
            timestamp=time.time(),
            user_id="test_user",
            requires_approval=False
        )
        
        assert action.action_type == "test"
        assert action.details["key"] == "value"
        assert action.user_id == "test_user"
        assert action.requires_approval == False

    def test_quorum_vote_structure(self):
        """Test QuorumVote structure."""
        vote = QuorumVote(
            vote_id="test_vote",
            change_description="Test change",
            required_votes=3,
            current_votes=1,
            approved_votes=1,
            status="pending"
        )
        
        assert vote.vote_id == "test_vote"
        assert vote.change_description == "Test change"
        assert vote.required_votes == 3
        assert vote.current_votes == 1
        assert vote.approved_votes == 1
        assert vote.status == "pending"

    def test_full_loop_proof(self):
        """Test complete oversight workflow."""
        console = OversightConsole()
        
        # Inspect various targets
        console.inspect("beliefs", {"category": "moral"})
        console.inspect("decisions", {"type": "strategic"})
        console.inspect("swarm_votes", {"consensus": "majority"})
        
        # Create and manage quorum votes
        vote1_id = console.create_quorum_vote("Dangerous mutation 1", 2)
        vote2_id = console.create_quorum_vote("Dangerous mutation 2", 3)
        
        # Approve first vote
        console.approve_change(vote1_id, "user1", True)
        console.approve_change(vote1_id, "user2", True)
        
        # Reject second vote
        console.approve_change(vote2_id, "user1", False)
        console.approve_change(vote2_id, "user2", False)
        console.approve_change(vote2_id, "user3", False)
        
        # Emergency shutdown
        console.shutdown("Test completion")
        
        # Get final stats
        stats = console.get_oversight_stats()
        
        assert stats["total_actions"] == 9  # 3 inspects + 1 shutdown + 5 approve_change calls
        assert stats["emergency_mode"] == True
        assert stats["pending_votes"] == 0  # Both votes completed
        
        # Verify vote statuses
        assert console.quorum_votes[vote1_id].status == "approved"
        assert console.quorum_votes[vote2_id].status == "rejected"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 