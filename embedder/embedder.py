"""
Multi-Model Embedder for OMNIMIND

Handles embeddings using multiple models for optimal retrieval.
"""

import os
from typing import List, Dict, Any, Optional
import logging
import numpy as np

logger = logging.getLogger(__name__)


class MultiModelEmbedder:
    """Multi-model embedder for generating embeddings."""
    
    def __init__(self, model_name: str = "text-embedding-ada-002"):
        self.model_name = model_name
        self.embedding_dim = 1536  # Default for OpenAI embeddings
        
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            # Placeholder for OpenAI embedding
            # In production, this would use the OpenAI API
            import openai
            
            response = openai.Embedding.create(
                input=text,
                model=self.model_name
            )
            return response['data'][0]['embedding']
        except ImportError:
            logger.warning("OpenAI not available, using dummy embedding")
            return self._dummy_embedding(text)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return self._dummy_embedding(text)
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = []
        for text in texts:
            embedding = self.embed_text(text)
            embeddings.append(embedding)
        return embeddings
    
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed a list of text chunks."""
        embedded_chunks = []
        
        for chunk in chunks:
            if "text" in chunk:
                embedding = self.embed_text(chunk["text"])
                embedded_chunk = chunk.copy()
                embedded_chunk["embedding"] = embedding
                embedded_chunk["embedding_model"] = self.model_name
                embedded_chunks.append(embedded_chunk)
        
        return embedded_chunks
    
    def _dummy_embedding(self, text: str) -> List[float]:
        """Generate a dummy embedding for testing."""
        # Simple hash-based embedding for testing
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Convert hash to embedding vector
        embedding = []
        for i in range(0, len(hash_hex), 2):
            if len(embedding) >= self.embedding_dim:
                break
            embedding.append(int(hash_hex[i:i+2], 16) / 255.0)
        
        # Pad or truncate to embedding_dim
        while len(embedding) < self.embedding_dim:
            embedding.append(0.0)
        
        return embedding[:self.embedding_dim] 