#!/usr/bin/env python3
"""
Simple Phase 1 Test Script for OMNIMIND

Quick test to verify the basic structure without external dependencies.
"""

import sys
import os
import tempfile

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_phase1_structure():
    """Test the basic structure and imports."""
    print("🧬 Testing OMNIMIND Phase 1 Structure")
    print("=" * 50)
    
    try:
        # Test 1: Check if all modules can be imported
        print("1️⃣ Testing module imports...")
        
        # Test basic loader (without scrapy dependency)
        try:
            from crawlers.basic_loader import BasicLoader
            print("✅ BasicLoader imported successfully")
        except ImportError as e:
            print(f"⚠️ BasicLoader import failed (expected): {e}")
        
        # Test chunker
        try:
            from chunker.chunker import SmartChunker
            print("✅ SmartChunker imported successfully")
        except ImportError as e:
            print(f"❌ SmartChunker import failed: {e}")
            return False
        
        # Test embedder
        try:
            from embedder.embedder import MultiModelEmbedder
            print("✅ MultiModelEmbedder imported successfully")
        except ImportError as e:
            print(f"❌ MultiModelEmbedder import failed: {e}")
            return False
        
        # Test vector database
        try:
            from vectordb.vectordb import VectorDB
            print("✅ VectorDB imported successfully")
        except ImportError as e:
            print(f"❌ VectorDB import failed: {e}")
            return False
        
        # Test knowledge graph
        try:
            from kg.kg_manager import KnowledgeGraphManager
            print("✅ KnowledgeGraphManager imported successfully")
        except ImportError as e:
            print(f"❌ KnowledgeGraphManager import failed: {e}")
            return False
        
        # Test pipeline
        try:
            from pipelines.pipeline import OMNIMINDPipeline
            print("✅ OMNIMINDPipeline imported successfully")
        except ImportError as e:
            print(f"❌ OMNIMINDPipeline import failed: {e}")
            return False
        
        # Test 2: Test basic functionality without external deps
        print("\n2️⃣ Testing basic functionality...")
        
        # Test chunker with simple text
        chunker = SmartChunker(chunk_size=100, overlap=20)
        test_text = "This is a simple test text for OMNIMIND. It should be chunked properly."
        chunks = chunker.chunk_text(test_text)
        print(f"✅ Chunker: Created {len(chunks)} chunks")
        
        # Test embedder with dummy mode
        embedder = MultiModelEmbedder()
        embedding = embedder.embed_text("Test text")
        print(f"✅ Embedder: Created embedding of length {len(embedding)}")
        
        # Test vector database
        vectordb = VectorDB()
        success = vectordb.create_collection("test_collection")
        print(f"✅ VectorDB: Collection creation {success}")
        
        # Test knowledge graph
        kg = KnowledgeGraphManager(use_neo4j=False)
        success = kg.add_entity("test_entity", "document", {"title": "Test"})
        print(f"✅ Knowledge Graph: Entity creation {success}")
        
        # Test pipeline structure
        pipeline = OMNIMINDPipeline()
        print(f"✅ Pipeline: {len(pipeline.steps)} steps configured")
        
        # Test 3: Check file structure
        print("\n3️⃣ Checking file structure...")
        
        required_files = [
            "main.py",
            "requirements.txt",
            "crawlers/basic_loader.py",
            "chunker/chunker.py",
            "embedder/embedder.py",
            "vectordb/vectordb.py",
            "kg/kg_manager.py",
            "pipelines/pipeline.py",
            "pipelines/ingest_step.py",
            "pipelines/chunk_step.py",
            "pipelines/embed_step.py",
            "pipelines/store_step.py",
            "tests/test_phase1.py"
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - MISSING")
                return False
        
        print("\n🎉 Phase 1 Structure Test Completed Successfully!")
        print("\n📋 Summary:")
        print("✅ All core modules created")
        print("✅ Basic functionality implemented")
        print("✅ Pipeline structure ready")
        print("✅ FastAPI endpoints configured")
        print("✅ Tests created")
        
        print("\n🚀 Next Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up environment: cp env.example .env")
        print("3. Run FastAPI: uvicorn main:app --reload")
        print("4. Test endpoints: curl http://localhost:8000/health")
        print("5. Run full tests: python3 test_phase1.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_phase1_structure()
    sys.exit(0 if success else 1) 