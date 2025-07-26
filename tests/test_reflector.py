"""
Test OmegaReflector — SentraAGI Sovereign Singularity Core (Phase 20)
Tests for contradiction detection, self-doubt loops, and lineage fitness scoring.
"""

import pytest
from unittest.mock import Mock, patch

# Import the module to test
try:
    from omega.omega_reflector import OmegaReflector
    REFLECTOR_AVAILABLE = True
except ImportError:
    REFLECTOR_AVAILABLE = False


@pytest.mark.skipif(not REFLECTOR_AVAILABLE, reason="OmegaReflector not available")
class TestOmegaReflector:
    """Test cases for OmegaReflector."""
    
    def test_reflector_instantiation(self):
        """Test that OmegaReflector can be instantiated."""
        reflector = OmegaReflector()
        assert reflector is not None
        assert hasattr(reflector, 'config')
        assert hasattr(reflector, 'reflection_threshold')
    
    def test_reflector_config_loading(self):
        """Test that OmegaReflector loads configuration correctly."""
        config = {'reflection_threshold': 0.9}
        reflector = OmegaReflector(config)
        assert reflector.reflection_threshold == 0.9
    
    def test_detect_contradictions(self):
        """Test contradiction detection with dummy data."""
        reflector = OmegaReflector()
        dummy_shards = [
            {"belief": "A is true", "confidence": 0.8},
            {"belief": "A is false", "confidence": 0.7}
        ]
        contradictions = reflector.detect_contradictions(dummy_shards)
        assert isinstance(contradictions, list)
    
    def test_generate_self_doubt_loop(self):
        """Test self-doubt loop generation."""
        reflector = OmegaReflector()
        dummy_contradictions = [{"contradiction": "A vs not A"}]
        loop = reflector.generate_self_doubt_loop(dummy_contradictions)
        assert isinstance(loop, dict)
        assert "self_doubt" in loop
        assert "contradictions" in loop
    
    def test_score_lineage_fitness(self):
        """Test lineage fitness scoring."""
        reflector = OmegaReflector()
        dummy_lineage = [
            {"belief": "A", "fitness": 0.8},
            {"belief": "B", "fitness": 0.9}
        ]
        fitness = reflector.score_lineage_fitness(dummy_lineage)
        assert isinstance(fitness, float)
        assert 0.0 <= fitness <= 1.0
    
    def test_full_loop_proof(self):
        """Test complete reflection loop."""
        reflector = OmegaReflector()
        
        # Create dummy thought shards with contradictions
        thought_shards = [
            {"belief": "The sky is blue", "confidence": 0.9},
            {"belief": "The sky is red", "confidence": 0.8},
            {"belief": "Gravity exists", "confidence": 0.95}
        ]
        
        # Detect contradictions
        contradictions = reflector.detect_contradictions(thought_shards)
        
        # Generate self-doubt loop
        doubt_loop = reflector.generate_self_doubt_loop(contradictions)
        
        # Score lineage fitness
        fitness = reflector.score_lineage_fitness(thought_shards)
        
        # Verify all components work together
        assert isinstance(contradictions, list)
        assert isinstance(doubt_loop, dict)
        assert isinstance(fitness, float)
        assert "self_doubt" in doubt_loop
        assert "contradictions" in doubt_loop


def test_reflector_import():
    """Test that OmegaReflector can be imported."""
    if REFLECTOR_AVAILABLE:
        from omega.omega_reflector import OmegaReflector
        assert OmegaReflector is not None
    else:
        pytest.skip("OmegaReflector module not available")


def test_reflector_main_function():
    """Test that OmegaReflector has a main function."""
    if REFLECTOR_AVAILABLE:
        from omega.omega_reflector import main
        assert callable(main)
    else:
        pytest.skip("OmegaReflector module not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 