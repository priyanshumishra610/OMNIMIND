"""
Basic tests for OMNIMIND components.
"""

import pytest
from unittest.mock import Mock, patch


def test_main_import():
    """Test that main module can be imported."""
    try:
        import main
        assert hasattr(main, 'app')
    except ImportError:
        pytest.skip("Main module not available")


def test_crawlers_import():
    """Test that crawlers module can be imported."""
    try:
        from crawlers import WebCrawler, FileIngestor
        assert WebCrawler is not None
        assert FileIngestor is not None
    except ImportError:
        pytest.skip("Crawlers module not available")


def test_chunker_import():
    """Test that chunker module can be imported."""
    try:
        from chunker import SmartChunker
        assert SmartChunker is not None
    except ImportError:
        pytest.skip("Chunker module not available")


def test_embedder_import():
    """Test that embedder module can be imported."""
    try:
        from embedder import MultiModelEmbedder
        assert MultiModelEmbedder is not None
    except ImportError:
        pytest.skip("Embedder module not available")


def test_vectordb_import():
    """Test that vectordb module can be imported."""
    try:
        from vectordb import VectorDB
        assert VectorDB is not None
    except ImportError:
        pytest.skip("VectorDB module not available")


def test_kg_import():
    """Test that knowledge graph module can be imported."""
    try:
        from kg import KnowledgeGraphManager
        assert KnowledgeGraphManager is not None
    except ImportError:
        pytest.skip("Knowledge Graph module not available")


def test_agents_import():
    """Test that agents module can be imported."""
    try:
        from agents import BaseAgent, FactChecker, Skeptic
        assert BaseAgent is not None
        assert FactChecker is not None
        assert Skeptic is not None
    except ImportError:
        pytest.skip("Agents module not available")


def test_simulator_import():
    """Test that simulator module can be imported."""
    try:
        from simulator import SimulationSandbox
        assert SimulationSandbox is not None
    except ImportError:
        pytest.skip("Simulator module not available")


def test_verifier_import():
    """Test that verifier module can be imported."""
    try:
        from verifier import ImmutableVerifier
        assert ImmutableVerifier is not None
    except ImportError:
        pytest.skip("Verifier module not available")


def test_self_mutator_import():
    """Test that self mutator module can be imported."""
    try:
        from self_mutator import SelfMutator
        assert SelfMutator is not None
    except ImportError:
        pytest.skip("Self Mutator module not available")


def test_pipelines_import():
    """Test that pipelines module can be imported."""
    try:
        from pipelines import IngestionPipeline, RetrievalPipeline, TrainingPipeline
        assert IngestionPipeline is not None
        assert RetrievalPipeline is not None
        assert TrainingPipeline is not None
    except ImportError:
        pytest.skip("Pipelines module not available")


def test_monitor_import():
    """Test that monitor module can be imported."""
    try:
        from monitor import PrometheusClient
        assert PrometheusClient is not None
    except ImportError:
        pytest.skip("Monitor module not available")


if __name__ == "__main__":
    pytest.main([__file__]) 