import unittest
from genesis.meta_learning_loop import MetaLearningLoop
from genesis.error_backpropagator import ErrorBackpropagator
from genesis.habit_forger import HabitForger
from pipelines.meta_learning_pipeline import meta_learning_step

class TestMetaLearning(unittest.TestCase):
    def test_loop(self):
        loop = MetaLearningLoop()
        exp = loop.experiment("a")
        self.assertIn("Experimented", exp)

    def test_backprop(self):
        bp = ErrorBackpropagator()
        err = bp.process_error("fail")
        self.assertIn("Processed error", err)

    def test_forger(self):
        forger = HabitForger()
        habit = forger.forge("pattern")
        self.assertIn("Forged habit", habit)

    def test_pipeline(self):
        result = meta_learning_step()
        self.assertIn("experiment", result)
        self.assertIn("error", result)
        self.assertIn("adapt", result)
        self.assertIn("habit", result)
        self.assertIn("reinforce", result)

if __name__ == "__main__":
    unittest.main() 