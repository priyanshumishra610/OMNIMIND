"""
Test ReflexSwarm — SentraAGI Sovereign Singularity Core (Phase 20)
Tests for swarm debate, betrayal testing, and majority voting.
"""

import pytest
from unittest.mock import Mock, patch

# Import the module to test
try:
    from arena.reflex_swarm import ReflexSwarm
    SWARM_AVAILABLE = True
except ImportError:
    SWARM_AVAILABLE = False


@pytest.mark.skipif(not SWARM_AVAILABLE, reason="ReflexSwarm not available")
class TestReflexSwarm:
    """Test cases for ReflexSwarm."""
    
    def test_swarm_instantiation(self):
        """Test that ReflexSwarm can be instantiated."""
        swarm = ReflexSwarm()
        assert swarm is not None
        assert hasattr(swarm, 'config')
        assert hasattr(swarm, 'swarm_size')
    
    def test_swarm_config_loading(self):
        """Test that ReflexSwarm loads configuration correctly."""
        config = {'swarm_size': 5}
        swarm = ReflexSwarm(config)
        assert swarm.swarm_size == 5
    
    def test_debate_mutation(self):
        """Test mutation debate with dummy data."""
        swarm = ReflexSwarm()
        dummy_mutation = {"mutation": "add new axiom", "axiom": "A implies B"}
        debate_result = swarm.debate_mutation(dummy_mutation)
        assert isinstance(debate_result, dict)
        assert "debate_result" in debate_result
        assert "mutation" in debate_result
    
    def test_betrayal_test(self):
        """Test betrayal detection."""
        swarm = ReflexSwarm()
        dummy_mutation = {"mutation": "modify belief", "target": "gravity"}
        betrayal = swarm.betrayal_test(dummy_mutation)
        assert isinstance(betrayal, bool)
    
    def test_majority_vote(self):
        """Test majority voting."""
        swarm = ReflexSwarm()
        dummy_debate = {"debate_result": "undecided", "mutation": "test"}
        vote = swarm.majority_vote(dummy_debate)
        assert isinstance(vote, bool)
    
    def test_full_loop_proof(self):
        """Test complete swarm debate loop."""
        swarm = ReflexSwarm()
        
        # Create dummy mutation
        mutation = {
            "mutation": "add belief",
            "belief": "consciousness is emergent",
            "confidence": 0.8
        }
        
        # Debate mutation
        debate = swarm.debate_mutation(mutation)
        
        # Test for betrayal
        betrayal = swarm.betrayal_test(mutation)
        
        # Vote on debate result
        vote = swarm.majority_vote(debate)
        
        # Verify all components work together
        assert isinstance(debate, dict)
        assert isinstance(betrayal, bool)
        assert isinstance(vote, bool)
        assert "debate_result" in debate
        assert "mutation" in debate


def test_swarm_import():
    """Test that ReflexSwarm can be imported."""
    if SWARM_AVAILABLE:
        from arena.reflex_swarm import ReflexSwarm
        assert ReflexSwarm is not None
    else:
        pytest.skip("ReflexSwarm module not available")


def test_swarm_main_function():
    """Test that ReflexSwarm has a main function."""
    if SWARM_AVAILABLE:
        from arena.reflex_swarm import main
        assert callable(main)
    else:
        pytest.skip("ReflexSwarm module not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 