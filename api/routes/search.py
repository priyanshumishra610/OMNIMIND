"""
Vector Search API Route
"""
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from vectordb.vectordb import VectorDB
from embedder.embedder import MultiModelEmbedder

router = APIRouter()

class SearchRequest(BaseModel):
    """Search request model."""
    query: str
    collection: str
    top_k: int = 10

class SearchResult(BaseModel):
    """Search result model."""
    id: str
    text: str
    score: float

class SearchResponse(BaseModel):
    """Search response model."""
    results: List[SearchResult]

def get_vectordb():
    """Dependency to get VectorDB instance."""
    return VectorDB()

def get_embedder():
    """Dependency to get MultiModelEmbedder instance."""
    return MultiModelEmbedder()

@router.post("/search", response_model=SearchResponse)
async def vector_search(
    request: SearchRequest,
    vectordb: VectorDB = Depends(get_vectordb),
    embedder: MultiModelEmbedder = Depends(get_embedder)
):
    """Vector search endpoint."""
    try:
        # Get query embedding
        query_embedding = embedder.embed_text(request.query)
        
        # Search vectors
        results = vectordb.search(
            request.collection,
            query_embedding,
            top_k=request.top_k
        )
        
        # Format results
        search_results = [
            SearchResult(
                id=str(result.get("id", "")),
                text=str(result.get("text", "")),
                score=float(result.get("similarity", 0.0))  # Changed from score to similarity
            )
            for result in (results or [])  # Handle None results
        ]
        
        return SearchResponse(results=search_results)
    except Exception as e:
        # Log the error but return empty results instead of failing
        print(f"Search error: {str(e)}")
        return SearchResponse(results=[]) 