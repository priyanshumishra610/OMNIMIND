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
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200, language: str = "en"):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.language = language
        
        # Language-specific sentence patterns
        self.sentence_patterns = {
            "en": r'(?<=[.!?])\s+',
            "es": r'(?<=[.!?])\s+',
            "fr": r'(?<=[.!?])\s+',
            "de": r'(?<=[.!?])\s+',
            "zh": r'(?<=[。！？])\s*',
            "ja": r'(?<=[。！？])\s*',
        }
    
    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Chunk text while preserving semantic boundaries."""
        if not text or len(text.strip()) == 0:
            return []
        
        if len(text) <= self.chunk_size:
            return [{
                "text": text.strip(),
                "start": 0,
                "end": len(text),
                "chunk_id": "chunk_0"
            }]
        
        chunks = []
        sentences = self._split_sentences(text)
        current_chunk = ""
        start_pos = 0
        chunk_id = 0
        
        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) + 1 <= self.chunk_size:
                current_chunk += sentence + " "
            else:
                # Save current chunk if it has content
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "start": start_pos,
                        "end": start_pos + len(current_chunk),
                        "chunk_id": f"chunk_{chunk_id}",
                        "size": len(current_chunk.strip())
                    })
                    chunk_id += 1
                
                # Start new chunk with overlap
                current_chunk = sentence + " "
                start_pos = max(0, start_pos + len(current_chunk) - self.overlap)
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "start": start_pos,
                "end": len(text),
                "chunk_id": f"chunk_{chunk_id}",
                "size": len(current_chunk.strip())
            })
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences while preserving structure."""
        pattern = self.sentence_patterns.get(self.language, self.sentence_patterns["en"])
        
        # Split by sentence boundaries
        sentences = re.split(pattern, text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # Minimum sentence length
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunk a list of documents."""
        all_chunks = []
        
        for doc in documents:
            if "content" in doc and doc["content"]:
                chunks = self.chunk_text(doc["content"])
                for chunk in chunks:
                    chunk.update({
                        "document_id": doc.get("id", doc.get("source", "unknown")),
                        "document_title": doc.get("title", ""),
                        "document_type": doc.get("content_type", "unknown"),
                        "source": doc.get("source", "")
                    })
                all_chunks.extend(chunks)
        
        return all_chunks
    
    def get_chunk_stats(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about chunks."""
        if not chunks:
            return {"total_chunks": 0, "avg_size": 0, "total_text": 0}
        
        total_chunks = len(chunks)
        total_text = sum(len(chunk.get("text", "")) for chunk in chunks)
        avg_size = total_text / total_chunks if total_chunks > 0 else 0
        
        return {
            "total_chunks": total_chunks,
            "avg_size": avg_size,
            "total_text": total_text,
            "min_size": min(len(chunk.get("text", "")) for chunk in chunks),
            "max_size": max(len(chunk.get("text", "")) for chunk in chunks)
        } 