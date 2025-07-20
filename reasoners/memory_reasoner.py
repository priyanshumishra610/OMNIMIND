import os
from typing import List, Dict, Any, Optional
from memory.episodic_manager import EpisodicManager
from memory.semantic_manager import SemanticManager
from memory.procedural_manager import ProceduralManager

class MemoryReasoner:
    """
    Searches episodic, semantic, and procedural memory, ranks relevance, and injects context for the Swarm Orchestrator.
    Modular and configurable for pipeline integration.
    """
    def __init__(self,
                 episodic_manager: Optional[EpisodicManager] = None,
                 semantic_manager: Optional[SemanticManager] = None,
                 procedural_manager: Optional[ProceduralManager] = None):
        self.episodic_manager = episodic_manager or EpisodicManager()
        self.semantic_manager = semantic_manager or SemanticManager()
        self.procedural_manager = procedural_manager or ProceduralManager()

    def search_memory(self, query: str, query_embedding: Optional[List[float]] = None, top_k: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Searches all memory stores for relevant episodes, semantic matches, and workflows.
        Args:
            query (str): The user/system query.
            query_embedding (List[float], optional): Embedding for semantic search.
            top_k (int): Number of top results per store.
        Returns:
            Dict[str, List[Dict]]: Results from episodic, semantic, and procedural memory.
        """
        episodic_results = self._search_episodic(query, top_k)
        semantic_results = self._search_semantic(query_embedding, top_k) if query_embedding else []
        procedural_results = self._search_procedural(query, top_k)
        return {
            "episodic": episodic_results,
            "semantic": semantic_results,
            "procedural": procedural_results
        }

    def rank_relevance(self, results: Dict[str, List[Dict[str, Any]]], query: str, query_embedding: Optional[List[float]] = None) -> List[Dict[str, Any]]:
        """
        Ranks all results by relevance to the query (simple heuristic: semantic > episodic > procedural).
        Args:
            results (dict): Results from search_memory.
            query (str): The query string.
            query_embedding (List[float], optional): Embedding for semantic ranking.
        Returns:
            List[Dict]: Ranked list of relevant memory items.
        """
        ranked = []
        # Prioritize semantic, then episodic, then procedural
        for item in results.get("semantic", []):
            item["_memory_type"] = "semantic"
            ranked.append(item)
        for item in results.get("episodic", []):
            item["_memory_type"] = "episodic"
            ranked.append(item)
        for item in results.get("procedural", []):
            item["_memory_type"] = "procedural"
            ranked.append(item)
        # Optionally, could sort by similarity/score if available
        return ranked

    def inject_context(self, context: Dict[str, Any], ranked_memories: List[Dict[str, Any]], max_items: int = 3) -> Dict[str, Any]:
        """
        Injects the most relevant memories into the provided context for the Swarm Orchestrator.
        Args:
            context (dict): The current context to augment.
            ranked_memories (List[Dict]): Ranked memory items.
            max_items (int): Max number of memories to inject.
        Returns:
            dict: Augmented context.
        """
        context = context.copy()
        context["injected_memories"] = ranked_memories[:max_items]
        return context

    def _search_episodic(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """
        Simple keyword search in episodic memory (user_query and agent_thoughts).
        """
        episodes = self.episodic_manager.retrieve_sessions(limit=100)
        results = []
        for ep in episodes:
            score = 0
            if query.lower() in ep.get("user_query", "").lower():
                score += 2
            if query.lower() in ep.get("agent_thoughts", "").lower():
                score += 1
            if score > 0:
                ep["_score"] = score
                results.append(ep)
        results.sort(key=lambda x: x["_score"], reverse=True)
        return results[:top_k]

    def _search_semantic(self, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        """
        Semantic search using the SemanticManager.
        """
        return self.semantic_manager.semantic_search(query_embedding, top_k=top_k)

    def _search_procedural(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """
        Search for similar workflows by tag/description.
        """
        return self.procedural_manager.get_similar_workflow(query, top_k=top_k) 