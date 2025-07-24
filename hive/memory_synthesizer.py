"""
Memory Synthesis Module
"""
from typing import Dict, List, Any

class MemorySynthesizer:
    """Synthesizes collective memories from swarm nodes."""
    
    def __init__(self):
        self.syntheses = []
        self.patterns = {}
        
    def synthesize(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize collective insights from node memories.
        
        Args:
            memories: List of memory dictionaries
            
        Returns:
            Dict containing synthesis results
        """
        # Extract patterns
        patterns = self._extract_patterns(memories)
        
        # Generate insights
        insights = self._generate_insights(patterns)
        
        # Form recommendations
        recommendations = self._form_recommendations(insights)
        
        synthesis = {
            "collective_insights": insights,
            "patterns": patterns,
            "recommendations": recommendations
        }
        
        self.syntheses.append(synthesis)
        return synthesis
        
    def _extract_patterns(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract patterns from memories.
        
        Args:
            memories: List of memory dictionaries
            
        Returns:
            Dict containing extracted patterns
        """
        patterns = {
            "experience": [],
            "behavior": [],
            "knowledge": []
        }
        
        for memory in memories:
            memory_type = memory.get("type")
            content = memory.get("content")
            
            if memory_type == "experience":
                patterns["experience"].append({
                    "type": "learning_pattern",
                    "content": content,
                    "frequency": self._count_similar_memories(content, memories)
                })
            elif memory_type == "pattern":
                patterns["behavior"].append({
                    "type": "behavior_pattern",
                    "content": content,
                    "source": memory.get("source")
                })
                
        return patterns
        
    def _generate_insights(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate insights from patterns.
        
        Args:
            patterns: Pattern dictionary
            
        Returns:
            List of insight strings
        """
        insights = []
        
        # Analyze experience patterns
        if patterns["experience"]:
            frequent_experiences = [p for p in patterns["experience"] if p["frequency"] > 1]
            if frequent_experiences:
                insights.append(f"Common learning pattern: {frequent_experiences[0]['content']}")
                
        # Analyze behavior patterns
        if patterns["behavior"]:
            behavior_sources = set(p["source"] for p in patterns["behavior"])
            if len(behavior_sources) > 1:
                insights.append("Cross-node behavior consistency detected")
                
        return insights
        
    def _form_recommendations(self, insights: List[str]) -> List[Dict[str, Any]]:
        """Form recommendations based on insights.
        
        Args:
            insights: List of insight strings
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        for insight in insights:
            if "learning pattern" in insight.lower():
                recommendations.append({
                    "type": "enhancement",
                    "target": "learning_system",
                    "action": "reinforce_pattern",
                    "priority": "high"
                })
            elif "consistency" in insight.lower():
                recommendations.append({
                    "type": "optimization",
                    "target": "swarm_coordination",
                    "action": "standardize_behavior",
                    "priority": "medium"
                })
                
        return recommendations
        
    def _count_similar_memories(self, content: str, memories: List[Dict[str, Any]]) -> int:
        """Count memories with similar content.
        
        Args:
            content: Content string to match
            memories: List of memory dictionaries
            
        Returns:
            Integer count of similar memories
        """
        return sum(1 for m in memories if m.get("content") == content) 