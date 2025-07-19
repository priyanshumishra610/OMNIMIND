from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import os

# Import OMNIMIND components
from embedder.embedder import MultiModelEmbedder
from vectordb.vectordb import VectorDB
from kg.kg_manager import KnowledgeGraphManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OMNIMIND",
    description="The Autonomous, Self-Simulating, Self-Evolving Cognitive Kernel",
    version="0.1.0"
)

# Initialize components
embedder = MultiModelEmbedder()
vectordb = VectorDB()
kg = KnowledgeGraphManager(use_neo4j=False)  # Use simple storage for now

# Pydantic models
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    collection_name: str = "omnimind_docs"

class SearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    kg_context: List[Dict[str, Any]]
    total_results: int
    search_time_ms: float

@app.get("/")
def read_root():
    return {"message": "👋 Welcome to OMNIMIND — The Autonomous, Self-Evolving Cognitive Kernel."}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    try:
        # Basic health checks
        health_status = {
            "status": "healthy",
            "service": "OMNIMIND",
            "version": "0.1.0",
            "components": {
                "embedder": "available",
                "vectordb": "available",
                "knowledge_graph": "available"
            }
        }
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {e}")

@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    """Search endpoint that embeds query and retrieves top K matches with KG context."""
    import time
    start_time = time.time()
    
    try:
        # 1. Embed the query
        query_embedding = embedder.embed_text(request.query)
        
        # 2. Search vector database
        search_results = vectordb.search(
            collection_name=request.collection_name,
            query_vector=query_embedding,
            top_k=request.top_k
        )
        
        # 3. Expand with knowledge graph context
        kg_context = []
        for result in search_results:
            # Get related entities from KG
            doc_id = result.get("document_id", "")
            if doc_id:
                related_entities = kg.get_relationships(entity_id=doc_id)
                kg_context.extend(related_entities)
        
        # 4. Calculate search time
        search_time_ms = (time.time() - start_time) * 1000
        
        # 5. Prepare response
        response = SearchResponse(
            query=request.query,
            results=search_results,
            kg_context=kg_context,
            total_results=len(search_results),
            search_time_ms=search_time_ms
        )
        
        logger.info(f"Search completed: {len(search_results)} results in {search_time_ms:.2f}ms")
        return response
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

@app.get("/stats")
def get_stats():
    """Get system statistics."""
    try:
        # Get vector database stats
        vector_stats = vectordb.get_collection_stats("omnimind_docs")
        
        # Get knowledge graph stats
        kg_stats = kg.get_graph_stats()
        
        return {
            "vector_database": vector_stats,
            "knowledge_graph": kg_stats,
            "embedding_model": embedder._get_used_model()
        }
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {e}")

@app.post("/ingest")
def ingest_documents(sources: List[str]):
    """Ingest documents from sources."""
    try:
        from pipelines.pipeline import run_pipeline
        
        # Run the complete pipeline
        result = run_pipeline(sources)
        
        if result["pipeline_success"]:
            return {
                "success": True,
                "message": f"Ingested {len(sources)} sources successfully",
                "details": result["final_data"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Pipeline failed"))
            
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 