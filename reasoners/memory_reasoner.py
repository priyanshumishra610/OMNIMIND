"""
Memory Reasoner Module
"""
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from memory.episodic_manager import EpisodicManager
from memory.semantic_manager import SemanticManager
from memory.procedural_manager import ProceduralManager

class MemoryReasoner:
    """Searches and reasons across different memory types."""
    
    def __init__(self,
                 episodic_manager: Optional[EpisodicManager] = None,
                 semantic_manager: Optional[SemanticManager] = None,
                 procedural_manager: Optional[ProceduralManager] = None):
        self.episodic_manager = episodic_manager or EpisodicManager()
        self.semantic_manager = semantic_manager or SemanticManager()
        self.procedural_manager = procedural_manager or ProceduralManager()

    def search_memory(self, query: str, query_embedding: Optional[List[float]] = None, top_k: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """Search all memory stores for relevant information.
        
        Args:
            query: Search query string
            query_embedding: Optional vector for semantic search
            top_k: Maximum number of results per store
            
        Returns:
            Dict containing results from each memory type
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
        """Rank results by relevance.
        
        Args:
            results: Search results from each memory type
            query: Original search query
            query_embedding: Optional vector for semantic ranking
            
        Returns:
            List of ranked results
        """
        ranked = []
        
        # Prioritize semantic results
        for item in results.get("semantic", []):
            item["_memory_type"] = "semantic"
            ranked.append(item)
            
        # Then episodic results
        for item in results.get("episodic", []):
            item["_memory_type"] = "episodic"
            ranked.append(item)
            
        # Finally procedural results
        for item in results.get("procedural", []):
            item["_memory_type"] = "procedural"
            ranked.append(item)
            
        return ranked

    def inject_context(self, context: Dict[str, Any], ranked_memories: List[Dict[str, Any]], max_items: int = 3) -> Dict[str, Any]:
        """Inject relevant memories into context.
        
        Args:
            context: Current context dictionary
            ranked_memories: Ranked memory items
            max_items: Maximum items to inject
            
        Returns:
            Updated context dictionary
        """
        context = context.copy()
        context["injected_memories"] = ranked_memories[:max_items]
        return context

    def _search_episodic(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Search episodic memory.
        
        Args:
            query: Search query
            top_k: Maximum results
            
        Returns:
            List of matching episodes
        """
        # Get recent sessions (last 30 days)
        start_date = datetime.utcnow() - timedelta(days=30)
        episodes = self.episodic_manager.retrieve_sessions(start_date=start_date)
        
        # Score and rank episodes
        scored_episodes = []
        for ep in episodes:
            score = 0
            if query.lower() in ep.get("user_query", "").lower():
                score += 2
            if query.lower() in ep.get("response", "").lower():
                score += 1
            if score > 0:
                ep["_score"] = score
                scored_episodes.append(ep)
                
        # Sort by score and return top results
        scored_episodes.sort(key=lambda x: x["_score"], reverse=True)
        return scored_episodes[:top_k]

    def _search_semantic(self, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        """Search semantic memory.
        
        Args:
            query_embedding: Query vector
            top_k: Maximum results
            
        Returns:
            List of semantic matches
        """
        return self.semantic_manager.semantic_search(query_embedding, top_k=top_k)

    def _search_procedural(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Search procedural memory.
        
        Args:
            query: Search query
            top_k: Maximum results
            
        Returns:
            List of matching workflows
        """
        return self.procedural_manager.get_similar_workflow(query, top_k=top_k) 