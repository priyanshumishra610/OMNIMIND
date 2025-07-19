"""
Vector Database for OMNIMIND

Handles vector storage and similarity search operations.
"""

import os
from typing import List, Dict, Any, Optional
import logging
import json

logger = logging.getLogger(__name__)


class VectorDB:
    """Vector database abstraction for storing and retrieving embeddings."""
    
    def __init__(self, db_path: str = "./data/vectordb"):
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
        self.collections = {}
    
    def create_collection(self, name: str, metadata: Dict[str, Any] = None) -> bool:
        """Create a new collection."""
        try:
            collection_path = os.path.join(self.db_path, name)
            os.makedirs(collection_path, exist_ok=True)
            
            self.collections[name] = {
                "path": collection_path,
                "metadata": metadata or {},
                "vectors": [],
                "documents": []
            }
            
            # Save collection metadata
            metadata_file = os.path.join(collection_path, "metadata.json")
            with open(metadata_file, 'w') as f:
                json.dump(self.collections[name], f, indent=2)
            
            logger.info(f"Created collection: {name}")
            return True
        except Exception as e:
            logger.error(f"Error creating collection {name}: {e}")
            return False
    
    def add_vectors(self, collection_name: str, vectors: List[Dict[str, Any]]) -> bool:
        """Add vectors to a collection."""
        try:
            if collection_name not in self.collections:
                self.create_collection(collection_name)
            
            collection = self.collections[collection_name]
            collection["vectors"].extend(vectors)
            collection["documents"].extend([v.get("text", "") for v in vectors])
            
            # Save vectors
            vectors_file = os.path.join(collection["path"], "vectors.json")
            with open(vectors_file, 'w') as f:
                json.dump(vectors, f, indent=2)
            
            logger.info(f"Added {len(vectors)} vectors to collection: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error adding vectors to {collection_name}: {e}")
            return False
    
    def search(self, collection_name: str, query_vector: List[float], 
               top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        try:
            if collection_name not in self.collections:
                logger.warning(f"Collection {collection_name} not found")
                return []
            
            collection = self.collections[collection_name]
            vectors = collection["vectors"]
            
            if not vectors:
                return []
            
            # Simple cosine similarity search
            similarities = []
            for i, vector_data in enumerate(vectors):
                if "embedding" in vector_data:
                    similarity = self._cosine_similarity(query_vector, vector_data["embedding"])
                    similarities.append((similarity, i, vector_data))
            
            # Sort by similarity and return top_k
            similarities.sort(key=lambda x: x[0], reverse=True)
            results = []
            
            for similarity, idx, vector_data in similarities[:top_k]:
                result = vector_data.copy()
                result["similarity"] = similarity
                result["rank"] = len(results) + 1
                results.append(result)
            
            return results
        except Exception as e:
            logger.error(f"Error searching collection {collection_name}: {e}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            import numpy as np
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except ImportError:
            # Fallback to pure Python implementation
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            norm1 = sum(a * a for a in vec1) ** 0.5
            norm2 = sum(b * b for b in vec2) ** 0.5
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics for a collection."""
        if collection_name not in self.collections:
            return {"error": "Collection not found"}
        
        collection = self.collections[collection_name]
        return {
            "name": collection_name,
            "vector_count": len(collection["vectors"]),
            "document_count": len(collection["documents"]),
            "metadata": collection["metadata"]
        } 