"""
Test Memory Components
"""
import os
import tempfile
import shutil
import numpy as np
from memory.episodic_manager import EpisodicManager
from memory.semantic_manager import SemanticManager
from memory.procedural_manager import ProceduralManager
from reasoners.memory_reasoner import MemoryReasoner
from logger.memory_logger import MemoryLogger

def test_episodic_manager():
    """Test storing, retrieving, and pruning episodic memory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = os.path.join(tmpdir, "episodic.jsonl")
        manager = EpisodicManager(log_path=log_path, retention_days=0)  # Use 0 to trigger pruning
        
        # Add multiple test sessions
        test_sessions = [
            ("sess1", "What is AI?", "Thinking about AI", "Good", {"foo": "bar"}),
            ("sess2", "How does ML work?", "Explaining ML", "Good", {"topic": "ml"}),
            ("sess3", "Tell me about NLP", "Discussing NLP", "Good", {"field": "nlp"})
        ]
        
        for session in test_sessions:
            manager.log_session(*session)
        
        # Verify sessions were added
        all_sessions = manager.retrieve_sessions()
        assert len(all_sessions) == len(test_sessions)
        
        # Test retrieval by session ID
        sess1 = manager.retrieve_sessions(session_id="sess1")
        assert len(sess1) == 1
        assert sess1[0]["user_query"] == "What is AI?"
        
        # Test pruning (retention_days = 0 should remove all sessions)
        removed = manager.prune_sessions()
        assert removed == len(test_sessions)  # Should remove all test sessions
        
        # Verify all sessions were pruned
        remaining = manager.retrieve_sessions()
        assert len(remaining) == 0

def test_semantic_manager():
    """Test clustering and semantic search."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fake vector DB
        from vectordb import VectorDB
        db = VectorDB(db_path=tmpdir)
        vectors = [
            {"embedding": [1.0, 0.0], "text": "cat"},
            {"embedding": [0.9, 0.1], "text": "kitten"},
            {"embedding": [0.0, 1.0], "text": "dog"},
            {"embedding": [0.1, 0.9], "text": "puppy"}
        ]
        db.create_collection("test")
        db.add_vectors("test", vectors)
        from kg import KnowledgeGraphManager
        kg = KnowledgeGraphManager(use_neo4j=False)
        manager = SemanticManager(vectordb=db, kg_manager=kg, collection_name="test", n_clusters=2)
        labels = manager.cluster_vectors()
        assert len(labels) == 4
        manager.link_to_kg()
        assert len(manager.cluster_to_kg) == 2
        # Semantic search
        results = manager.semantic_search([1.0, 0.0], top_k=2)
        assert len(results) == 2

def test_procedural_manager():
    """Test saving, retrieving, and applying workflows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        wf_path = os.path.join(tmpdir, "procedural.jsonl")
        manager = ProceduralManager(workflow_path=wf_path)
        steps = [{"name": "step1"}, {"name": "step2"}]
        manager.save_workflow("wf1", steps, description="Test workflow", tags=["test"])
        similar = manager.get_similar_workflow("test")
        assert len(similar) == 1
        applied = manager.apply_workflow("wf1", context={"foo": "bar"})
        assert applied[0]["foo"] == "bar"

def test_memory_reasoner():
    """Test searching, ranking, and injecting context from all memory types."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Episodic
        epi_path = os.path.join(tmpdir, "epi.jsonl")
        epi = EpisodicManager(log_path=epi_path)
        epi.log_session("s1", "foo", "bar", "good", {"test": True})
        
        # Semantic
        from vectordb import VectorDB
        db = VectorDB(db_path=tmpdir)
        db.create_collection("test")
        db.add_vectors("test", [{"embedding": [1.0, 0.0], "text": "cat"}])
        from kg import KnowledgeGraphManager
        kg = KnowledgeGraphManager(use_neo4j=False)
        sem = SemanticManager(vectordb=db, kg_manager=kg, collection_name="test", n_clusters=1)
        
        # Procedural
        proc_path = os.path.join(tmpdir, "proc.jsonl")
        proc = ProceduralManager(workflow_path=proc_path)
        proc.save_workflow("wf1", [{"name": "step1"}], description="foo")
        
        # Reasoner
        reasoner = MemoryReasoner(epi, sem, proc)
        results = reasoner.search_memory("foo", query_embedding=[1.0, 0.0], top_k=1)
        ranked = reasoner.rank_relevance(results, "foo", query_embedding=[1.0, 0.0])
        assert any(r["_memory_type"] == "semantic" for r in ranked)
        context = reasoner.inject_context({}, ranked, max_items=1)
        assert "injected_memories" in context

def test_memory_logger():
    """Test logging and hashability of memory operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = os.path.join(tmpdir, "memlog.jsonl")
        logger = MemoryLogger(log_path=log_path)
        h1 = logger.log("create", "episodic", {"foo": "bar"})
        h2 = logger.log("update", "semantic", {"bar": "baz"})
        assert isinstance(h1, str) and len(h1) == 64
        assert isinstance(h2, str) and len(h2) == 64 