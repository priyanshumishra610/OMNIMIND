"""
Knowledge Graph API Route
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from kg.kg_manager import KnowledgeGraphManager

router = APIRouter()

class KGQueryRequest(BaseModel):
    """Knowledge graph query request model."""
    query: str
    limit: int = 10

class KGEntity(BaseModel):
    """Knowledge graph entity model."""
    id: str
    type: str
    name: str
    properties: Dict[str, Any] = {}

class KGRelationship(BaseModel):
    """Knowledge graph relationship model."""
    source: str
    target: str
    type: str
    properties: Dict[str, Any] = {}

class KGQueryResponse(BaseModel):
    """Knowledge graph query response model."""
    entities: List[KGEntity]
    relationships: List[KGRelationship]

def get_kg_manager():
    """Dependency to get KnowledgeGraphManager instance."""
    return KnowledgeGraphManager(use_neo4j=False)

@router.post("/kg/query", response_model=KGQueryResponse)
async def kg_query(
    request: KGQueryRequest,
    kg: KnowledgeGraphManager = Depends(get_kg_manager)
):
    """Knowledge graph query endpoint."""
    try:
        # Query knowledge graph
        results = kg.query(
            query=request.query,
            limit=request.limit
        )
        
        if not results or not isinstance(results, dict):
            return KGQueryResponse(entities=[], relationships=[])
        
        # Format entities
        entities = [
            KGEntity(
                id=entity.get("id", ""),
                type=entity.get("type", ""),
                name=entity.get("name", ""),
                properties=entity.get("properties", {})
            )
            for entity in results.get("entities", [])
        ]
        
        # Format relationships
        relationships = [
            KGRelationship(
                source=rel.get("source", ""),
                target=rel.get("target", ""),
                type=rel.get("type", ""),
                properties=rel.get("properties", {})
            )
            for rel in results.get("relationships", [])
        ]
        
        return KGQueryResponse(
            entities=entities,
            relationships=relationships
        )
    except Exception as e:
        # Log the error but return empty results instead of failing
        print(f"Knowledge graph query error: {str(e)}")
        return KGQueryResponse(entities=[], relationships=[]) 