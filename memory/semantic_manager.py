import os
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.cluster import KMeans
from vectordb import VectorDB
from kg import KnowledgeGraphManager

class SemanticManager:
    """
    Manages semantic memory: clusters embeddings, links clusters to KG, and performs semantic search.
    Configurable via environment variables. Modular for pipeline integration.
    """
    def __init__(self,
                 vectordb: Optional[VectorDB] = None,
                 kg_manager: Optional[KnowledgeGraphManager] = None,
                 collection_name: Optional[str] = None,
                 n_clusters: Optional[int] = None):
        """
        Args:
            vectordb (VectorDB): Vector database instance.
            kg_manager (KnowledgeGraphManager): Knowledge graph manager instance.
            collection_name (str): Name of the vector collection to use.
            n_clusters (int): Number of clusters for semantic grouping.
        """
        self.vectordb = vectordb or VectorDB()
        self.kg_manager = kg_manager or KnowledgeGraphManager()
        self.collection_name = collection_name or os.getenv("SEMANTIC_COLLECTION", "omnimind_docs")
        self.n_clusters = n_clusters or int(os.getenv("SEMANTIC_N_CLUSTERS", "10"))
        self.clusters = None
        self.cluster_labels = None
        self.cluster_to_kg = {}

    def cluster_vectors(self) -> List[int]:
        """
        Clusters all vectors in the collection using KMeans.
        Returns:
            List[int]: Cluster labels for each vector.
        """
        vectors = self._get_embeddings()
        if not vectors:
            self.clusters = None
            self.cluster_labels = None
            return []
        X = np.array(vectors)
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        self.cluster_labels = kmeans.fit_predict(X)
        self.clusters = kmeans
        return self.cluster_labels.tolist()

    def link_to_kg(self) -> None:
        """
        Links each cluster to a KG node (creates or updates entity for each cluster).
        """
        if self.cluster_labels is None:
            self.cluster_vectors()
        for cluster_id in set(self.cluster_labels):
            entity_id = f"semantic_cluster_{cluster_id}"
            properties = {"cluster_id": cluster_id, "collection": self.collection_name}
            self.kg_manager.add_entity(entity_id, "SemanticCluster", properties)
            self.cluster_to_kg[cluster_id] = entity_id

    def semantic_search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs semantic search in the vector DB and returns top_k results.
        Args:
            query_embedding (List[float]): Embedding of the query.
            top_k (int): Number of top results to return.
        Returns:
            List[Dict]: List of matching vector metadata.
        """
        return self.vectordb.search(self.collection_name, query_embedding, top_k=top_k)

    def _get_embeddings(self) -> List[List[float]]:
        """
        Loads all embeddings from the vector DB collection.
        Returns:
            List[List[float]]: List of embedding vectors.
        """
        # Try to load from in-memory, else from file
        if self.collection_name in self.vectordb.collections:
            vectors = self.vectordb.collections[self.collection_name]["vectors"]
        else:
            # Try to load from file
            import pickle, os
            collection_path = os.path.join(self.vectordb.db_path, self.collection_name, "vectors.pkl")
            if not os.path.exists(collection_path):
                return []
            with open(collection_path, "rb") as f:
                vectors = pickle.load(f)
        return [v["embedding"] for v in vectors if "embedding" in v] 