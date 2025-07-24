"""
Test Swarm Autonomy Components
"""
import unittest
from unittest.mock import MagicMock
from hive.task_delegator import TaskDelegator
from hive.swarm_coordinator import SwarmCoordinator
from hive.memory_synthesizer import MemorySynthesizer

class TestSwarmAutonomy(unittest.TestCase):
    def setUp(self):
        self.delegator = TaskDelegator()
        self.coordinator = SwarmCoordinator()
        self.memory_synth = MemorySynthesizer()

    def test_task_delegation(self):
        """Test autonomous task delegation"""
        tasks = [
            {"id": "task1", "type": "analysis", "priority": "high"},
            {"id": "task2", "type": "synthesis", "priority": "medium"}
        ]
        nodes = [
            {"id": "node1", "capacity": 0.8, "specialties": ["analysis"]},
            {"id": "node2", "capacity": 0.6, "specialties": ["synthesis"]}
        ]
        assignments = self.delegator.assign_tasks(tasks, nodes)
        self.assertIsInstance(assignments, dict)
        self.assertEqual(len(assignments), len(tasks))
        for task_id, node_id in assignments.items():
            self.assertIn(node_id, [node["id"] for node in nodes])

    def test_swarm_coordination(self):
        """Test swarm coordination and conflict resolution"""
        conflict = {
            "type": "resource_contention",
            "nodes": ["node1", "node2"],
            "resource": "memory",
            "severity": "medium"
        }
        resolution = self.coordinator.resolve_conflict(conflict)
        self.assertIsInstance(resolution, dict)
        self.assertIn("action", resolution)
        self.assertIn("resource_allocation", resolution)

    def test_memory_synthesis(self):
        """Test collective memory synthesis"""
        memories = [
            {"source": "node1", "type": "experience", "content": "error_handling"},
            {"source": "node2", "type": "pattern", "content": "optimization"}
        ]
        synthesis = self.memory_synth.synthesize(memories)
        self.assertIsInstance(synthesis, dict)
        self.assertIn("collective_insights", synthesis)
        self.assertIn("patterns", synthesis)
        self.assertIn("recommendations", synthesis)

if __name__ == "__main__":
    unittest.main() 