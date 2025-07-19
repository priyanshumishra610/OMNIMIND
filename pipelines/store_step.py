"""
Storage Pipeline Step for OMNIMIND

Handles storing embeddings in vector database and knowledge graph.
"""

from typing import List, Dict, Any
import logging
from vectordb.vectordb import VectorDB
from kg.kg_manager import KnowledgeGraphManager

logger = logging.getLogger(__name__)


def store_step(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Store embedded chunks in vector database and knowledge graph."""
    try:
        embedded_chunks = input_data.get("embedded_chunks", [])
        if not embedded_chunks:
            logger.warning("No embedded chunks provided for storage")
            return {"stored_count": 0, "error": "No embedded chunks provided"}
        
        # Get storage parameters
        collection_name = input_data.get("collection_name", "omnimind_docs")
        backend = input_data.get("backend", "simple")
        use_neo4j = input_data.get("use_neo4j", False)
        
        # Initialize vector database
        vectordb = VectorDB(backend=backend)
        
        # Initialize knowledge graph
        kg = KnowledgeGraphManager(use_neo4j=use_neo4j)
        
        # Store in vector database
        vector_success = vectordb.add_vectors(collection_name, embedded_chunks)
        
        # Store in knowledge graph
        kg_success = _store_in_kg(kg, embedded_chunks)
        
        # Get statistics
        vector_stats = vectordb.get_collection_stats(collection_name)
        kg_stats = kg.get_graph_stats()
        
        # Log results
        logger.info(f"Stored {len(embedded_chunks)} chunks in vector database")
        logger.info(f"Vector DB stats: {vector_stats}")
        logger.info(f"Knowledge Graph stats: {kg_stats}")
        
        return {
            "stored_count": len(embedded_chunks),
            "vector_success": vector_success,
            "kg_success": kg_success,
            "vector_stats": vector_stats,
            "kg_stats": kg_stats,
            "collection_name": collection_name,
            "backend": backend,
            "use_neo4j": use_neo4j
        }
        
    except Exception as e:
        logger.error(f"Error in store step: {e}")
        return {"error": str(e), "stored_count": 0}


def _store_in_kg(kg: KnowledgeGraphManager, embedded_chunks: List[Dict[str, Any]]) -> bool:
    """Store chunks in knowledge graph."""
    try:
        for chunk in embedded_chunks:
            # Add document entity
            doc_id = chunk.get("document_id", "unknown")
            kg.add_entity(
                entity_id=doc_id,
                entity_type="document",
                properties={
                    "title": chunk.get("document_title", ""),
                    "source": chunk.get("source", ""),
                    "content_type": chunk.get("document_type", "")
                }
            )
            
            # Add chunk entity
            chunk_id = chunk.get("chunk_id", "unknown")
            kg.add_entity(
                entity_id=chunk_id,
                entity_type="chunk",
                properties={
                    "text": chunk.get("text", "")[:100] + "...",  # Truncate for storage
                    "size": chunk.get("size", 0),
                    "embedding_model": chunk.get("embedding_model", "")
                }
            )
            
            # Add relationship between document and chunk
            kg.add_relationship(
                source_id=doc_id,
                target_id=chunk_id,
                relationship_type="contains",
                properties={"chunk_index": chunk.get("chunk_id", "")}
            )
        
        return True
    except Exception as e:
        logger.error(f"Error storing in knowledge graph: {e}")
        return False 