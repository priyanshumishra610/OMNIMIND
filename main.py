from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import os

# Import OMNIMIND components
from embedder.embedder import MultiModelEmbedder
from vectordb.vectordb import VectorDB
from kg.kg_manager import KnowledgeGraphManager
from memory.episodic_manager import EpisodicManager
from memory.semantic_manager import SemanticManager
from memory.procedural_manager import ProceduralManager
from reasoners.memory_reasoner import MemoryReasoner
from logger.memory_logger import MemoryLogger
from supervisor.supervisor_core import SupervisorCore

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

# Initialize memory components
episodic_manager = EpisodicManager()
semantic_manager = SemanticManager(vectordb=vectordb, kg_manager=kg)
procedural_manager = ProceduralManager()
memory_reasoner = MemoryReasoner(episodic_manager, semantic_manager, procedural_manager)
memory_logger = MemoryLogger()

# Supervisor Core instance
supervisor_core = SupervisorCore()

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

class MemoryReasonRequest(BaseModel):
    query: str
    top_k: int = 5
    use_semantic: bool = True
    use_episodic: bool = True
    use_procedural: bool = True

class SupervisorControlRequest(BaseModel):
    command: str
    params: Optional[Dict[str, Any]] = None

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
    """Search endpoint that embeds query and retrieves top K matches with KG context. Logs query as episode."""
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
            doc_id = result.get("document_id", "")
            if doc_id:
                related_entities = kg.get_relationships(entity_id=doc_id)
                kg_context.extend(related_entities)
        # 4. Calculate search time
        search_time_ms = (time.time() - start_time) * 1000
        # 5. Log as episode
        episodic_manager.log_session(
            session_id="search",
            user_query=request.query,
            agent_thoughts=f"Search results: {len(search_results)}",
            feedback=None,
            extra={"kg_context": kg_context}
        )
        memory_logger.log("create", "episodic", {
            "query": request.query,
            "results": search_results
        })
        # 6. Prepare response
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

@app.get("/memory/inspect")
def memory_inspect():
    """Returns a summary of episodic, semantic, and procedural memory for dashboard visualization."""
    try:
        episodic = episodic_manager.retrieve_sessions(limit=10)
        semantic_labels = semantic_manager.cluster_vectors()
        procedural = procedural_manager._load_workflows()[:5]
        return {
            "episodic": episodic,
            "semantic_clusters": list(set(semantic_labels)) if semantic_labels else [],
            "procedural": procedural
        }
    except Exception as e:
        logger.error(f"Memory inspect failed: {e}")
        raise HTTPException(status_code=500, detail=f"Memory inspect failed: {e}")

@app.get("/memory/episodic")
def memory_episodic():
    """List all episodic memory episodes."""
    return episodic_manager.retrieve_sessions(limit=100)

@app.get("/memory/semantic")
def memory_semantic():
    """List all semantic clusters and their KG links."""
    labels = semantic_manager.cluster_vectors()
    return {
        "clusters": list(set(labels)) if labels else [],
        "cluster_to_kg": semantic_manager.cluster_to_kg
    }

@app.get("/memory/procedural")
def memory_procedural():
    """List all procedural workflows."""
    return procedural_manager._load_workflows()

@app.post("/memory/reason")
def memory_reason(request: MemoryReasonRequest):
    """Run the memory reasoner and return ranked relevant memories."""
    query_embedding = embedder.embed_text(request.query) if request.use_semantic else None
    results = memory_reasoner.search_memory(
        query=request.query,
        query_embedding=query_embedding,
        top_k=request.top_k
    )
    ranked = memory_reasoner.rank_relevance(results, request.query, query_embedding=query_embedding)
    memory_logger.log("create", "reasoner", {"query": request.query, "ranked": ranked})
    return {"ranked": ranked}

@app.get("/supervisor/status")
def supervisor_status():
    """Return live system state from Supervisor Core."""
    return supervisor_core.get_status()

@app.post("/supervisor/control")
def supervisor_control(request: SupervisorControlRequest):
    """Control tasks: pause, resume, reroute, or kill via Supervisor Core."""
    return supervisor_core.control(request.command, request.params)

@app.get("/supervisor/metrics")
def supervisor_metrics():
    """Return Supervisor Core health and performance metrics."""
    return supervisor_core.get_metrics()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 