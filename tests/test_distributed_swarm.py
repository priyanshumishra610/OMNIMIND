"""
Tests for DistributedSwarm — SentraAGI Phase 21: The Final Sovereign Trials
"""

import pytest
import time
from arena.distributed_swarm import DistributedSwarm, SwarmNode, ConsensusResult, NodeState


class TestDistributedSwarm:
    """Test cases for DistributedSwarm."""

    def test_instantiation(self):
        """Test DistributedSwarm instantiation."""
        swarm = DistributedSwarm("test_node")
        assert swarm.node_id == "test_node"
        assert len(swarm.nodes) == 1
        assert "test_node" in swarm.nodes
        assert swarm.nodes["test_node"].state == NodeState.ACTIVE
        assert swarm.running == False

    def test_instantiation_default_node_id(self):
        """Test DistributedSwarm instantiation with default node ID."""
        swarm = DistributedSwarm()
        assert swarm.node_id == "node_1"
        assert "node_1" in swarm.nodes

    def test_start_node(self):
        """Test starting a node."""
        swarm = DistributedSwarm("test_node")
        shards = ["shard_a", "shard_b"]
        
        swarm.start_node(shards)
        assert swarm.running == True
        assert swarm.local_shards == shards
        assert swarm.nodes["test_node"].shards == shards

    def test_start_node_no_shards(self):
        """Test starting a node without shards."""
        swarm = DistributedSwarm("test_node")
        swarm.start_node()
        assert swarm.running == True
        assert swarm.local_shards == []

    def test_stop_node(self):
        """Test stopping a node."""
        swarm = DistributedSwarm("test_node")
        swarm.start_node()
        swarm.stop_node()
        assert swarm.running == False

    def test_add_node(self):
        """Test adding a new node."""
        swarm = DistributedSwarm("node_1")
        swarm.add_node("node_2", ["shard_c", "shard_d"])
        
        assert "node_2" in swarm.nodes
        assert swarm.nodes["node_2"].shards == ["shard_c", "shard_d"]
        assert swarm.nodes["node_2"].state == NodeState.ACTIVE

    def test_add_node_no_shards(self):
        """Test adding a node without shards."""
        swarm = DistributedSwarm("node_1")
        swarm.add_node("node_2")
        
        assert "node_2" in swarm.nodes
        assert swarm.nodes["node_2"].shards == []

    def test_remove_node(self):
        """Test removing a node."""
        swarm = DistributedSwarm("node_1")
        swarm.add_node("node_2")
        
        assert "node_2" in swarm.nodes
        swarm.remove_node("node_2")
        assert "node_2" not in swarm.nodes

    def test_sync_state(self):
        """Test state synchronization."""
        swarm = DistributedSwarm("node_1")
        swarm.add_node("node_2")
        
        success = swarm.sync_state()
        assert success == True

    def test_sync_state_specific_node(self):
        """Test state synchronization with specific node."""
        swarm = DistributedSwarm("node_1")
        swarm.add_node("node_2")
        
        success = swarm.sync_state("node_2")
        assert success == True

    def test_sync_state_invalid_node(self):
        """Test state synchronization with invalid node."""
        swarm = DistributedSwarm("node_1")
        success = swarm.sync_state("invalid_node")
        assert success == False

    def test_resolve_conflict(self):
        """Test conflict resolution."""
        swarm = DistributedSwarm("node_1")
        swarm.add_node("node_2")
        swarm.add_node("node_3")
        
        conflict_data = {"type": "belief_conflict", "data": "A vs not A"}
        result = swarm.resolve_conflict(conflict_data)
        
        assert isinstance(result, ConsensusResult)
        assert result.success == True
        assert result.participating_nodes == 3
        assert result.total_nodes == 3
        assert result.conflicts_resolved == 1

    def test_resolve_conflict_insufficient_nodes(self):
        """Test conflict resolution with insufficient nodes."""
        swarm = DistributedSwarm("node_1")
        # Only one node, need at least 2 for consensus
        
        conflict_data = {"type": "belief_conflict", "data": "A vs not A"}
        result = swarm.resolve_conflict(conflict_data)
        
        assert isinstance(result, ConsensusResult)
        assert result.success == False

    def test_get_swarm_status(self):
        """Test getting swarm status."""
        swarm = DistributedSwarm("node_1")
        swarm.add_node("node_2")
        swarm.add_node("node_3")
        
        status = swarm.get_swarm_status()
        
        assert status["total_nodes"] == 3
        assert status["active_nodes"] == 3
        assert status["partitioned_nodes"] == 0
        assert status["inactive_nodes"] == 0
        assert status["consensus_history"] == 0
        assert "node_1" in status["node_states"]
        assert "node_2" in status["node_states"]
        assert "node_3" in status["node_states"]

    def test_swarm_node_structure(self):
        """Test SwarmNode structure."""
        node = SwarmNode(
            node_id="test_node",
            state=NodeState.ACTIVE,
            last_heartbeat=time.time(),
            shards=["shard_a", "shard_b"],
            network_partition=False
        )
        
        assert node.node_id == "test_node"
        assert node.state == NodeState.ACTIVE
        assert node.shards == ["shard_a", "shard_b"]
        assert node.network_partition == False

    def test_consensus_result_structure(self):
        """Test ConsensusResult structure."""
        result = ConsensusResult(
            success=True,
            majority_decision="decision_a",
            participating_nodes=3,
            total_nodes=3,
            conflicts_resolved=1
        )
        
        assert result.success == True
        assert result.majority_decision == "decision_a"
        assert result.participating_nodes == 3
        assert result.total_nodes == 3
        assert result.conflicts_resolved == 1

    def test_node_state_enum(self):
        """Test NodeState enum values."""
        assert NodeState.ACTIVE.value == "active"
        assert NodeState.INACTIVE.value == "inactive"
        assert NodeState.PARTITIONED.value == "partitioned"
        assert NodeState.RECOVERING.value == "recovering"

    def test_full_loop_proof(self):
        """Test complete distributed swarm workflow."""
        swarm = DistributedSwarm("node_1")
        
        # Add nodes
        swarm.add_node("node_2", ["shard_a", "shard_b"])
        swarm.add_node("node_3", ["shard_c", "shard_d"])
        
        # Start node
        swarm.start_node(["shard_e", "shard_f"])
        
        # Sync state
        sync_success = swarm.sync_state()
        assert sync_success == True
        
        # Resolve conflicts
        conflicts = [
            {"type": "belief_conflict", "data": "A vs not A"},
            {"type": "decision_conflict", "data": "Strategy A vs Strategy B"}
        ]
        
        results = []
        for conflict in conflicts:
            result = swarm.resolve_conflict(conflict)
            results.append(result)
        
        # Verify results
        assert len(results) == 2
        for result in results:
            assert isinstance(result, ConsensusResult)
            assert result.success == True
        
        # Get status
        status = swarm.get_swarm_status()
        assert status["total_nodes"] == 3
        assert status["active_nodes"] == 3
        assert status["consensus_history"] == 2
        
        # Stop node
        swarm.stop_node()
        assert swarm.running == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 