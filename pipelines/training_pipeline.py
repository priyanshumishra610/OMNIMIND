"""
Training Pipeline for OMNIMIND

Handles model training pipeline using ZenML.
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TrainingPipeline:
    """Model training pipeline for OMNIMIND."""
    
    def __init__(self, pipeline_name: str = "omnimind_training"):
        self.pipeline_name = pipeline_name
        self.steps = []
        self.execution_history = []
    
    def add_step(self, step_name: str, step_function, 
                 dependencies: List[str] = None):
        """Add a step to the pipeline."""
        step = {
            "name": step_name,
            "function": step_function,
            "dependencies": dependencies or [],
            "status": "pending"
        }
        self.steps.append(step)
        logger.info(f"Added step: {step_name}")
    
    def execute(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the training pipeline."""
        try:
            logger.info(f"Starting training pipeline: {self.pipeline_name}")
            
            # Execute pipeline steps
            current_data = training_data.copy()
            
            for step in self.steps:
                step_result = self._execute_step(step, current_data)
                current_data.update(step_result.get("output", {}))
            
            return current_data
            
        except Exception as e:
            logger.error(f"Training pipeline failed: {e}")
            return {"error": str(e)}
    
    def _execute_step(self, step: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single pipeline step."""
        import time
        start_time = time.time()
        
        try:
            step["status"] = "running"
            output = step["function"](input_data)
            step["status"] = "completed"
            
            duration = time.time() - start_time
            
            return {
                "status": "completed",
                "output": output,
                "duration": duration
            }
        except Exception as e:
            step["status"] = "failed"
            duration = time.time() - start_time
            
            logger.error(f"Step {step['name']} failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "duration": duration
            } 