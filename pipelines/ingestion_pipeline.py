"""
Ingestion Pipeline for OMNIMIND

Handles data ingestion pipeline using ZenML.
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """Data ingestion pipeline for OMNIMIND."""
    
    def __init__(self, pipeline_name: str = "omnimind_ingestion"):
        self.pipeline_name = pipeline_name
        self.steps = []
        self.execution_history = []
    
    def add_step(self, step_name: str, step_function: callable, 
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
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the ingestion pipeline."""
        try:
            logger.info(f"Starting ingestion pipeline: {self.pipeline_name}")
            
            # Track execution
            execution_id = f"exec_{len(self.execution_history) + 1}"
            execution_record = {
                "execution_id": execution_id,
                "pipeline_name": self.pipeline_name,
                "steps": [],
                "status": "running"
            }
            
            current_data = input_data.copy()
            
            # Execute steps in dependency order
            executed_steps = set()
            
            while len(executed_steps) < len(self.steps):
                for step in self.steps:
                    if step["name"] in executed_steps:
                        continue
                    
                    # Check if dependencies are met
                    dependencies_met = all(
                        dep in executed_steps for dep in step["dependencies"]
                    )
                    
                    if dependencies_met:
                        # Execute step
                        step_result = self._execute_step(step, current_data)
                        executed_steps.add(step["name"])
                        
                        # Update current data
                        current_data.update(step_result.get("output", {}))
                        
                        # Record step execution
                        execution_record["steps"].append({
                            "step_name": step["name"],
                            "status": step_result["status"],
                            "duration": step_result.get("duration", 0),
                            "output_keys": list(step_result.get("output", {}).keys())
                        })
                        
                        logger.info(f"Executed step: {step['name']}")
            
            execution_record["status"] = "completed"
            execution_record["final_data_keys"] = list(current_data.keys())
            self.execution_history.append(execution_record)
            
            logger.info(f"Pipeline completed: {self.pipeline_name}")
            return current_data
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            execution_record["status"] = "failed"
            execution_record["error"] = str(e)
            self.execution_history.append(execution_record)
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
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get pipeline execution history."""
        return self.execution_history.copy()
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status."""
        return {
            "pipeline_name": self.pipeline_name,
            "total_steps": len(self.steps),
            "step_names": [step["name"] for step in self.steps],
            "total_executions": len(self.execution_history)
        } 