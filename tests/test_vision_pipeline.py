"""
Test Vision Pipeline Module - Phase 19
Synthetic Perception Expansion for SentraAGI

Tests for Vision Pipeline functionality:
- Minimal class instantiation
- Dummy image feed
- Assert output shape
"""

import pytest
import tempfile
import os
import time
from unittest.mock import Mock, patch

# Import the module to test
try:
    from pipelines.vision_pipeline import (
        VisionPipelineConfig,
        initialize_virtual_senses,
        initialize_perceptual_memory,
        initialize_vision_agent,
        run_vision_processing,
        generate_perception_report,
        run_vision_pipeline_standalone
    )
    VISION_PIPELINE_AVAILABLE = True
except ImportError:
    VISION_PIPELINE_AVAILABLE = False


@pytest.mark.skipif(not VISION_PIPELINE_AVAILABLE, reason="Vision Pipeline not available")
class TestVisionPipeline:
    """Test cases for Vision Pipeline."""
    
    def test_vision_pipeline_config_instantiation(self):
        """Test that Vision Pipeline Config can be instantiated."""
        config = VisionPipelineConfig()
        assert config is not None
        assert hasattr(config, 'processing_interval')
        assert hasattr(config, 'max_frames_in_memory')
        assert hasattr(config, 'text_queries')
        assert hasattr(config, 'yolo_model_path')
        assert hasattr(config, 'sam_model_path')
        assert hasattr(config, 'clip_model_name')
    
    def test_vision_pipeline_config_defaults(self):
        """Test Vision Pipeline Config default values."""
        config = VisionPipelineConfig()
        
        assert config.processing_interval == 0.1
        assert config.max_frames_in_memory == 100
        assert config.yolo_model_path == "yolov8n.pt"
        assert config.sam_model_path == "sam_vit_h_4b8939.pth"
        assert config.clip_model_name == "ViT-B/32"
        assert config.max_perceptual_entries == 10000
        assert config.persist_perceptual_memory == True
        assert config.enable_world_model_integration == True
        assert config.enable_dreamscape_integration == True
    
    def test_vision_pipeline_config_custom_values(self):
        """Test Vision Pipeline Config with custom values."""
        config = VisionPipelineConfig(
            processing_interval=0.2,
            max_frames_in_memory=50,
            text_queries=['custom_object'],
            yolo_model_path="custom_yolo.pt",
            max_perceptual_entries=5000,
            persist_perceptual_memory=False
        )
        
        assert config.processing_interval == 0.2
        assert config.max_frames_in_memory == 50
        assert config.text_queries == ['custom_object']
        assert config.yolo_model_path == "custom_yolo.pt"
        assert config.max_perceptual_entries == 5000
        assert config.persist_perceptual_memory == False
    
    @patch('pipelines.vision_pipeline.VirtualSenses')
    def test_initialize_virtual_senses(self, mock_virtual_senses):
        """Test virtual senses initialization."""
        config = VisionPipelineConfig()
        mock_vs_instance = Mock()
        mock_vs_instance.get_status.return_value = {'opencv_available': True}
        mock_virtual_senses.return_value = mock_vs_instance
        
        result = initialize_virtual_senses(config)
        
        assert result == mock_vs_instance
        mock_virtual_senses.assert_called_once()
    
    @patch('pipelines.vision_pipeline.PerceptualMemory')
    def test_initialize_perceptual_memory(self, mock_perceptual_memory):
        """Test perceptual memory initialization."""
        config = VisionPipelineConfig()
        mock_memory_instance = Mock()
        mock_memory_instance.get_memory_summary.return_value = {'total_perceptions': 0}
        mock_perceptual_memory.return_value = mock_memory_instance
        
        result = initialize_perceptual_memory(config)
        
        assert result == mock_memory_instance
        mock_perceptual_memory.assert_called_once()
    
    @patch('pipelines.vision_pipeline.VisionAgent')
    @patch('pipelines.vision_pipeline.VirtualSenses')
    @patch('pipelines.vision_pipeline.PerceptualMemory')
    def test_initialize_vision_agent(
        self, 
        mock_perceptual_memory, 
        mock_virtual_senses, 
        mock_vision_agent
    ):
        """Test vision agent initialization."""
        config = VisionPipelineConfig()
        mock_vs_instance = Mock()
        mock_memory_instance = Mock()
        mock_agent_instance = Mock()
        mock_agent_instance.get_status.return_value = {'is_running': False}
        
        mock_virtual_senses.return_value = mock_vs_instance
        mock_perceptual_memory.return_value = mock_memory_instance
        mock_vision_agent.return_value = mock_agent_instance
        
        result = initialize_vision_agent(config, mock_vs_instance, mock_memory_instance)
        
        assert result == mock_agent_instance
        mock_vision_agent.assert_called_once()
        mock_agent_instance.set_perceptual_memory.assert_called_once_with(mock_memory_instance)
    
    @patch('pipelines.vision_pipeline.VisionAgent')
    def test_run_vision_processing_success(self, mock_vision_agent):
        """Test successful vision processing."""
        config = VisionPipelineConfig()
        mock_agent_instance = Mock()
        mock_agent_instance.get_status.return_value = {'is_running': False}
        mock_agent_instance.get_perception_summary.return_value = {'total_frames': 10}
        mock_agent_instance.get_recent_perceptions.return_value = [{}] * 5
        
        # Set environment variable for processing duration
        os.environ['SENTRA_VISION_PROCESSING_DURATION'] = '1'
        
        result = run_vision_processing(mock_agent_instance, config)
        
        assert result['success'] == True
        assert 'status' in result
        assert 'summary' in result
        assert 'recent_perceptions_count' in result
        assert 'processing_duration' in result
        
        mock_agent_instance.start_processing.assert_called_once()
        mock_agent_instance.stop_processing.assert_called_once()
    
    @patch('pipelines.vision_pipeline.VisionAgent')
    def test_run_vision_processing_error(self, mock_vision_agent):
        """Test vision processing with error."""
        config = VisionPipelineConfig()
        mock_agent_instance = Mock()
        mock_agent_instance.start_processing.side_effect = Exception("Test error")
        
        os.environ['SENTRA_VISION_PROCESSING_DURATION'] = '1'
        
        result = run_vision_processing(mock_agent_instance, config)
        
        assert result['success'] == False
        assert 'error' in result
        assert result['error'] == "Test error"
    
    @patch('pipelines.vision_pipeline.PerceptualMemory')
    def test_generate_perception_report(self, mock_perceptual_memory):
        """Test perception report generation."""
        mock_memory_instance = Mock()
        mock_memory_instance.get_memory_summary.return_value = {
            'total_perceptions': 5,
            'total_objects_detected': 3
        }
        mock_memory_instance.get_recent_perceptions.return_value = [
            {'detections': [{'class_name': 'person'}]},
            {'detections': [{'class_name': 'car'}]},
            {'detections': [{'class_name': 'person'}]}
        ]
        
        processing_results = {
            'success': True,
            'summary': {'total_frames': 10}
        }
        
        result = generate_perception_report(mock_memory_instance, processing_results)
        
        assert 'timestamp' in result
        assert 'memory_summary' in result
        assert 'processing_results' in result
        assert 'recent_perceptions_count' in result
        assert 'object_distribution' in result
        assert 'pipeline_status' in result
        assert result['pipeline_status'] == 'completed'
        assert result['object_distribution']['person'] == 2
        assert result['object_distribution']['car'] == 1
    
    @patch('pipelines.vision_pipeline.initialize_virtual_senses')
    @patch('pipelines.vision_pipeline.initialize_perceptual_memory')
    @patch('pipelines.vision_pipeline.initialize_vision_agent')
    @patch('pipelines.vision_pipeline.run_vision_processing')
    @patch('pipelines.vision_pipeline.generate_perception_report')
    def test_run_vision_pipeline_standalone_success(
        self,
        mock_generate_report,
        mock_run_processing,
        mock_init_agent,
        mock_init_memory,
        mock_init_vs
    ):
        """Test successful standalone pipeline execution."""
        config = VisionPipelineConfig()
        
        # Mock return values
        mock_vs = Mock()
        mock_memory = Mock()
        mock_agent = Mock()
        mock_processing_results = {'success': True}
        mock_report = {'pipeline_status': 'completed'}
        
        mock_init_vs.return_value = mock_vs
        mock_init_memory.return_value = mock_memory
        mock_init_agent.return_value = mock_agent
        mock_run_processing.return_value = mock_processing_results
        mock_generate_report.return_value = mock_report
        
        result = run_vision_pipeline_standalone(config)
        
        assert result == mock_report
        assert result['pipeline_status'] == 'completed'
        
        # Verify all steps were called
        mock_init_vs.assert_called_once_with(config)
        mock_init_memory.assert_called_once_with(config)
        mock_init_agent.assert_called_once_with(config, mock_vs, mock_memory)
        mock_run_processing.assert_called_once_with(mock_agent, config)
        mock_generate_report.assert_called_once_with(mock_memory, mock_processing_results)
        mock_agent.cleanup.assert_called_once()
    
    @patch('pipelines.vision_pipeline.initialize_virtual_senses')
    def test_run_vision_pipeline_standalone_error(self, mock_init_vs):
        """Test standalone pipeline execution with error."""
        config = VisionPipelineConfig()
        mock_init_vs.side_effect = Exception("Initialization error")
        
        result = run_vision_pipeline_standalone(config)
        
        assert result['pipeline_status'] == 'failed'
        assert 'error' in result
        assert result['error'] == "Initialization error"
    
    def test_vision_pipeline_config_post_init(self):
        """Test that config post_init sets default text queries."""
        config = VisionPipelineConfig(text_queries=None)
        
        # The post_init should set default text queries
        assert config.text_queries is not None
        assert isinstance(config.text_queries, list)
        assert len(config.text_queries) > 0


def test_vision_pipeline_import():
    """Test that Vision Pipeline can be imported."""
    if VISION_PIPELINE_AVAILABLE:
        from pipelines.vision_pipeline import VisionPipelineConfig
        assert VisionPipelineConfig is not None
    else:
        pytest.skip("Vision Pipeline module not available")


def test_vision_pipeline_main_function():
    """Test that Vision Pipeline has a main function."""
    if VISION_PIPELINE_AVAILABLE:
        from pipelines.vision_pipeline import main
        assert callable(main)
    else:
        pytest.skip("Vision Pipeline module not available")


def test_zenml_availability():
    """Test ZenML availability detection."""
    if VISION_PIPELINE_AVAILABLE:
        from pipelines.vision_pipeline import ZENML_AVAILABLE
        assert isinstance(ZENML_AVAILABLE, bool)
    else:
        pytest.skip("Vision Pipeline module not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 