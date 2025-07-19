from self_mutator.mutation_engine import MutationEngine

def mutation_step(metrics_fn):
    """
    Pipeline step: runs the mutation engine and returns the best config.
    """
    engine = MutationEngine()
    result = engine.run(metrics_fn)
    return result 