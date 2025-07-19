import logging
from memory.episodic_memory import EpisodicMemory
from memory.memory_indexer import MemoryIndexer

logger = logging.getLogger(__name__)

class MemoryLogger:
    """
    Logs and stores each new session's full memory snapshot.
    """
    def __init__(self, memory_path="memory/episodic_memory.jsonl"):
        self.memory = EpisodicMemory(memory_path)
        self.indexer = MemoryIndexer(memory_path)

    def log_memory(self, data: dict, embed_fn=None):
        memory_id = self.memory.store_memory(data)
        self.indexer.index_memory({**data, "id": memory_id}, embed_fn=embed_fn)
        logger.info(f"Memory snapshot stored and indexed: {memory_id}")
        return memory_id 