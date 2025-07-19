"""
Main Pipeline for OMNIMIND

Orchestrates the complete ingest → chunk → embed → store pipeline.
"""

from typing import List, Dict, Any
import logging
from .ingest_step import ingest_step
from .chunk_step import chunk_step
from .embed_step import embed_step
from .store_step import store_step

logger = logging.getLogger(__name__)


class OMNIMINDPipeline:
    """Main pipeline orchestrator for OMNIMIND."""
    
    def __init__(self):
        self.steps = [
            ("ingest", ingest_step),
            ("chunk", chunk_step),
            ("embed", embed_step),
            ("store", store_step)
        ]
        self.execution_history = []
    
    def run(self, sources: List[str], **kwargs) -> Dict[str, Any]:
        """Run the complete pipeline."""
        try:
            logger.info("Starting OMNIMIND pipeline")
            
            # Initialize pipeline data
            pipeline_data = {
                "sources": sources,
                **kwargs
            }
            
            # Execute each step
            for step_name, step_function in self.steps:
                logger.info(f"Executing step: {step_name}")
                
                # Execute step
                step_result = step_function(pipeline_data)
                
                # Update pipeline data with step results
                pipeline_data.update(step_result)
                
                # Record step execution
                self.execution_history.append({
                    "step": step_name,
                    "result": step_result,
                    "success": "error" not in step_result
                })
                
                # Check for errors
                if "error" in step_result:
                    logger.error(f"Step {step_name} failed: {step_result['error']}")
                    break
                
                logger.info(f"Step {step_name} completed successfully")
            
            # Prepare final result
            final_result = {
                "pipeline_success": "error" not in pipeline_data,
                "steps_executed": len(self.execution_history),
                "final_data": pipeline_data,
                "execution_history": self.execution_history
            }
            
            if final_result["pipeline_success"]:
                logger.info("OMNIMIND pipeline completed successfully")
            else:
                logger.error("OMNIMIND pipeline failed")
            
            return final_result
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            return {
                "pipeline_success": False,
                "error": str(e),
                "steps_executed": len(self.execution_history),
                "execution_history": self.execution_history
            }
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get pipeline execution history."""
        return self.execution_history.copy()
    
    def reset(self):
        """Reset pipeline state."""
        self.execution_history = []
        logger.info("Pipeline state reset")


# Convenience function for running the pipeline
def run_pipeline(sources: List[str], **kwargs) -> Dict[str, Any]:
    """Run the OMNIMIND pipeline with given sources."""
    pipeline = OMNIMINDPipeline()
    return pipeline.run(sources, **kwargs) 