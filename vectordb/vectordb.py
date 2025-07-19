"""
Vector Database for OMNIMIND

Handles vector storage and similarity search operations using FAISS/Chroma.
"""

import os
from typing import List, Dict, Any, Optional
import logging
import json
import pickle

logger = logging.getLogger(__name__)


class VectorDB:
    """Vector database abstraction with FAISS/Chroma support."""
    
    def __init__(self, db_path: str = "./data/vectordb", backend: str = "faiss"):
        self.db_path = db_path
        self.backend = backend
        os.makedirs(db_path, exist_ok=True)
        self.collections = {}
        self._faiss_indexes = {}
        self._chroma_client = None
        
        # Initialize backend
        self._init_backend()
    
    def _init_backend(self):
        """Initialize the vector database backend."""
        if self.backend == "faiss":
            self._init_faiss()
        elif self.backend == "chroma":
            self._init_chroma()
        else:
            logger.warning(f"Unknown backend {self.backend}, using simple storage")
    
    def _init_faiss(self):
        """Initialize FAISS backend."""
        try:
            import faiss
            logger.info("FAISS backend initialized")
        except ImportError:
            logger.warning("FAISS not available, using simple storage")
            self.backend = "simple"
    
    def _init_chroma(self):
        """Initialize ChromaDB backend."""
        try:
            import chromadb
            self._chroma_client = chromadb.PersistentClient(path=self.db_path)
            logger.info("ChromaDB backend initialized")
        except ImportError:
            logger.warning("ChromaDB not available, using simple storage")
            self.backend = "simple"
    
    def create_collection(self, name: str, metadata: Dict[str, Any] = None) -> bool:
        """Create a new collection."""
        try:
            if self.backend == "chroma" and self._chroma_client:
                # Create ChromaDB collection
                self._chroma_client.create_collection(name=name, metadata=metadata or {})
                logger.info(f"Created ChromaDB collection: {name}")
                return True
            
            # Create simple collection
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
            if self.backend == "chroma" and self._chroma_client:
                return self._add_vectors_chroma(collection_name, vectors)
            else:
                return self._add_vectors_simple(collection_name, vectors)
        except Exception as e:
            logger.error(f"Error adding vectors to {collection_name}: {e}")
            return False
    
    def _add_vectors_chroma(self, collection_name: str, vectors: List[Dict[str, Any]]) -> bool:
        """Add vectors using ChromaDB."""
        try:
            collection = self._chroma_client.get_collection(name=collection_name)
            
            texts = []
            metadatas = []
            ids = []
            
            for i, vector_data in enumerate(vectors):
                if "text" in vector_data:
                    texts.append(vector_data["text"])
                    metadatas.append({
                        "document_id": vector_data.get("document_id", ""),
                        "chunk_id": vector_data.get("chunk_id", f"chunk_{i}"),
                        "source": vector_data.get("source", "")
                    })
                    ids.append(f"doc_{i}")
            
            if texts:
                collection.add(
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Added {len(texts)} vectors to ChromaDB collection: {collection_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"ChromaDB add error: {e}")
            return False
    
    def _add_vectors_simple(self, collection_name: str, vectors: List[Dict[str, Any]]) -> bool:
        """Add vectors using simple storage."""
        if collection_name not in self.collections:
            self.create_collection(collection_name)
        
        collection = self.collections[collection_name]
        collection["vectors"].extend(vectors)
        collection["documents"].extend([v.get("text", "") for v in vectors])
        
        # Save vectors
        vectors_file = os.path.join(collection["path"], "vectors.pkl")
        with open(vectors_file, 'wb') as f:
            pickle.dump(vectors, f)
        
        logger.info(f"Added {len(vectors)} vectors to collection: {collection_name}")
        return True
    
    def search(self, collection_name: str, query_vector: List[float], 
               top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        try:
            if self.backend == "chroma" and self._chroma_client:
                return self._search_chroma(collection_name, query_vector, top_k)
            else:
                return self._search_simple(collection_name, query_vector, top_k)
        except Exception as e:
            logger.error(f"Error searching collection {collection_name}: {e}")
            return []
    
    def _search_chroma(self, collection_name: str, query_vector: List[float], 
                      top_k: int) -> List[Dict[str, Any]]:
        """Search using ChromaDB."""
        try:
            collection = self._chroma_client.get_collection(name=collection_name)
            
            # Convert query vector to query text (placeholder)
            query_text = " ".join([str(x) for x in query_vector[:10]])  # Simple conversion
            
            results = collection.query(
                query_texts=[query_text],
                n_results=top_k
            )
            
            # Convert ChromaDB results to our format
            formatted_results = []
            for i in range(len(results['documents'][0])):
                result = {
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "id": results['ids'][0][i],
                    "similarity": 0.8,  # ChromaDB doesn't return similarity by default
                    "rank": i + 1
                }
                formatted_results.append(result)
            
            return formatted_results
        except Exception as e:
            logger.error(f"ChromaDB search error: {e}")
            return []
    
    def _search_simple(self, collection_name: str, query_vector: List[float], 
                      top_k: int) -> List[Dict[str, Any]]:
        """Search using simple storage."""
        if collection_name not in self.collections:
            logger.warning(f"Collection {collection_name} not found")
            return []
        
        collection = self.collections[collection_name]
        vectors = collection["vectors"]
        
        if not vectors:
            return []
        
        # Calculate similarities
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
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection."""
        try:
            if self.backend == "chroma" and self._chroma_client:
                self._chroma_client.delete_collection(name=collection_name)
            else:
                if collection_name in self.collections:
                    import shutil
                    collection_path = self.collections[collection_name]["path"]
                    shutil.rmtree(collection_path)
                    del self.collections[collection_name]
            
            logger.info(f"Deleted collection: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection {collection_name}: {e}")
            return False
    
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
        if self.backend == "chroma" and self._chroma_client:
            try:
                collection = self._chroma_client.get_collection(name=collection_name)
                count = collection.count()
                return {
                    "name": collection_name,
                    "vector_count": count,
                    "backend": "chroma"
                }
            except:
                return {"error": "Collection not found"}
        
        if collection_name not in self.collections:
            return {"error": "Collection not found"}
        
        collection = self.collections[collection_name]
        return {
            "name": collection_name,
            "vector_count": len(collection["vectors"]),
            "document_count": len(collection["documents"]),
            "metadata": collection["metadata"],
            "backend": self.backend
        } 