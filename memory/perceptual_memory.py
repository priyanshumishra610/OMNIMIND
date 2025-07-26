"""
Perceptual Memory Module - Phase 19
Synthetic Perception Expansion for SentraAGI

Stores and manages perceptual data:
- Objects, masks, embeddings
- Timestamp, context
- Integration with existing memory systems
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import numpy as np
from collections import deque

logger = logging.getLogger(__name__)


class PerceptualMemory:
    """
    Perceptual Memory store for vision and sensory data.
    
    Manages storage, retrieval, and indexing of perceptual information
    including objects, segmentation masks, embeddings, and contextual data.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize Perceptual Memory with configuration.
        
        Args:
            config: Configuration dictionary with storage settings
        """
        self.config = config or self._load_default_config()
        
        # Storage settings
        self.max_entries = self.config.get('max_entries', 10000)
        self.persist_to_disk = self.config.get('persist_to_disk', True)
        self.storage_path = self.config.get('storage_path', 'data/perceptual_memory')
        
        # Memory structures
        self.perceptions = deque(maxlen=self.max_entries)
        self.object_index = {}  # object_id -> perception_ids
        self.temporal_index = {}  # timestamp_bucket -> perception_ids
        self.embedding_index = {}  # concept -> perception_ids
        
        # Statistics
        self.stats = {
            'total_perceptions': 0,
            'total_objects': 0,
            'total_embeddings': 0,
            'last_updated': None
        }
        
        # Initialize storage
        self._initialize_storage()
        
        logger.info("Perceptual Memory initialized")
    
    def _load_default_config(self) -> Dict:
        """Load default configuration from environment variables."""
        return {
            'max_entries': int(os.getenv('SENTRA_PERCEPTUAL_MEMORY_MAX_ENTRIES', '10000')),
            'persist_to_disk': os.getenv('SENTRA_PERCEPTUAL_MEMORY_PERSIST', 'true').lower() == 'true',
            'storage_path': os.getenv('SENTRA_PERCEPTUAL_MEMORY_PATH', 'data/perceptual_memory'),
            'temporal_bucket_size': 3600,  # 1 hour buckets
            'embedding_similarity_threshold': 0.8
        }
    
    def _initialize_storage(self):
        """Initialize storage directory and load existing data."""
        if self.persist_to_disk:
            os.makedirs(self.storage_path, exist_ok=True)
            self._load_existing_data()
    
    def _load_existing_data(self):
        """Load existing perceptual data from disk."""
        try:
            data_file = os.path.join(self.storage_path, 'perceptual_data.json')
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.perceptions = deque(data.get('perceptions', []), maxlen=self.max_entries)
                    self.object_index = data.get('object_index', {})
                    self.temporal_index = data.get('temporal_index', {})
                    self.embedding_index = data.get('embedding_index', {})
                    self.stats = data.get('stats', self.stats)
                
                logger.info(f"Loaded {len(self.perceptions)} existing perceptions")
        except Exception as e:
            logger.error(f"Error loading existing data: {e}")
    
    def _save_to_disk(self):
        """Save current perceptual data to disk."""
        if not self.persist_to_disk:
            return
        
        try:
            data = {
                'perceptions': list(self.perceptions),
                'object_index': self.object_index,
                'temporal_index': self.temporal_index,
                'embedding_index': self.embedding_index,
                'stats': self.stats
            }
            
            data_file = os.path.join(self.storage_path, 'perceptual_data.json')
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving to disk: {e}")
    
    def store_perception(self, perception_data: Dict) -> str:
        """
        Store a perception entry with full context.
        
        Args:
            perception_data: Complete perception data from Virtual Senses
            
        Returns:
            Unique ID of the stored perception
        """
        # Generate unique ID
        perception_id = f"perception_{int(time.time() * 1000)}_{len(self.perceptions)}"
        
        # Create storage entry
        entry = {
            'id': perception_id,
            'timestamp': perception_data.get('timestamp', time.time()),
            'frame_shape': perception_data.get('frame_shape'),
            'detections': perception_data.get('detections', []),
            'segmentation': perception_data.get('segmentation', {}),
            'embeddings': perception_data.get('embeddings', {}),
            'context': {
                'source': 'virtual_senses',
                'processing_time': time.time() - perception_data.get('timestamp', time.time())
            }
        }
        
        # Store in main memory
        self.perceptions.append(entry)
        
        # Update indexes
        self._update_object_index(perception_id, entry)
        self._update_temporal_index(perception_id, entry)
        self._update_embedding_index(perception_id, entry)
        
        # Update statistics
        self.stats['total_perceptions'] += 1
        self.stats['total_objects'] += len(entry['detections'])
        if entry['embeddings'].get('image_embedding'):
            self.stats['total_embeddings'] += 1
        self.stats['last_updated'] = time.time()
        
        # Persist to disk
        self._save_to_disk()
        
        logger.debug(f"Stored perception {perception_id} with {len(entry['detections'])} detections")
        return perception_id
    
    def _update_object_index(self, perception_id: str, entry: Dict):
        """Update object index with detected objects."""
        for detection in entry['detections']:
            object_id = detection.get('class_name', 'unknown')
            if object_id not in self.object_index:
                self.object_index[object_id] = []
            self.object_index[object_id].append(perception_id)
    
    def _update_temporal_index(self, perception_id: str, entry: Dict):
        """Update temporal index with timestamp buckets."""
        timestamp = entry['timestamp']
        bucket_size = self.config.get('temporal_bucket_size', 3600)
        bucket = int(timestamp // bucket_size)
        
        if bucket not in self.temporal_index:
            self.temporal_index[bucket] = []
        self.temporal_index[bucket].append(perception_id)
    
    def _update_embedding_index(self, perception_id: str, entry: Dict):
        """Update embedding index with concept similarities."""
        similarities = entry['embeddings'].get('similarities', {})
        for concept, similarity in similarities.items():
            if similarity > self.config.get('embedding_similarity_threshold', 0.8):
                if concept not in self.embedding_index:
                    self.embedding_index[concept] = []
                self.embedding_index[concept].append(perception_id)
    
    def get_perception(self, perception_id: str) -> Optional[Dict]:
        """
        Retrieve a specific perception by ID.
        
        Args:
            perception_id: Unique ID of the perception
            
        Returns:
            Perception data or None if not found
        """
        for perception in self.perceptions:
            if perception['id'] == perception_id:
                return perception
        return None
    
    def get_perceptions_by_object(self, object_name: str, limit: int = 100) -> List[Dict]:
        """
        Get perceptions containing a specific object.
        
        Args:
            object_name: Name of the object to search for
            limit: Maximum number of perceptions to return
            
        Returns:
            List of perception data
        """
        perception_ids = self.object_index.get(object_name, [])
        perceptions = []
        
        for pid in perception_ids[-limit:]:
            perception = self.get_perception(pid)
            if perception:
                perceptions.append(perception)
        
        return perceptions
    
    def get_perceptions_by_time_range(self, start_time: float, end_time: float) -> List[Dict]:
        """
        Get perceptions within a time range.
        
        Args:
            start_time: Start timestamp
            end_time: End timestamp
            
        Returns:
            List of perception data within the time range
        """
        perceptions = []
        for perception in self.perceptions:
            timestamp = perception['timestamp']
            if start_time <= timestamp <= end_time:
                perceptions.append(perception)
        
        return perceptions
    
    def get_perceptions_by_concept(self, concept: str, limit: int = 100) -> List[Dict]:
        """
        Get perceptions with high similarity to a concept.
        
        Args:
            concept: Concept to search for
            limit: Maximum number of perceptions to return
            
        Returns:
            List of perception data
        """
        perception_ids = self.embedding_index.get(concept, [])
        perceptions = []
        
        for pid in perception_ids[-limit:]:
            perception = self.get_perception(pid)
            if perception:
                perceptions.append(perception)
        
        return perceptions
    
    def get_recent_perceptions(self, count: int = 10) -> List[Dict]:
        """
        Get the most recent perceptions.
        
        Args:
            count: Number of recent perceptions to return
            
        Returns:
            List of recent perception data
        """
        return list(self.perceptions)[-count:]
    
    def get_memory_summary(self) -> Dict:
        """Get summary statistics of the perceptual memory."""
        return {
            'total_perceptions': len(self.perceptions),
            'total_objects_detected': len(self.object_index),
            'total_concepts_indexed': len(self.embedding_index),
            'temporal_buckets': len(self.temporal_index),
            'stats': self.stats,
            'storage_path': self.storage_path if self.persist_to_disk else None
        }
    
    def clear_memory(self):
        """Clear all stored perceptual data."""
        self.perceptions.clear()
        self.object_index.clear()
        self.temporal_index.clear()
        self.embedding_index.clear()
        self.stats = {
            'total_perceptions': 0,
            'total_objects': 0,
            'total_embeddings': 0,
            'last_updated': None
        }
        
        if self.persist_to_disk:
            self._save_to_disk()
        
        logger.info("Perceptual memory cleared")
    
    def export_data(self, filepath: str):
        """Export perceptual data to a file."""
        try:
            data = {
                'perceptions': list(self.perceptions),
                'object_index': self.object_index,
                'temporal_index': self.temporal_index,
                'embedding_index': self.embedding_index,
                'stats': self.stats,
                'export_timestamp': time.time()
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Perceptual data exported to {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")


def main():
    """Example usage of Perceptual Memory."""
    import time
    
    # Initialize perceptual memory
    memory = PerceptualMemory()
    
    # Create sample perception data
    sample_perception = {
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
    perception_id = memory.store_perception(sample_perception)
    print(f"Stored perception: {perception_id}")
    
    # Get memory summary
    summary = memory.get_memory_summary()
    print("Memory Summary:", summary)
    
    # Retrieve by object
    person_perceptions = memory.get_perceptions_by_object('person')
    print(f"Found {len(person_perceptions)} perceptions with person")
    
    # Retrieve by concept
    person_concept = memory.get_perceptions_by_concept('person')
    print(f"Found {len(person_concept)} perceptions with person concept")


if __name__ == "__main__":
    main() 