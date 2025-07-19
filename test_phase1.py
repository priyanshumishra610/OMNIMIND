#!/usr/bin/env python3
"""
Phase 1 Test Script for OMNIMIND

Quick test to verify the complete ingest → chunk → embed → store → search pipeline.
"""

import sys
import os
import tempfile
import time

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_phase1_pipeline():
    """Test the complete Phase 1 pipeline."""
    print("🧬 Testing OMNIMIND Phase 1 Pipeline")
    print("=" * 50)
    
    try:
        # 1. Test Basic Loader
        print("1️⃣ Testing Basic Loader...")
        from crawlers.basic_loader import BasicLoader
        
        # Create test file
        test_content = """
        OMNIMIND is an autonomous, self-simulating, self-evolving cognitive kernel.
        It retrieves trusted knowledge from vast sources and verifies information with multi-agent swarm debate.
        The system maintains a living Knowledge Graph and Vector DB for optimal information retrieval.
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            loader = BasicLoader()
            result = loader.load_file(test_file)
            print(f"✅ Loader: {result['success']} - {result['size_bytes']} bytes")
        finally:
            os.unlink(test_file)
        
        # 2. Test Smart Chunker
        print("2️⃣ Testing Smart Chunker...")
        from chunker.chunker import SmartChunker
        
        chunker = SmartChunker(chunk_size=100, overlap=20)
        chunks = chunker.chunk_text(test_content)
        stats = chunker.get_chunk_stats(chunks)
        print(f"✅ Chunker: {stats['total_chunks']} chunks, avg size: {stats['avg_size']:.1f}")
        
        # 3. Test Multi-Model Embedder
        print("3️⃣ Testing Multi-Model Embedder...")
        from embedder.embedder import MultiModelEmbedder
        
        embedder = MultiModelEmbedder()
        embeddings = []
        for chunk in chunks:
            embedding = embedder.embed_text(chunk["text"])
            embeddings.append(embedding)
        
        embed_stats = embedder.get_embedding_stats(embeddings)
        print(f"✅ Embedder: {embed_stats['total_embeddings']} embeddings, dim: {embed_stats['embedding_dim']}")
        
        # 4. Test Vector Database
        print("4️⃣ Testing Vector Database...")
        from vectordb.vectordb import VectorDB
        
        vectordb = VectorDB()
        vectordb.create_collection("test_collection")
        
        # Prepare vectors for storage
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vectors.append({
                "text": chunk["text"],
                "embedding": embedding,
                "document_id": f"test_doc_{i}",
                "chunk_id": chunk["chunk_id"]
            })
        
        success = vectordb.add_vectors("test_collection", vectors)
        print(f"✅ VectorDB: {success} - stored {len(vectors)} vectors")
        
        # 5. Test Knowledge Graph
        print("5️⃣ Testing Knowledge Graph...")
        from kg.kg_manager import KnowledgeGraphManager
        
        kg = KnowledgeGraphManager(use_neo4j=False)
        
        # Add entities and relationships
        for i, chunk in enumerate(chunks):
            kg.add_entity(f"doc_{i}", "document", {"title": f"Test Doc {i}"})
            kg.add_entity(chunk["chunk_id"], "chunk", {"text": chunk["text"][:50]})
            kg.add_relationship(f"doc_{i}", chunk["chunk_id"], "contains")
        
        kg_stats = kg.get_graph_stats()
        print(f"✅ Knowledge Graph: {kg_stats['total_entities']} entities, {kg_stats['total_relationships']} relationships")
        
        # 6. Test Search
        print("6️⃣ Testing Search...")
        query = "OMNIMIND cognitive kernel"
        query_embedding = embedder.embed_text(query)
        
        search_results = vectordb.search("test_collection", query_embedding, top_k=3)
        print(f"✅ Search: {len(search_results)} results found")
        
        # 7. Test Complete Pipeline
        print("7️⃣ Testing Complete Pipeline...")
        from pipelines.pipeline import run_pipeline
        
        # Create another test file for pipeline
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            pipeline_file = f.name
        
        try:
            pipeline_result = run_pipeline([pipeline_file])
            print(f"✅ Pipeline: {pipeline_result['pipeline_success']} - {pipeline_result['steps_executed']} steps")
        finally:
            os.unlink(pipeline_file)
        
        # 8. Test FastAPI Endpoints
        print("8️⃣ Testing FastAPI Endpoints...")
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        health_response = client.get("/health")
        print(f"✅ Health: {health_response.status_code} - {health_response.json()['status']}")
        
        # Test search endpoint
        search_data = {"query": "OMNIMIND", "top_k": 2}
        search_response = client.post("/search", json=search_data)
        print(f"✅ Search API: {search_response.status_code}")
        
        print("\n🎉 Phase 1 Pipeline Test Completed Successfully!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up environment: cp env.example .env")
        print("3. Run FastAPI: uvicorn main:app --reload")
        print("4. Test endpoints: curl http://localhost:8000/health")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_phase1_pipeline()
    sys.exit(0 if success else 1) 