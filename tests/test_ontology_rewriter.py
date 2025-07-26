"""
Test OntologyRewriter — SentraAGI Sovereign Singularity Core (Phase 20)
Tests for patch generation, application, and rollback functionality.
"""

import pytest
from unittest.mock import Mock, patch

# Import the module to test
try:
    from genesis.ontology_rewriter import OntologyRewriter
    REWRITER_AVAILABLE = True
except ImportError:
    REWRITER_AVAILABLE = False


@pytest.mark.skipif(not REWRITER_AVAILABLE, reason="OntologyRewriter not available")
class TestOntologyRewriter:
    """Test cases for OntologyRewriter."""
    
    def test_rewriter_instantiation(self):
        """Test that OntologyRewriter can be instantiated."""
        rewriter = OntologyRewriter()
        assert rewriter is not None
        assert hasattr(rewriter, 'config')
        assert hasattr(rewriter, 'ontology_path')
        assert hasattr(rewriter, '_last_patch')
    
    def test_rewriter_config_loading(self):
        """Test that OntologyRewriter loads configuration correctly."""
        config = {'ontology_path': 'custom_belief_graph.json'}
        rewriter = OntologyRewriter(config)
        assert rewriter.ontology_path == 'custom_belief_graph.json'
    
    def test_generate_patch(self):
        """Test patch generation with dummy belief."""
        rewriter = OntologyRewriter()
        dummy_belief = {"belief": "sky is blue", "confidence": 0.9}
        patch = rewriter.generate_patch(dummy_belief)
        assert isinstance(patch, dict)
        assert "patch" in patch
    
    def test_apply_patch(self):
        """Test patch application."""
        rewriter = OntologyRewriter()
        dummy_patch = {"patch": {"belief": "test belief"}}
        result = rewriter.apply_patch(dummy_patch)
        assert isinstance(result, bool)
        assert rewriter._last_patch == dummy_patch
    
    def test_rollback_patch(self):
        """Test patch rollback."""
        rewriter = OntologyRewriter()
        
        # First apply a patch
        dummy_patch = {"patch": {"belief": "test belief"}}
        rewriter.apply_patch(dummy_patch)
        assert rewriter._last_patch is not None
        
        # Then rollback
        result = rewriter.rollback_patch()
        assert isinstance(result, bool)
        assert rewriter._last_patch is None
    
    def test_rollback_without_patch(self):
        """Test rollback when no patch has been applied."""
        rewriter = OntologyRewriter()
        result = rewriter.rollback_patch()
        assert isinstance(result, bool)
        assert result == False
    
    def test_full_loop_proof(self):
        """Test complete patch and rollback loop."""
        rewriter = OntologyRewriter()
        
        # Create dummy belief
        belief = {
            "belief": "gravity is constant",
            "confidence": 0.95,
            "source": "physics"
        }
        
        # Generate patch
        patch = rewriter.generate_patch(belief)
        
        # Apply patch
        applied = rewriter.apply_patch(patch)
        
        # Rollback patch
        rolled_back = rewriter.rollback_patch()
        
        # Verify all components work together
        assert isinstance(patch, dict)
        assert isinstance(applied, bool)
        assert isinstance(rolled_back, bool)
        assert "patch" in patch
        assert applied == True
        assert rolled_back == True


def test_rewriter_import():
    """Test that OntologyRewriter can be imported."""
    if REWRITER_AVAILABLE:
        from genesis.ontology_rewriter import OntologyRewriter
        assert OntologyRewriter is not None
    else:
        pytest.skip("OntologyRewriter module not available")


def test_rewriter_main_function():
    """Test that OntologyRewriter has a main function."""
    if REWRITER_AVAILABLE:
        from genesis.ontology_rewriter import main
        assert callable(main)
    else:
        pytest.skip("OntologyRewriter module not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 