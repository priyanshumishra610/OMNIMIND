import os
import json
import threading
from typing import List, Dict, Any, Optional
from datetime import datetime

class ProceduralManager:
    """
    Manages procedural memory: stores, retrieves, and applies reusable workflows/strategies.
    Stores each workflow as a JSONL entry for hashable, auditable logs.
    Configurable via environment variables. Thread-safe.
    """
    def __init__(self, workflow_path: Optional[str] = None):
        """
        Args:
            workflow_path (str): Path to the procedural memory log file (JSONL).
        """
        self.workflow_path = workflow_path or os.getenv("PROCEDURAL_MEMORY_LOG", "memory/procedural_memory.jsonl")
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(self.workflow_path), exist_ok=True)

    def save_workflow(self, workflow_id: str, steps: List[Dict[str, Any]], description: str = "", tags: Optional[List[str]] = None, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Saves a workflow/strategy to procedural memory.
        Args:
            workflow_id (str): Unique workflow identifier.
            steps (List[Dict]): List of steps (each step is a dict).
            description (str): Description of the workflow.
            tags (List[str], optional): Tags for searching.
            extra (dict, optional): Additional metadata.
        """
        workflow = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "workflow_id": workflow_id,
            "steps": steps,
            "description": description,
            "tags": tags or [],
            "extra": extra or {}
        }
        with self._lock, open(self.workflow_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(workflow, sort_keys=True) + "\n")

    def get_similar_workflow(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves top_k workflows most similar to the query (by tag or description match).
        Args:
            query (str): Query string (searches tags and description).
            top_k (int): Number of top results to return.
        Returns:
            List[Dict]: List of matching workflow dicts.
        """
        workflows = self._load_workflows()
        scored = []
        for wf in workflows:
            score = 0
            if query.lower() in wf.get("description", "").lower():
                score += 2
            if any(query.lower() in tag.lower() for tag in wf.get("tags", [])):
                score += 1
            if score > 0:
                scored.append((score, wf))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [wf for _, wf in scored[:top_k]]

    def apply_workflow(self, workflow_id: str, context: Optional[Dict[str, Any]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieves and returns the steps for a given workflow_id, optionally injecting context.
        Args:
            workflow_id (str): Workflow identifier.
            context (dict, optional): Context to inject into steps.
        Returns:
            List[Dict]: List of steps with context applied, or None if not found.
        """
        workflows = self._load_workflows()
        for wf in workflows:
            if wf["workflow_id"] == workflow_id:
                steps = wf["steps"]
                if context:
                    # Optionally inject context into each step
                    steps = [self._inject_context(step, context) for step in steps]
                return steps
        return None

    def _inject_context(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Injects context into a workflow step (simple merge).
        """
        step = step.copy()
        step.update(context)
        return step

    def _load_workflows(self) -> List[Dict[str, Any]]:
        """
        Loads all workflows from the procedural memory log.
        Returns:
            List[Dict]: List of workflow dicts.
        """
        if not os.path.exists(self.workflow_path):
            return []
        workflows = []
        with self._lock, open(self.workflow_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    wf = json.loads(line)
                    workflows.append(wf)
                except Exception:
                    continue
        return workflows 