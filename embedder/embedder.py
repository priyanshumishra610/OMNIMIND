"""
Multi-Model Embedder for OMNIMIND

Handles embeddings using OpenAI + sentence-transformers fallback.
"""

import os
from typing import List, Dict, Any, Optional
import logging
import numpy as np

logger = logging.getLogger(__name__)


class MultiModelEmbedder:
    """Multi-model embedder with OpenAI + sentence-transformers fallback."""
    
    def __init__(self, model_name: str = "text-embedding-ada-002", 
                 fallback_model: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.fallback_model = fallback_model
        self.embedding_dim = 1536  # Default for OpenAI embeddings
        self._openai_client = None
        self._sentence_transformer = None
        
        # Initialize OpenAI client
        self._init_openai()
        
        # Initialize fallback model
        self._init_fallback()
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai.api_key = api_key
                self._openai_client = openai
                logger.info("OpenAI client initialized successfully")
            else:
                logger.warning("OPENAI_API_KEY not found in environment")
        except ImportError:
            logger.warning("OpenAI package not installed")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
    
    def _init_fallback(self):
        """Initialize sentence-transformers fallback."""
        try:
            from sentence_transformers import SentenceTransformer
            self._sentence_transformer = SentenceTransformer(self.fallback_model)
            logger.info(f"Fallback model {self.fallback_model} initialized")
        except ImportError:
            logger.warning("sentence-transformers not installed")
        except Exception as e:
            logger.error(f"Failed to initialize fallback model: {e}")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        if not text or not text.strip():
            return self._zero_embedding()
        
        # Try OpenAI first
        if self._openai_client:
            try:
                response = self._openai_client.Embedding.create(
                    input=text,
                    model=self.model_name
                )
                embedding = response['data'][0]['embedding']
                logger.debug(f"Generated OpenAI embedding for text of length {len(text)}")
                return embedding
            except Exception as e:
                logger.warning(f"OpenAI embedding failed: {e}")
        
        # Fallback to sentence-transformers
        if self._sentence_transformer:
            try:
                embedding = self._sentence_transformer.encode(text).tolist()
                logger.debug(f"Generated fallback embedding for text of length {len(text)}")
                return embedding
            except Exception as e:
                logger.warning(f"Fallback embedding failed: {e}")
        
        # Last resort: dummy embedding
        logger.warning("Using dummy embedding as last resort")
        return self._dummy_embedding(text)
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = []
        for i, text in enumerate(texts):
            embedding = self.embed_text(text)
            embeddings.append(embedding)
            if (i + 1) % 100 == 0:
                logger.info(f"Processed {i + 1}/{len(texts)} texts")
        return embeddings
    
    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed a list of text chunks."""
        embedded_chunks = []
        
        for i, chunk in enumerate(chunks):
            if "text" in chunk and chunk["text"]:
                embedding = self.embed_text(chunk["text"])
                embedded_chunk = chunk.copy()
                embedded_chunk["embedding"] = embedding
                embedded_chunk["embedding_model"] = self._get_used_model()
                embedded_chunk["embedding_dim"] = len(embedding)
                embedded_chunks.append(embedded_chunk)
                
                if (i + 1) % 50 == 0:
                    logger.info(f"Embedded {i + 1}/{len(chunks)} chunks")
        
        return embedded_chunks
    
    def _get_used_model(self) -> str:
        """Get the model that was actually used for embedding."""
        if self._openai_client:
            return self.model_name
        elif self._sentence_transformer:
            return self.fallback_model
        else:
            return "dummy"
    
    def _zero_embedding(self) -> List[float]:
        """Return zero embedding for empty text."""
        return [0.0] * self.embedding_dim
    
    def _dummy_embedding(self, text: str) -> List[float]:
        """Generate a dummy embedding for testing."""
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
    
    def get_embedding_stats(self, embeddings: List[List[float]]) -> Dict[str, Any]:
        """Get statistics about embeddings."""
        if not embeddings:
            return {"total_embeddings": 0, "embedding_dim": 0}
        
        embedding_dim = len(embeddings[0]) if embeddings else 0
        total_embeddings = len(embeddings)
        
        return {
            "total_embeddings": total_embeddings,
            "embedding_dim": embedding_dim,
            "model_used": self._get_used_model()
        } 