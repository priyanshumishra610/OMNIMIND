"""
Meta-Learning Pipeline (ZenML)
"""
from zenml import step
from genesis.meta_learning_loop import MetaLearningLoop
from genesis.error_backpropagator import ErrorBackpropagator
from genesis.habit_forger import HabitForger

@step
def meta_learning_step(config=None):
    """ZenML step for meta-learning loop."""
    loop = MetaLearningLoop(config)
    backprop = ErrorBackpropagator(config)
    forger = HabitForger(config)

    # Example: experiment, adapt, reinforce
    exp = loop.experiment("try new strategy")
    err = backprop.process_error("failure event")
    adapt = loop.adapt("feedback from error")
    habit = forger.forge("useful pattern")
    reinforce = loop.reinforce("useful pattern")

    return {
        "experiment": exp,
        "error": err,
        "adapt": adapt,
        "habit": habit,
        "reinforce": reinforce
    }

def main():
    print("--- Running Meta-Learning Pipeline ---")
    result = meta_learning_step()
    print(result)

if __name__ == "__main__":
    main() 