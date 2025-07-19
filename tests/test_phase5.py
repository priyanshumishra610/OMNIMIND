import pytest
from memory.episodic_memory import EpisodicMemory
from memory.memory_indexer import MemoryIndexer
from memory.memory_query import MemoryQuery
from verifier.immutable_verifier import ImmutableVerifier

def test_store_and_retrieve_memory():
    mem = EpisodicMemory("memory/test_mem.jsonl")
    data = {"query": "test", "final_answer": "42", "chain_of_thought": "reasoning", "proof_hash": "abc", "hypothetical_branches": [], "config_hash": "def"}
    memory_id = mem.store_memory(data)
    retrieved = mem.get_memory_by_id(memory_id)
    assert retrieved["final_answer"] == "42"

def test_index_and_reindex():
    mem = EpisodicMemory("memory/test_mem.jsonl")
    idx = MemoryIndexer("memory/test_mem.jsonl", "memory/test_index.json")
    idx.reindex_all(embed_fn=lambda x: [1.0, 2.0, 3.0])
    assert isinstance(idx.memory_ids, list)

def test_query_by_date():
    mem = EpisodicMemory("memory/test_mem.jsonl")
    idx = MemoryIndexer("memory/test_mem.jsonl", "memory/test_index.json")
    q = MemoryQuery("memory/test_mem.jsonl")
    mem.store_memory({"query": "date test", "final_answer": "ok", "timestamp": "2024-06-01T12:00:00"})
    results = q.query_by_date("2024-06-01")
    assert results

def test_query_by_topic():
    mem = EpisodicMemory("memory/test_mem.jsonl")
    q = MemoryQuery("memory/test_mem.jsonl")
    mem.store_memory({"query": "topic test", "final_answer": "ok"})
    results = q.query_by_topic("topic")
    assert results

def test_hash_memory():
    data = {"query": "hash test", "final_answer": "ok"}
    proof = ImmutableVerifier.hash_memory(data)
    assert len(proof) == 64 