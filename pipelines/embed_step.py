"""
Embedding Pipeline Step for OMNIMIND

Handles text embedding using the multi-model embedder.
"""

from typing import List, Dict, Any
import logging
from embedder.embedder import MultiModelEmbedder

logger = logging.getLogger(__name__)


def embed_step(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Embed chunks into vector representations."""
    try:
        chunks = input_data.get("chunks", [])
        if not chunks:
            logger.warning("No chunks provided for embedding")
            return {"embedded_chunks": [], "error": "No chunks provided"}
        
        # Get embedding parameters
        model_name = input_data.get("model_name", "text-embedding-ada-002")
        fallback_model = input_data.get("fallback_model", "all-MiniLM-L6-v2")
        
        # Initialize embedder
        embedder = MultiModelEmbedder(
            model_name=model_name,
            fallback_model=fallback_model
        )
        
        # Embed chunks
        embedded_chunks = embedder.embed_chunks(chunks)
        
        # Get embedding statistics
        embeddings = [chunk.get("embedding", []) for chunk in embedded_chunks if chunk.get("embedding")]
        embed_stats = embedder.get_embedding_stats(embeddings)
        
        # Log results
        logger.info(f"Embedded {len(embedded_chunks)} chunks")
        logger.info(f"Embedding stats: {embed_stats}")
        
        return {
            "embedded_chunks": embedded_chunks,
            "embedding_stats": embed_stats,
            "total_chunks": len(chunks),
            "embedded_count": len(embedded_chunks),
            "model_used": embed_stats.get("model_used", "unknown"),
            "embedding_dim": embed_stats.get("embedding_dim", 0)
        }
        
    except Exception as e:
        logger.error(f"Error in embed step: {e}")
        return {"error": str(e), "embedded_chunks": []} 