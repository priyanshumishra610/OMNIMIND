"""
Smart Chunker for OMNIMIND

Handles intelligent text chunking for optimal embedding and retrieval.
"""

import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class SmartChunker:
    """Intelligent text chunker that preserves semantic boundaries."""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Chunk text while preserving semantic boundaries."""
        if not text or len(text) <= self.chunk_size:
            return [{"text": text, "start": 0, "end": len(text)}]
        
        chunks = []
        sentences = self._split_sentences(text)
        current_chunk = ""
        start_pos = 0
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += sentence
            else:
                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "start": start_pos,
                        "end": start_pos + len(current_chunk)
                    })
                
                # Start new chunk with overlap
                current_chunk = sentence
                start_pos = len(text) - len(current_chunk) - self.overlap
        
        # Add the last chunk
        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "start": start_pos,
                "end": len(text)
            })
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences while preserving structure."""
        # Simple sentence splitting - can be enhanced with NLP libraries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunk a list of documents."""
        all_chunks = []
        
        for doc in documents:
            if "content" in doc:
                chunks = self.chunk_text(doc["content"])
                for chunk in chunks:
                    chunk.update({
                        "document_id": doc.get("id", doc.get("url", "unknown")),
                        "document_title": doc.get("title", ""),
                        "document_type": doc.get("type", "unknown")
                    })
                all_chunks.extend(chunks)
        
        return all_chunks 