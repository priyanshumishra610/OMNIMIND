"""
Vision Agent Module - Phase 19
Synthetic Perception Expansion for SentraAGI

Orchestrates the complete vision pipeline:
- Pulls frames from Virtual Senses
- Runs detection, segmentation, embedding
- Logs results to Perceptual Memory
- Integrates with World Model and Dreamscape
"""

import time
import logging
from typing import Dict, List, Optional, Any
from threading import Thread, Event
import numpy as np

from .virtual_senses import VirtualSenses

logger = logging.getLogger(__name__)


class VisionAgent:
    """
    Vision Agent orchestrator for real-time perception processing.
    
    Coordinates frame capture, analysis, and memory storage.
    Provides continuous perception feed to World Model and Dreamscape.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize Vision Agent with configuration.
        
        Args:
            config: Configuration dictionary with processing settings
        """
        self.config = config or self._load_default_config()
        self.virtual_senses = VirtualSenses(self.config.get('virtual_senses', {}))
        
        # Processing settings
        self.processing_interval = self.config.get('processing_interval', 0.1)  # seconds
        self.max_frames_in_memory = self.config.get('max_frames_in_memory', 100)
        self.text_queries = self.config.get('text_queries', ['person', 'car', 'building', 'object'])
        
        # State management
        self.is_running = False
        self.stop_event = Event()
        self.processing_thread = None
        
        # Memory integration (will be set by external components)
        self.perceptual_memory = None
        self.world_model = None
        self.dreamscape = None
        
        # Frame buffer
        self.frame_buffer = []
        self.last_processed_timestamp = 0
        
        logger.info("Vision Agent initialized")
    
    def _load_default_config(self) -> Dict:
        """Load default configuration."""
        return {
            'processing_interval': 0.1,  # seconds
            'max_frames_in_memory': 100,
            'text_queries': ['person', 'car', 'building', 'object'],
            'virtual_senses': {
                'opencv_device': 0,
                'yolo_model_path': 'yolov8n.pt',
                'sam_model_path': 'sam_vit_h_4b8939.pth',
                'clip_model_name': 'ViT-B/32'
            }
        }
    
    def set_perceptual_memory(self, memory):
        """Set the perceptual memory instance for logging results."""
        self.perceptual_memory = memory
        logger.info("Perceptual memory connected to Vision Agent")
    
    def set_world_model(self, world_model):
        """Set the world model instance for perception integration."""
        self.world_model = world_model
        logger.info("World model connected to Vision Agent")
    
    def set_dreamscape(self, dreamscape):
        """Set the dreamscape instance for perception integration."""
        self.dreamscape = dreamscape
        logger.info("Dreamscape connected to Vision Agent")
    
    def process_single_frame(self) -> Optional[Dict]:
        """
        Process a single frame through the complete pipeline.
        
        Returns:
            Processed perception data or None if no frame available
        """
        # Capture frame
        frame = self.virtual_senses.capture_frame()
        if frame is None:
            return None
        
        # Process frame through virtual senses
        perception_data = self.virtual_senses.process_frame(frame, self.text_queries)
        
        # Add frame to buffer
        self.frame_buffer.append({
            'frame': frame,
            'perception_data': perception_data,
            'timestamp': time.time()
        })
        
        # Maintain buffer size
        if len(self.frame_buffer) > self.max_frames_in_memory:
            self.frame_buffer.pop(0)
        
        # Log to perceptual memory
        if self.perceptual_memory:
            try:
                self.perceptual_memory.store_perception(perception_data)
            except Exception as e:
                logger.error(f"Error storing perception in memory: {e}")
        
        # Feed to world model
        if self.world_model:
            try:
                self.world_model.update_perception(perception_data)
            except Exception as e:
                logger.error(f"Error updating world model: {e}")
        
        # Feed to dreamscape
        if self.dreamscape:
            try:
                self.dreamscape.process_perception(perception_data)
            except Exception as e:
                logger.error(f"Error processing perception in dreamscape: {e}")
        
        self.last_processed_timestamp = perception_data['timestamp']
        return perception_data
    
    def _processing_loop(self):
        """Main processing loop for continuous frame analysis."""
        logger.info("Vision Agent processing loop started")
        
        while not self.stop_event.is_set():
            try:
                # Process frame
                perception_data = self.process_single_frame()
                
                if perception_data:
                    logger.debug(f"Processed frame: {len(perception_data.get('detections', []))} detections")
                
                # Wait for next processing cycle
                time.sleep(self.processing_interval)
                
            except Exception as e:
                logger.error(f"Error in processing loop: {e}")
                time.sleep(1)  # Wait before retrying
        
        logger.info("Vision Agent processing loop stopped")
    
    def start_processing(self):
        """Start continuous frame processing in background thread."""
        if self.is_running:
            logger.warning("Vision Agent already running")
            return
        
        self.is_running = True
        self.stop_event.clear()
        self.processing_thread = Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        
        logger.info("Vision Agent started")
    
    def stop_processing(self):
        """Stop continuous frame processing."""
        if not self.is_running:
            logger.warning("Vision Agent not running")
            return
        
        self.is_running = False
        self.stop_event.set()
        
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        
        logger.info("Vision Agent stopped")
    
    def get_status(self) -> Dict:
        """Get current status of Vision Agent."""
        return {
            'is_running': self.is_running,
            'virtual_senses_status': self.virtual_senses.get_status(),
            'frame_buffer_size': len(self.frame_buffer),
            'last_processed_timestamp': self.last_processed_timestamp,
            'perceptual_memory_connected': self.perceptual_memory is not None,
            'world_model_connected': self.world_model is not None,
            'dreamscape_connected': self.dreamscape is not None
        }
    
    def get_recent_perceptions(self, count: int = 10) -> List[Dict]:
        """
        Get recent perception data from buffer.
        
        Args:
            count: Number of recent perceptions to return
            
        Returns:
            List of recent perception data
        """
        return self.frame_buffer[-count:] if self.frame_buffer else []
    
    def get_perception_summary(self) -> Dict:
        """Get summary of recent perception activity."""
        if not self.frame_buffer:
            return {'total_frames': 0, 'total_detections': 0}
        
        total_detections = sum(
            len(frame_data['perception_data'].get('detections', []))
            for frame_data in self.frame_buffer
        )
        
        return {
            'total_frames': len(self.frame_buffer),
            'total_detections': total_detections,
            'processing_interval': self.processing_interval,
            'buffer_utilization': len(self.frame_buffer) / self.max_frames_in_memory
        }
    
    def update_text_queries(self, queries: List[str]):
        """Update the text queries used for CLIP concept grounding."""
        self.text_queries = queries
        logger.info(f"Updated text queries: {queries}")
    
    def cleanup(self):
        """Clean up resources."""
        self.stop_processing()
        if self.virtual_senses:
            self.virtual_senses.cleanup()


def main():
    """Example usage of Vision Agent."""
    import time
    
    # Initialize vision agent
    agent = VisionAgent()
    
    try:
        print("Vision Agent Status:", agent.get_status())
        
        # Start processing
        agent.start_processing()
        
        # Let it run for a few seconds
        time.sleep(3)
        
        # Get status and summary
        print("Updated Status:", agent.get_status())
        print("Perception Summary:", agent.get_perception_summary())
        
        # Get recent perceptions
        recent = agent.get_recent_perceptions(5)
        print(f"Recent perceptions: {len(recent)}")
        
        # Stop processing
        agent.stop_processing()
        
    finally:
        agent.cleanup()


if __name__ == "__main__":
    main()
