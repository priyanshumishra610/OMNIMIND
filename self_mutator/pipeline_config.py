import json
import copy
from typing import Dict, Any

class PipelineConfig:
    """
    Stores and manages all tunable pipeline parameters.
    """
    DEFAULTS = {
        "chunk_size": 200,
        "chunk_overlap": 0.2,
        "embedding_model": "openai",
        "retrieval_top_k": 10,
        "swarm_threshold": 0.8,
        "vector_store": "faiss"
    }

    def __init__(self, config: Dict[str, Any] = None):
        self.config = copy.deepcopy(self.DEFAULTS)
        if config:
            self.config.update(config)

    def to_dict(self) -> Dict[str, Any]:
        return copy.deepcopy(self.config)

    def update(self, updates: Dict[str, Any]):
        self.config.update(updates)

    def serialize(self) -> str:
        return json.dumps(self.config, sort_keys=True)

    @classmethod
    def deserialize(cls, s: str):
        return cls(json.loads(s)) 