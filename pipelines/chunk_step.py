"""
Chunking Pipeline Step for OMNIMIND

Handles text chunking using the smart chunker.
"""

from typing import List, Dict, Any
import logging
from chunker.chunker import SmartChunker

logger = logging.getLogger(__name__)


def chunk_step(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Chunk documents into smaller pieces."""
    try:
        documents = input_data.get("documents", [])
        if not documents:
            logger.warning("No documents provided for chunking")
            return {"chunks": [], "error": "No documents provided"}
        
        # Get chunking parameters
        chunk_size = input_data.get("chunk_size", 1000)
        overlap = input_data.get("overlap", 200)
        language = input_data.get("language", "en")
        
        # Initialize chunker
        chunker = SmartChunker(
            chunk_size=chunk_size,
            overlap=overlap,
            language=language
        )
        
        # Chunk documents
        chunks = chunker.chunk_documents(documents)
        
        # Get chunk statistics
        chunk_stats = chunker.get_chunk_stats(chunks)
        
        # Log results
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        logger.info(f"Chunk stats: {chunk_stats}")
        
        return {
            "chunks": chunks,
            "chunk_stats": chunk_stats,
            "total_documents": len(documents),
            "total_chunks": len(chunks),
            "chunk_size": chunk_size,
            "overlap": overlap,
            "language": language
        }
        
    except Exception as e:
        logger.error(f"Error in chunk step: {e}")
        return {"error": str(e), "chunks": []} 