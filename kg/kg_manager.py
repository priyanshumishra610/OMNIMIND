"""
Knowledge Graph Manager for OMNIMIND

Handles knowledge graph operations with Neo4j support.
"""

import os
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class KnowledgeGraphManager:
    """Manages knowledge graph operations with Neo4j backend."""
    
    def __init__(self, graph_name: str = "omnimind_kg", use_neo4j: bool = True):
        self.graph_name = graph_name
        self.use_neo4j = use_neo4j
        self.entities = {}
        self.relationships = []
        self._neo4j_driver = None
        
        if use_neo4j:
            self._init_neo4j()
    
    def _init_neo4j(self):
        """Initialize Neo4j connection."""
        try:
            from neo4j import GraphDatabase
            
            uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            user = os.getenv("NEO4J_USER", "neo4j")
            password = os.getenv("NEO4J_PASSWORD", "password")
            
            self._neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
            
            # Test connection
            with self._neo4j_driver.session() as session:
                session.run("RETURN 1")
            
            logger.info("Neo4j connection established")
        except ImportError:
            logger.warning("Neo4j driver not available, using in-memory storage")
            self.use_neo4j = False
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.use_neo4j = False
    
    def add_entity(self, entity_id: str, entity_type: str, 
                   properties: Dict[str, Any]) -> bool:
        """Add an entity to the knowledge graph."""
        try:
            if self.use_neo4j and self._neo4j_driver:
                return self._add_entity_neo4j(entity_id, entity_type, properties)
            else:
                return self._add_entity_simple(entity_id, entity_type, properties)
        except Exception as e:
            logger.error(f"Error adding entity {entity_id}: {e}")
            return False
    
    def _add_entity_neo4j(self, entity_id: str, entity_type: str, 
                         properties: Dict[str, Any]) -> bool:
        """Add entity using Neo4j."""
        try:
            with self._neo4j_driver.session() as session:
                # Create or merge entity
                query = """
                MERGE (e:Entity {id: $entity_id})
                SET e.type = $entity_type,
                    e += $properties
                RETURN e
                """
                session.run(query, entity_id=entity_id, 
                           entity_type=entity_type, properties=properties)
            
            logger.info(f"Added entity to Neo4j: {entity_id}")
            return True
        except Exception as e:
            logger.error(f"Neo4j entity creation error: {e}")
            return False
    
    def _add_entity_simple(self, entity_id: str, entity_type: str, 
                          properties: Dict[str, Any]) -> bool:
        """Add entity using simple storage."""
        self.entities[entity_id] = {
            "id": entity_id,
            "type": entity_type,
            "properties": properties
        }
        logger.info(f"Added entity: {entity_id}")
        return True
    
    def add_relationship(self, source_id: str, target_id: str, 
                        relationship_type: str, properties: Dict[str, Any] = None) -> bool:
        """Add a relationship between entities."""
        try:
            if self.use_neo4j and self._neo4j_driver:
                return self._add_relationship_neo4j(source_id, target_id, relationship_type, properties)
            else:
                return self._add_relationship_simple(source_id, target_id, relationship_type, properties)
        except Exception as e:
            logger.error(f"Error adding relationship: {e}")
            return False
    
    def _add_relationship_neo4j(self, source_id: str, target_id: str, 
                               relationship_type: str, properties: Dict[str, Any] = None) -> bool:
        """Add relationship using Neo4j."""
        try:
            with self._neo4j_driver.session() as session:
                # Create relationship
                query = """
                MATCH (source:Entity {id: $source_id})
                MATCH (target:Entity {id: $target_id})
                MERGE (source)-[r:RELATES {type: $relationship_type}]->(target)
                SET r += $properties
                RETURN r
                """
                session.run(query, source_id=source_id, target_id=target_id,
                           relationship_type=relationship_type, 
                           properties=properties or {})
            
            logger.info(f"Added relationship to Neo4j: {source_id} -> {target_id}")
            return True
        except Exception as e:
            logger.error(f"Neo4j relationship creation error: {e}")
            return False
    
    def _add_relationship_simple(self, source_id: str, target_id: str, 
                                relationship_type: str, properties: Dict[str, Any] = None) -> bool:
        """Add relationship using simple storage."""
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
    
    def query_entities(self, entity_type: str = None, 
                      properties: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query entities by type and properties."""
        if self.use_neo4j and self._neo4j_driver:
            return self._query_entities_neo4j(entity_type, properties)
        else:
            return self._query_entities_simple(entity_type, properties)
    
    def _query_entities_neo4j(self, entity_type: str = None, 
                             properties: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query entities using Neo4j."""
        try:
            with self._neo4j_driver.session() as session:
                if entity_type and properties:
                    query = """
                    MATCH (e:Entity)
                    WHERE e.type = $entity_type
                    AND all(key IN keys($properties) WHERE e[key] = $properties[key])
                    RETURN e
                    """
                    result = session.run(query, entity_type=entity_type, properties=properties)
                elif entity_type:
                    query = "MATCH (e:Entity {type: $entity_type}) RETURN e"
                    result = session.run(query, entity_type=entity_type)
                else:
                    query = "MATCH (e:Entity) RETURN e"
                    result = session.run(query)
                
                entities = []
                for record in result:
                    node = record["e"]
                    entities.append({
                        "id": node["id"],
                        "type": node["type"],
                        "properties": {k: v for k, v in node.items() if k not in ["id", "type"]}
                    })
                
                return entities
        except Exception as e:
            logger.error(f"Neo4j query error: {e}")
            return []
    
    def _query_entities_simple(self, entity_type: str = None, 
                              properties: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query entities using simple storage."""
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
        if self.use_neo4j and self._neo4j_driver:
            return self._get_relationships_neo4j(entity_id, relationship_type)
        else:
            return self._get_relationships_simple(entity_id, relationship_type)
    
    def _get_relationships_neo4j(self, entity_id: str = None, 
                                relationship_type: str = None) -> List[Dict[str, Any]]:
        """Get relationships using Neo4j."""
        try:
            with self._neo4j_driver.session() as session:
                if entity_id and relationship_type:
                    query = """
                    MATCH (source:Entity {id: $entity_id})-[r:RELATES {type: $relationship_type}]->(target:Entity)
                    RETURN source.id as source, target.id as target, r.type as type, r as properties
                    """
                    result = session.run(query, entity_id=entity_id, relationship_type=relationship_type)
                elif entity_id:
                    query = """
                    MATCH (source:Entity {id: $entity_id})-[r:RELATES]->(target:Entity)
                    RETURN source.id as source, target.id as target, r.type as type, r as properties
                    """
                    result = session.run(query, entity_id=entity_id)
                else:
                    query = "MATCH (source:Entity)-[r:RELATES]->(target:Entity) RETURN source.id as source, target.id as target, r.type as type, r as properties"
                    result = session.run(query)
                
                relationships = []
                for record in result:
                    rel_props = {k: v for k, v in record["properties"].items() if k != "type"}
                    relationships.append({
                        "source": record["source"],
                        "target": record["target"],
                        "type": record["type"],
                        "properties": rel_props
                    })
                
                return relationships
        except Exception as e:
            logger.error(f"Neo4j relationship query error: {e}")
            return []
    
    def _get_relationships_simple(self, entity_id: str = None, 
                                 relationship_type: str = None) -> List[Dict[str, Any]]:
        """Get relationships using simple storage."""
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
        if self.use_neo4j and self._neo4j_driver:
            return self._get_graph_stats_neo4j()
        else:
            return self._get_graph_stats_simple()
    
    def _get_graph_stats_neo4j(self) -> Dict[str, Any]:
        """Get graph statistics using Neo4j."""
        try:
            with self._neo4j_driver.session() as session:
                # Count entities
                entity_count = session.run("MATCH (e:Entity) RETURN count(e) as count").single()["count"]
                
                # Count relationships
                rel_count = session.run("MATCH ()-[r:RELATES]->() RETURN count(r) as count").single()["count"]
                
                # Entity types
                entity_types = session.run("MATCH (e:Entity) RETURN e.type as type, count(e) as count")
                entity_type_counts = {record["type"]: record["count"] for record in entity_types}
                
                # Relationship types
                rel_types = session.run("MATCH ()-[r:RELATES]->() RETURN r.type as type, count(r) as count")
                rel_type_counts = {record["type"]: record["count"] for record in rel_types}
                
                return {
                    "total_entities": entity_count,
                    "total_relationships": rel_count,
                    "entity_types": entity_type_counts,
                    "relationship_types": rel_type_counts,
                    "backend": "neo4j"
                }
        except Exception as e:
            logger.error(f"Neo4j stats error: {e}")
            return {"error": str(e)}
    
    def _get_graph_stats_simple(self) -> Dict[str, Any]:
        """Get graph statistics using simple storage."""
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
            "relationship_types": relationship_types,
            "backend": "simple"
        }
    
    def close(self):
        """Close Neo4j connection."""
        if self._neo4j_driver:
            self._neo4j_driver.close() 