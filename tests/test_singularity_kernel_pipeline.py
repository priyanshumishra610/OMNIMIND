"""
Test Singularity Kernel Pipeline — SentraAGI Sovereign Singularity Core (Phase 20)
Tests for the complete sovereign loop pipeline.
"""

import pytest
from unittest.mock import Mock, patch

# Import the module to test
try:
    from pipelines.singularity_kernel_pipeline import (
        SingularityKernelPipeline,
        run_singularity_pipeline_standalone
    )
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False


@pytest.mark.skipif(not PIPELINE_AVAILABLE, reason="Singularity Kernel Pipeline not available")
class TestSingularityKernelPipeline:
    """Test cases for Singularity Kernel Pipeline."""
    
    def test_pipeline_instantiation(self):
        """Test that Singularity Kernel Pipeline can be instantiated."""
        pipeline = SingularityKernelPipeline()
        assert pipeline is not None
        assert hasattr(pipeline, 'config')
    
    def test_pipeline_config_loading(self):
        """Test that pipeline loads configuration correctly."""
        config = {
            'reflection_threshold': 0.9,
            'moral_horizon': 0.8,
            'swarm_size': 5
        }
        pipeline = SingularityKernelPipeline(config)
        assert pipeline.config == config
    
    def test_initialize_components(self):
        """Test component initialization."""
        pipeline = SingularityKernelPipeline()
        components = pipeline.initialize_components()
        
        assert 'neuroforge' in components
        assert 'omega_reflector' in components
        assert 'consequence_simulator' in components
        assert 'ontology_rewriter' in components
        assert 'reflex_swarm' in components
    
    def test_run_sovereign_loop(self):
        """Test running the sovereign loop."""
        pipeline = SingularityKernelPipeline()
        dummy_mutation = {"mutation": "test mutation"}
        result = pipeline.run_sovereign_loop(dummy_mutation)
        
        assert isinstance(result, dict)
        assert 'success' in result
        assert 'trace' in result
    
    def test_full_loop_proof(self):
        """Test complete pipeline loop."""
        pipeline = SingularityKernelPipeline()
        
        # Create dummy mutation
        mutation = {
            "mutation": "add belief",
            "belief": "consciousness is computational",
            "confidence": 0.85
        }
        
        # Run complete sovereign loop
        result = pipeline.run_sovereign_loop(mutation)
        
        # Verify result structure
        assert isinstance(result, dict)
        assert 'success' in result
        assert 'trace' in result
        assert 'fitness_score' in result
        assert 'sandbox_proof' in result
        assert 'swarm_vote' in result


def test_pipeline_import():
    """Test that Singularity Kernel Pipeline can be imported."""
    if PIPELINE_AVAILABLE:
        from pipelines.singularity_kernel_pipeline import SingularityKernelPipeline
        assert SingularityKernelPipeline is not None
    else:
        pytest.skip("Singularity Kernel Pipeline module not available")


def test_pipeline_main_function():
    """Test that pipeline has a main function."""
    if PIPELINE_AVAILABLE:
        from pipelines.singularity_kernel_pipeline import main
        assert callable(main)
    else:
        pytest.skip("Singularity Kernel Pipeline module not available")


def test_standalone_pipeline():
    """Test standalone pipeline execution."""
    if PIPELINE_AVAILABLE:
        result = run_singularity_pipeline_standalone()
        assert isinstance(result, dict)
        assert 'pipeline_status' in result
    else:
        pytest.skip("Singularity Kernel Pipeline module not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 