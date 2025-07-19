#!/usr/bin/env python3
"""
OMNIMIND Test Runner

Simple script to test basic OMNIMIND functionality.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("🧬 Testing OMNIMIND imports...")
    
    try:
        # Test main module
        import main
        print("✅ Main module imported successfully")
        
        # Test crawlers
        from crawlers import WebCrawler, FileIngestor
        print("✅ Crawlers module imported successfully")
        
        # Test chunker
        from chunker import SmartChunker
        print("✅ Chunker module imported successfully")
        
        # Test embedder
        from embedder import MultiModelEmbedder
        print("✅ Embedder module imported successfully")
        
        # Test vectordb
        from vectordb import VectorDB
        print("✅ VectorDB module imported successfully")
        
        # Test knowledge graph
        from kg import KnowledgeGraphManager
        print("✅ Knowledge Graph module imported successfully")
        
        # Test agents
        from agents import BaseAgent, FactChecker, Skeptic
        print("✅ Agents module imported successfully")
        
        # Test simulator
        from simulator import SimulationSandbox
        print("✅ Simulator module imported successfully")
        
        # Test verifier
        from verifier import ImmutableVerifier
        print("✅ Verifier module imported successfully")
        
        # Test self mutator
        from self_mutator import SelfMutator
        print("✅ Self Mutator module imported successfully")
        
        # Test pipelines
        from pipelines import IngestionPipeline, RetrievalPipeline, TrainingPipeline
        print("✅ Pipelines module imported successfully")
        
        # Test monitor
        from monitor import PrometheusClient
        print("✅ Monitor module imported successfully")
        
        print("\n🎉 All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of OMNIMIND components."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test chunker
        from chunker import SmartChunker
        chunker = SmartChunker()
        text = "This is a test document for OMNIMIND. It contains multiple sentences. We will chunk this text."
        chunks = chunker.chunk_text(text)
        print(f"✅ Chunker: Created {len(chunks)} chunks")
        
        # Test embedder
        from embedder import MultiModelEmbedder
        embedder = MultiModelEmbedder()
        embedding = embedder.embed_text("Test text for embedding")
        print(f"✅ Embedder: Generated embedding of length {len(embedding)}")
        
        # Test vectordb
        from vectordb import VectorDB
        vectordb = VectorDB()
        success = vectordb.create_collection("test_collection")
        print(f"✅ VectorDB: Collection creation {'successful' if success else 'failed'}")
        
        # Test knowledge graph
        from kg import KnowledgeGraphManager
        kg = KnowledgeGraphManager()
        success = kg.add_entity("test_entity", "test_type", {"name": "Test"})
        print(f"✅ Knowledge Graph: Entity addition {'successful' if success else 'failed'}")
        
        # Test agents
        from agents import FactChecker, Skeptic
        fact_checker = FactChecker()
        skeptic = Skeptic()
        print(f"✅ Agents: Created {fact_checker.name} and {skeptic.name}")
        
        # Test simulator
        from simulator import SimulationSandbox
        simulator = SimulationSandbox()
        print(f"✅ Simulator: Created {simulator.sandbox_name}")
        
        # Test verifier
        from verifier import ImmutableVerifier
        verifier = ImmutableVerifier()
        proof = verifier.create_proof({"test": "data"})
        print(f"✅ Verifier: Created proof {proof.get('proof_id', 'unknown')}")
        
        # Test self mutator
        from self_mutator import SelfMutator
        mutator = SelfMutator()
        print(f"✅ Self Mutator: Created with population size {mutator.population_size}")
        
        # Test monitor
        from monitor import PrometheusClient
        monitor = PrometheusClient()
        monitor.record_metric("test_metric", 42.0)
        print("✅ Monitor: Recorded test metric")
        
        print("\n🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def main():
    """Main test function."""
    print("🧬 OMNIMIND Test Suite")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 OMNIMIND is ready to evolve!")
            print("\nNext steps:")
            print("1. Install dependencies: pip install -r requirements.txt")
            print("2. Set up environment: cp env.example .env")
            print("3. Run FastAPI: python main.py")
            print("4. Run dashboard: streamlit run dashboard/app.py")
        else:
            print("\n❌ Functionality tests failed")
            sys.exit(1)
    else:
        print("\n❌ Import tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 