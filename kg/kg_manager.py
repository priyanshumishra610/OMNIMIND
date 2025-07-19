"""
Knowledge Graph Manager for OMNIMIND

Handles knowledge graph operations and entity relationships.
"""

from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class KnowledgeGraphManager:
    """Manages knowledge graph operations."""
    
    def __init__(self, graph_name: str = "omnimind_kg"):
        self.graph_name = graph_name
        self.entities = {}
        self.relationships = []
    
    def add_entity(self, entity_id: str, entity_type: str, 
                   properties: Dict[str, Any]) -> bool:
        """Add an entity to the knowledge graph."""
        try:
            self.entities[entity_id] = {
                "id": entity_id,
                "type": entity_type,
                "properties": properties
            }
            logger.info(f"Added entity: {entity_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding entity {entity_id}: {e}")
            return False
    
    def add_relationship(self, source_id: str, target_id: str, 
                        relationship_type: str, properties: Dict[str, Any] = None) -> bool:
        """Add a relationship between entities."""
        try:
            if source_id not in self.entities or target_id not in self.entities:
                logger.warning(f"Entities not found: {source_id} or {target_id}")
                return False
            
            relationship = {
                "source": source_id,
                "target": target_id,
                "type": relationship_type,
                "properties": properties or {}
            }
            
            self.relationships.append(relationship)
            logger.info(f"Added relationship: {source_id} -> {target_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding relationship: {e}")
            return False
    
    def query_entities(self, entity_type: str = None, 
                      properties: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query entities by type and properties."""
        results = []
        
        for entity in self.entities.values():
            if entity_type and entity["type"] != entity_type:
                continue
            
            if properties:
                match = True
                for key, value in properties.items():
                    if key not in entity["properties"] or entity["properties"][key] != value:
                        match = False
                        break
                if not match:
                    continue
            
            results.append(entity)
        
        return results
    
    def get_relationships(self, entity_id: str = None, 
                         relationship_type: str = None) -> List[Dict[str, Any]]:
        """Get relationships for an entity or by type."""
        results = []
        
        for rel in self.relationships:
            if entity_id and rel["source"] != entity_id and rel["target"] != entity_id:
                continue
            
            if relationship_type and rel["type"] != relationship_type:
                continue
            
            results.append(rel)
        
        return results
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """Get knowledge graph statistics."""
        entity_types = {}
        relationship_types = {}
        
        for entity in self.entities.values():
            entity_type = entity["type"]
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
        
        for rel in self.relationships:
            rel_type = rel["type"]
            relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
        
        return {
            "total_entities": len(self.entities),
            "total_relationships": len(self.relationships),
            "entity_types": entity_types,
            "relationship_types": relationship_types
        } 