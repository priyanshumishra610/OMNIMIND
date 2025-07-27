"""
Test Vision Agent Module - Phase 19
Synthetic Perception Expansion for SentraAGI

Tests for Vision Agent functionality:
- Minimal class instantiation
- Dummy image feed
- Assert output shape
"""

import pytest
import numpy as np
import time
from unittest.mock import Mock, patch

# Import the module to test
try:
    from multi_modal.vision_agent import VisionAgent
    VISION_AGENT_AVAILABLE = True
except ImportError:
    VISION_AGENT_AVAILABLE = False


@pytest.mark.skipif(not VISION_AGENT_AVAILABLE, reason="Vision Agent not available")
class TestVisionAgent:
    """Test cases for Vision Agent."""
    
    def test_vision_agent_instantiation(self):
        """Test that Vision Agent can be instantiated."""
        agent = VisionAgent()
        assert agent is not None
        assert hasattr(agent, 'config')
        assert hasattr(agent, 'virtual_senses')
        assert hasattr(agent, 'processing_interval')
    
    def test_vision_agent_config_loading(self):
        """Test that Vision Agent loads configuration correctly."""
        config = {
            'processing_interval': 0.2,
            'max_frames_in_memory': 50,
            'text_queries': ['test_object']
        }
        
        agent = VisionAgent(config)
        assert agent.processing_interval == 0.2
        assert agent.max_frames_in_memory == 50
        assert agent.text_queries == ['test_object']
    
    def test_vision_agent_status(self):
        """Test that Vision Agent returns status information."""
        agent = VisionAgent()
        status = agent.get_status()
        
        assert isinstance(status, dict)
        assert 'is_running' in status
        assert 'virtual_senses_status' in status
        assert 'frame_buffer_size' in status
        assert 'perceptual_memory_connected' in status
    
    def test_vision_agent_initial_state(self):
        """Test that Vision Agent starts in correct initial state."""
        agent = VisionAgent()
        
        assert not agent.is_running
        assert len(agent.frame_buffer) == 0
        assert agent.perceptual_memory is None
        assert agent.world_model is None
        assert agent.dreamscape is None
    
    def test_vision_agent_set_perceptual_memory(self):
        """Test setting perceptual memory."""
        agent = VisionAgent()
        mock_memory = Mock()
        
        agent.set_perceptual_memory(mock_memory)
        assert agent.perceptual_memory == mock_memory
    
    def test_vision_agent_set_world_model(self):
        """Test setting world model."""
        agent = VisionAgent()
        mock_world_model = Mock()
        
        agent.set_world_model(mock_world_model)
        assert agent.world_model == mock_world_model
    
    def test_vision_agent_set_dreamscape(self):
        """Test setting dreamscape."""
        agent = VisionAgent()
        mock_dreamscape = Mock()
        
        agent.set_dreamscape(mock_dreamscape)
        assert agent.dreamscape == mock_dreamscape
    
    def test_vision_agent_update_text_queries(self):
        """Test updating text queries."""
        agent = VisionAgent()
        new_queries = ['new_object', 'another_object']
        
        agent.update_text_queries(new_queries)
        assert agent.text_queries == new_queries
    
    def test_vision_agent_perception_summary_empty(self):
        """Test perception summary when no frames processed."""
        agent = VisionAgent()
        summary = agent.get_perception_summary()
        
        assert isinstance(summary, dict)
        assert summary['total_frames'] == 0
        assert summary['total_detections'] == 0
    
    def test_vision_agent_recent_perceptions_empty(self):
        """Test getting recent perceptions when buffer is empty."""
        agent = VisionAgent()
        recent = agent.get_recent_perceptions(5)
        
        assert isinstance(recent, list)
        assert len(recent) == 0
    
    @patch('multi_modal.vision_agent.VirtualSenses')
    def test_vision_agent_process_single_frame_no_frame(self, mock_virtual_senses):
        """Test processing when no frame is available."""
        # Mock virtual senses to return None for frame
        mock_vs_instance = Mock()
        mock_vs_instance.capture_frame.return_value = None
        mock_virtual_senses.return_value = mock_vs_instance
        
        agent = VisionAgent()
        result = agent.process_single_frame()
        
        assert result is None
    
    @patch('multi_modal.vision_agent.VirtualSenses')
    def test_vision_agent_process_single_frame_with_frame(self, mock_virtual_senses):
        """Test processing with a dummy frame."""
        # Create dummy frame
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Mock virtual senses
        mock_vs_instance = Mock()
        mock_vs_instance.capture_frame.return_value = dummy_frame
        mock_vs_instance.process_frame.return_value = {
            'timestamp': time.time(),
            'frame_shape': dummy_frame.shape,
            'detections': [],
            'segmentation': {'masks': [], 'metadata': {}},
            'embeddings': {'image_embedding': None, 'similarities': {}}
        }
        mock_virtual_senses.return_value = mock_vs_instance
        
        # Create agent after setting up the mock
        agent = VisionAgent()
        result = agent.process_single_frame()
        
        # Verify the mock was called
        mock_vs_instance.capture_frame.assert_called_once()
        mock_vs_instance.process_frame.assert_called_once_with(dummy_frame, ['person', 'car', 'building', 'object'])
        
        assert result is not None
        assert 'timestamp' in result
        assert 'frame_shape' in result
        assert 'detections' in result
        assert 'segmentation' in result
        assert 'embeddings' in result
    
    def test_vision_agent_start_stop_processing(self):
        """Test starting and stopping processing."""
        agent = VisionAgent()
        
        # Test start
        agent.start_processing()
        assert agent.is_running
        
        # Test stop
        agent.stop_processing()
        assert not agent.is_running
    
    def test_vision_agent_cleanup(self):
        """Test cleanup functionality."""
        agent = VisionAgent()
        
        # Should not raise any exceptions
        agent.cleanup()
        
        # Verify cleanup sets running to False
        assert not agent.is_running


def test_vision_agent_import():
    """Test that Vision Agent can be imported."""
    if VISION_AGENT_AVAILABLE:
        from multi_modal.vision_agent import VisionAgent
        assert VisionAgent is not None
    else:
        pytest.skip("Vision Agent module not available")


def test_vision_agent_main_function():
    """Test that Vision Agent has a main function."""
    if VISION_AGENT_AVAILABLE:
        from multi_modal.vision_agent import main
        assert callable(main)
    else:
        pytest.skip("Vision Agent module not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 