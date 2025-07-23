import unittest
from hive.autonomous_delegator import AutonomousDelegator
from hive.swarm_negotiator import SwarmNegotiator
from hive.hive_memory_fusion import HiveMemoryFusion
from pipelines.swarm_autonomy_pipeline import swarm_autonomy_step

class TestSwarmAutonomy(unittest.TestCase):
    def test_delegator(self):
        delegator = AutonomousDelegator()
        assignments = delegator.delegate(["t1"], ["n1"])
        self.assertIn("t1", assignments)

    def test_negotiator(self):
        negotiator = SwarmNegotiator()
        res = negotiator.negotiate("conflict")
        self.assertIn("Resolved", res)

    def test_fusion(self):
        fusion = HiveMemoryFusion()
        fused = fusion.fuse(["exp"])
        self.assertIn("exp", fused)

    def test_pipeline(self):
        result = swarm_autonomy_step()
        self.assertIn("assignments", result)
        self.assertIn("resolution", result)
        self.assertIn("fused", result)

if __name__ == "__main__":
    unittest.main() 