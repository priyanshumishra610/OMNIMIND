from typing import List, Dict, Any
from memory.episodic_memory import EpisodicMemory
from memory.memory_indexer import MemoryIndexer

class MemoryQuery:
    """
    Query interface for episodic memory.
    """
    def __init__(self, memory_path="memory/episodic_memory.jsonl"):
        self.memory = EpisodicMemory(memory_path)
        self.indexer = MemoryIndexer(memory_path)

    def query_by_date(self, date: str) -> List[Dict[str, Any]]:
        ids = self.indexer.search_by_date(date)
        return [self.memory.get_memory_by_id(i) for i in ids]

    def query_by_topic(self, keyword: str) -> List[Dict[str, Any]]:
        ids = self.indexer.search_by_topic(keyword)
        return [self.memory.get_memory_by_id(i) for i in ids]

    def query_by_semantic(self, query_text: str, embed_fn, top_k=5) -> List[Dict[str, Any]]:
        ids = self.indexer.search_by_semantic(query_text, embed_fn, top_k=top_k)
        return [self.memory.get_memory_by_id(i) for i in ids] 