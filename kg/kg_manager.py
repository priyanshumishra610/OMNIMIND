"""
Knowledge Graph Manager Module
"""
from typing import Dict, List, Any, Optional

class KnowledgeGraphManager:
    """Manages knowledge graph operations."""
    
    def __init__(self, use_neo4j: bool = False):
        self.use_neo4j = use_neo4j
        self.entities = {}
        self.relationships = []
        
    def add_entity(self, entity_id: str, entity_type: str, properties: Dict[str, Any]) -> bool:
        """Add an entity to the graph.
        
        Args:
            entity_id: Unique entity identifier
            entity_type: Type of entity
            properties: Entity properties
            
        Returns:
            Success status
        """
        if entity_id not in self.entities:
            self.entities[entity_id] = {
                "type": entity_type,
                "properties": properties
            }
            return True
        return False
        
    def add_relationship(self, source_id: str, target_id: str, relationship_type: str) -> bool:
        """Add a relationship between entities.
        
        Args:
            source_id: Source entity ID
            target_id: Target entity ID
            relationship_type: Type of relationship
            
        Returns:
            Success status
        """
        if source_id in self.entities and target_id in self.entities:
            self.relationships.append({
                "source": source_id,
                "target": target_id,
                "type": relationship_type
            })
            return True
        return False
        
    def get_graph_stats(self) -> Dict[str, Any]:
        """Get graph statistics.
        
        Returns:
            Dictionary of statistics
        """
        entity_types = set(e["type"] for e in self.entities.values())
        relationship_types = set(r["type"] for r in self.relationships)
        
        return {
            "total_entities": len(self.entities),
            "total_relationships": len(self.relationships),
            "entity_types": list(entity_types),
            "relationship_types": list(relationship_types)
        }
        
    def query(self, query: str, limit: Optional[int] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Query the knowledge graph.
        
        Args:
            query: Query string
            limit: Maximum number of results
            
        Returns:
            Dictionary containing entities and relationships
        """
        # Simple keyword-based query
        matching_entities = []
        for entity_id, entity in self.entities.items():
            if (query.lower() in entity_id.lower() or
                query.lower() in entity["type"].lower() or
                any(query.lower() in str(v).lower() for v in entity["properties"].values())):
                matching_entities.append({
                    "id": entity_id,
                    "type": entity["type"],
                    "name": entity["properties"].get("name", entity_id)
                })
                
        # Find relationships involving matching entities
        matching_relationships = []
        matching_entity_ids = set(e["id"] for e in matching_entities)
        for rel in self.relationships:
            if rel["source"] in matching_entity_ids or rel["target"] in matching_entity_ids:
                matching_relationships.append({
                    "source": rel["source"],
                    "target": rel["target"],
                    "type": rel["type"]
                })
                
        # Apply limit if specified
        if limit:
            matching_entities = matching_entities[:limit]
            matching_relationships = matching_relationships[:limit]
            
        return {
            "entities": matching_entities,
            "relationships": matching_relationships
        } 