import unittest
from world_model.environment_synthesizer import EnvironmentSynthesizer
from world_model.agent_actor import AgentActor
from world_model.consequence_predictor import ConsequencePredictor
from pipelines.world_simulation_pipeline import world_simulation_step

class TestWorldSimulation(unittest.TestCase):
    def test_synthesizer(self):
        synth = EnvironmentSynthesizer()
        res = synth.synthesize({"test": 1})
        self.assertIn("Synthesized scenario", res)

    def test_actor(self):
        actor = AgentActor()
        res = actor.deploy({"test": 1})
        self.assertIn("Deployed agent", res)

    def test_predictor(self):
        predictor = ConsequencePredictor()
        res = predictor.predict({"test": 1})
        self.assertIn("Outcome for", res)

    def test_pipeline(self):
        result = world_simulation_step()
        self.assertIn("synthesized", result)
        self.assertIn("deployed", result)
        self.assertIn("predicted", result)

if __name__ == "__main__":
    unittest.main() 