import pytest
from self_mutator.mutation_engine import MutationEngine
from self_mutator.fitness_tracker import FitnessTracker
from self_mutator.pipeline_config import PipelineConfig

def test_population_init():
    engine = MutationEngine(population_size=4, generations=1)
    pop = engine.initialize_population()
    assert len(pop) == 4

def test_crossover_and_mutation():
    engine = MutationEngine()
    p1 = PipelineConfig({"chunk_size": 100, "chunk_overlap": 0.1, "embedding_model": "openai", "retrieval_top_k": 5, "swarm_threshold": 0.7, "vector_store": "faiss"})
    p2 = PipelineConfig({"chunk_size": 300, "chunk_overlap": 0.3, "embedding_model": "bge", "retrieval_top_k": 15, "swarm_threshold": 0.9, "vector_store": "chroma"})
    child = engine.crossover(p1, p2)
    mutated = engine.mutate(child)
    assert isinstance(mutated, PipelineConfig)

def test_fitness_tracker():
    tracker = FitnessTracker()
    score = tracker.evaluate({"accuracy": 0.8, "consensus": 0.9, "latency": 0.5, "feedback": 0.7})
    assert 0 <= score <= 1

def test_mutation_engine_run():
    engine = MutationEngine(population_size=4, generations=2)
    def dummy_metrics(config):
        return {"accuracy": 0.8, "consensus": 0.8, "latency": 0.5, "feedback": 0.7}
    result = engine.run(dummy_metrics)
    assert "best_config" in result
    assert "history" in result 