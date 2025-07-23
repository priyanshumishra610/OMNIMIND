import unittest
from embodiment.somatic_core import SomaticCore
from embodiment.homeostasis_engine import HomeostasisEngine
from embodiment.stress_adaptive_layer import StressAdaptiveLayer
from multi_modal.tactile_agent import TactileAgent
from multi_modal.visual_foveation import VisualFoveation

class TestEmbodiment(unittest.TestCase):
    def test_somatic_core(self):
        core = SomaticCore()
        status = core.update_state(-5, "sitting", {"touch": "active"})
        self.assertIn("energy", status)

    def test_homeostasis_engine(self):
        engine = HomeostasisEngine()
        state = engine.regulate({"stress": 0.2})
        self.assertIn("stress", state)

    def test_stress_adaptive_layer(self):
        layer = StressAdaptiveLayer()
        threshold = layer.adapt_threshold()
        self.assertIsInstance(threshold, float)

    def test_tactile_agent(self):
        agent = TactileAgent()
        sensed = agent.sense_touch({"pressure": 0.5})
        self.assertIn("Touch sensed", sensed)

    def test_visual_foveation(self):
        vf = VisualFoveation()
        focused = vf.focus_attention("img", (0,0,10,10))
        self.assertIn("Attention focused", focused)

if __name__ == "__main__":
    unittest.main() 