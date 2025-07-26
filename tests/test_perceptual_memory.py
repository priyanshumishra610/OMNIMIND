"""
Test Perceptual Memory Module - Phase 19
Synthetic Perception Expansion for SentraAGI

Tests for Perceptual Memory functionality:
- Minimal class instantiation
- Dummy image feed
- Assert output shape
"""

import pytest
import tempfile
import os
import time
import json
from unittest.mock import Mock, patch

# Import the module to test
try:
    from memory.perceptual_memory import PerceptualMemory
    PERCEPTUAL_MEMORY_AVAILABLE = True
except ImportError:
    PERCEPTUAL_MEMORY_AVAILABLE = False


@pytest.mark.skipif(not PERCEPTUAL_MEMORY_AVAILABLE, reason="Perceptual Memory not available")
class TestPerceptualMemory:
    """Test cases for Perceptual Memory."""
    
    def test_perceptual_memory_instantiation(self):
        """Test that Perceptual Memory can be instantiated."""
        memory = PerceptualMemory()
        assert memory is not None
        assert hasattr(memory, 'config')
        assert hasattr(memory, 'perceptions')
        assert hasattr(memory, 'object_index')
        assert hasattr(memory, 'temporal_index')
        assert hasattr(memory, 'embedding_index')
    
    def test_perceptual_memory_config_loading(self):
        """Test that Perceptual Memory loads configuration correctly."""
        config = {
            'max_entries': 5000,
            'persist_to_disk': False,
            'storage_path': '/tmp/test_memory'
        }
        
        memory = PerceptualMemory(config)
        assert memory.max_entries == 5000
        assert memory.persist_to_disk == False
        assert memory.storage_path == '/tmp/test_memory'
    
    def test_perceptual_memory_initial_state(self):
        """Test that Perceptual Memory starts in correct initial state."""
        memory = PerceptualMemory()
        
        assert len(memory.perceptions) == 0
        assert len(memory.object_index) == 0
        assert len(memory.temporal_index) == 0
        assert len(memory.embedding_index) == 0
        assert memory.stats['total_perceptions'] == 0
    
    def test_perceptual_memory_store_perception(self):
        """Test storing a perception entry."""
        memory = PerceptualMemory()
        
        # Create sample perception data
        perception_data = {
            'timestamp': time.time(),
            'frame_shape': (480, 640, 3),
            'detections': [
                {
                    'bbox': [100, 100, 200, 200],
                    'confidence': 0.95,
                    'class_id': 0,
                    'class_name': 'person'
                }
            ],
            'segmentation': {
                'masks': [],
                'metadata': {'num_masks': 0}
            },
            'embeddings': {
                'image_embedding': None,
                'similarities': {'person': 0.9, 'car': 0.1}
            }
        }
        
        # Store perception
        perception_id = memory.store_perception(perception_data)
        
        assert perception_id is not None
        assert len(memory.perceptions) == 1
        assert memory.stats['total_perceptions'] == 1
        assert memory.stats['total_objects'] == 1
    
    def test_perceptual_memory_get_perception(self):
        """Test retrieving a specific perception."""
        memory = PerceptualMemory()
        
        # Store a perception
        perception_data = {
            'timestamp': time.time(),
            'frame_shape': (480, 640, 3),
            'detections': [],
            'segmentation': {'masks': [], 'metadata': {}},
            'embeddings': {'image_embedding': None, 'similarities': {}}
        }
        
        perception_id = memory.store_perception(perception_data)
        
        # Retrieve the perception
        retrieved = memory.get_perception(perception_id)
        
        assert retrieved is not None
        assert retrieved['id'] == perception_id
        assert retrieved['frame_shape'] == (480, 640, 3)
    
    def test_perceptual_memory_get_perception_not_found(self):
        """Test retrieving a non-existent perception."""
        memory = PerceptualMemory()
        
        result = memory.get_perception("non_existent_id")
        assert result is None
    
    def test_perceptual_memory_get_perceptions_by_object(self):
        """Test retrieving perceptions by object."""
        memory = PerceptualMemory()
        
        # Store perceptions with different objects
        perception_data_1 = {
            'timestamp': time.time(),
            'frame_shape': (480, 640, 3),
            'detections': [{'class_name': 'person'}],
            'segmentation': {'masks': [], 'metadata': {}},
            'embeddings': {'image_embedding': None, 'similarities': {}}
        }
        
        perception_data_2 = {
            'timestamp': time.time(),
            'frame_shape': (480, 640, 3),
            'detections': [{'class_name': 'car'}],
            'segmentation': {'masks': [], 'metadata': {}},
            'embeddings': {'image_embedding': None, 'similarities': {}}
        }
        
        memory.store_perception(perception_data_1)
        memory.store_perception(perception_data_2)
        
        # Get perceptions by object
        person_perceptions = memory.get_perceptions_by_object('person')
        car_perceptions = memory.get_perceptions_by_object('car')
        
        assert len(person_perceptions) == 1
        assert len(car_perceptions) == 1
        assert person_perceptions[0]['detections'][0]['class_name'] == 'person'
        assert car_perceptions[0]['detections'][0]['class_name'] == 'car'
    
    def test_perceptual_memory_get_perceptions_by_time_range(self):
        """Test retrieving perceptions by time range."""
        memory = PerceptualMemory()
        
        # Store perceptions with different timestamps
        base_time = time.time()
        
        perception_data_1 = {
            'timestamp': base_time,
            'frame_shape': (480, 640, 3),
            'detections': [],
            'segmentation': {'masks': [], 'metadata': {}},
            'embeddings': {'image_embedding': None, 'similarities': {}}
        }
        
        perception_data_2 = {
            'timestamp': base_time + 100,
            'frame_shape': (480, 640, 3),
            'detections': [],
            'segmentation': {'masks': [], 'metadata': {}},
            'embeddings': {'image_embedding': None, 'similarities': {}}
        }
        
        memory.store_perception(perception_data_1)
        memory.store_perception(perception_data_2)
        
        # Get perceptions in time range
        perceptions = memory.get_perceptions_by_time_range(base_time, base_time + 50)
        
        assert len(perceptions) == 1
        assert perceptions[0]['timestamp'] == base_time
    
    def test_perceptual_memory_get_perceptions_by_concept(self):
        """Test retrieving perceptions by concept similarity."""
        memory = PerceptualMemory()
        
        # Store perception with concept similarities
        perception_data = {
            'timestamp': time.time(),
            'frame_shape': (480, 640, 3),
            'detections': [],
            'segmentation': {'masks': [], 'metadata': {}},
            'embeddings': {
                'image_embedding': None,
                'similarities': {'person': 0.9, 'car': 0.1}
            }
        }
        
        memory.store_perception(perception_data)
        
        # Get perceptions by concept
        person_perceptions = memory.get_perceptions_by_concept('person')
        car_perceptions = memory.get_perceptions_by_concept('car')
        
        assert len(person_perceptions) == 1  # High similarity
        assert len(car_perceptions) == 0     # Low similarity
    
    def test_perceptual_memory_get_recent_perceptions(self):
        """Test getting recent perceptions."""
        memory = PerceptualMemory()
        
        # Store multiple perceptions
        for i in range(5):
            perception_data = {
                'timestamp': time.time() + i,
                'frame_shape': (480, 640, 3),
                'detections': [],
                'segmentation': {'masks': [], 'metadata': {}},
                'embeddings': {'image_embedding': None, 'similarities': {}}
            }
            memory.store_perception(perception_data)
        
        # Get recent perceptions
        recent = memory.get_recent_perceptions(3)
        
        assert len(recent) == 3
        assert recent[-1]['timestamp'] > recent[0]['timestamp']  # Most recent last
    
    def test_perceptual_memory_get_memory_summary(self):
        """Test getting memory summary."""
        memory = PerceptualMemory()
        
        # Store some perceptions
        perception_data = {
            'timestamp': time.time(),
            'frame_shape': (480, 640, 3),
            'detections': [{'class_name': 'person'}],
            'segmentation': {'masks': [], 'metadata': {}},
            'embeddings': {'image_embedding': None, 'similarities': {'person': 0.9}}
        }
        
        memory.store_perception(perception_data)
        
        # Get summary
        summary = memory.get_memory_summary()
        
        assert isinstance(summary, dict)
        assert summary['total_perceptions'] == 1
        assert summary['total_objects_detected'] == 1
        assert summary['total_concepts_indexed'] == 1
    
    def test_perceptual_memory_clear_memory(self):
        """Test clearing memory."""
        memory = PerceptualMemory()
        
        # Store some data
        perception_data = {
            'timestamp': time.time(),
            'frame_shape': (480, 640, 3),
            'detections': [],
            'segmentation': {'masks': [], 'metadata': {}},
            'embeddings': {'image_embedding': None, 'similarities': {}}
        }
        
        memory.store_perception(perception_data)
        assert len(memory.perceptions) > 0
        
        # Clear memory
        memory.clear_memory()
        
        assert len(memory.perceptions) == 0
        assert len(memory.object_index) == 0
        assert len(memory.temporal_index) == 0
        assert len(memory.embedding_index) == 0
        assert memory.stats['total_perceptions'] == 0
    
    def test_perceptual_memory_export_data(self):
        """Test exporting data to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = PerceptualMemory({'storage_path': tmpdir})
            
            # Store some data
            perception_data = {
                'timestamp': time.time(),
                'frame_shape': (480, 640, 3),
                'detections': [],
                'segmentation': {'masks': [], 'metadata': {}},
                'embeddings': {'image_embedding': None, 'similarities': {}}
            }
            
            memory.store_perception(perception_data)
            
            # Export data
            export_path = os.path.join(tmpdir, 'export.json')
            memory.export_data(export_path)
            
            # Verify export file exists and contains data
            assert os.path.exists(export_path)
            
            with open(export_path, 'r') as f:
                exported_data = json.load(f)
            
            assert 'perceptions' in exported_data
            assert 'stats' in exported_data
            assert len(exported_data['perceptions']) == 1


def test_perceptual_memory_import():
    """Test that Perceptual Memory can be imported."""
    if PERCEPTUAL_MEMORY_AVAILABLE:
        from memory.perceptual_memory import PerceptualMemory
        assert PerceptualMemory is not None
    else:
        pytest.skip("Perceptual Memory module not available")


def test_perceptual_memory_main_function():
    """Test that Perceptual Memory has a main function."""
    if PERCEPTUAL_MEMORY_AVAILABLE:
        from memory.perceptual_memory import main
        assert callable(main)
    else:
        pytest.skip("Perceptual Memory module not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 