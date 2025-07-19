import os
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
import dateparser

try:
    import faiss
    import numpy as np
except ImportError:
    faiss = None
    np = None

class MemoryIndexer:
    """
    Builds semantic and temporal index for episodic memory.
    """
    def __init__(self, memory_path: str = "memory/episodic_memory.jsonl", index_path: str = "memory/memory_index.json"):
        self.memory_path = memory_path
        self.index_path = index_path
        self.semantic_index = None
        self.memory_ids = []
        self.embeddings = []
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_path):
            with open(self.index_path, "r") as f:
                data = json.load(f)
                self.memory_ids = data.get("memory_ids", [])
                self.embeddings = data.get("embeddings", [])
        else:
            self.memory_ids = []
            self.embeddings = []

    def _save_index(self):
        with open(self.index_path, "w") as f:
            json.dump({"memory_ids": self.memory_ids, "embeddings": self.embeddings}, f)

    def index_memory(self, data: Dict[str, Any], embed_fn=None):
        """
        Adds a memory to the semantic and temporal index.
        """
        memory_id = data["id"]
        self.memory_ids.append(memory_id)
        if embed_fn:
            emb = embed_fn(data.get("final_answer", "") + " " + data.get("query", ""))
            self.embeddings.append(emb)
        self._save_index()

    def reindex_all(self, embed_fn=None):
        """
        Rebuilds the index from all memories.
        """
        from memory.episodic_memory import EpisodicMemory
        mem = EpisodicMemory(self.memory_path)
        self.memory_ids = []
        self.embeddings = []
        for m in mem.get_all_memories():
            self.index_memory(m, embed_fn=embed_fn)
        self._save_index()

    def search_by_semantic(self, query: str, embed_fn, top_k: int = 5) -> List[str]:
        """
        Returns memory IDs most similar to the query.
        """
        if not faiss or not np or not self.embeddings:
            return []
        query_emb = np.array([embed_fn(query)], dtype="float32")
        index = faiss.IndexFlatL2(len(self.embeddings[0]))
        index.add(np.array(self.embeddings, dtype="float32"))
        D, I = index.search(query_emb, top_k)
        return [self.memory_ids[i] for i in I[0] if i < len(self.memory_ids)]

    def search_by_date(self, date_str: str) -> List[str]:
        """
        Returns memory IDs for a given date (YYYY-MM-DD or natural language).
        """
        target = dateparser.parse(date_str)
        from memory.episodic_memory import EpisodicMemory
        mem = EpisodicMemory(self.memory_path)
        results = []
        for m in mem.get_all_memories():
            ts = dateparser.parse(m.get("timestamp", ""))
            if ts and target and ts.date() == target.date():
                results.append(m["id"])
        return results

    def search_by_topic(self, keyword: str) -> List[str]:
        """
        Returns memory IDs where the topic/keyword appears in query or answer.
        """
        from memory.episodic_memory import EpisodicMemory
        mem = EpisodicMemory(self.memory_path)
        results = []
        for m in mem.get_all_memories():
            if keyword.lower() in (m.get("query", "") + m.get("final_answer", "")).lower():
                results.append(m["id"])
        return results 