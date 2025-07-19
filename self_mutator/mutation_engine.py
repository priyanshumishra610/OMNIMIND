import random
import copy
import logging
from typing import List, Dict, Any
from .pipeline_config import PipelineConfig
from .fitness_tracker import FitnessTracker
from .mutation_logger import MutationLogger

logger = logging.getLogger(__name__)

PARAM_SPACE = {
    "chunk_size": [100, 200, 300],
    "chunk_overlap": [0.1, 0.2, 0.3],
    "embedding_model": ["openai", "bge", "sentence-transformers"],
    "retrieval_top_k": [5, 10, 15],
    "swarm_threshold": [0.7, 0.8, 0.9],
    "vector_store": ["faiss", "chroma"]
}

class MutationEngine:
    """
    Genetic Algorithm for evolving pipeline configs.
    """

    def __init__(self, population_size=6, generations=3, mutation_rate=0.3, logger_path="logs/mutation_history.jsonl"):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.fitness_tracker = FitnessTracker()
        self.logger = MutationLogger(log_path=logger_path)

    def initialize_population(self) -> List[PipelineConfig]:
        pop = []
        for _ in range(self.population_size):
            config = {k: random.choice(v) for k, v in PARAM_SPACE.items()}
            pop.append(PipelineConfig(config))
        logger.info(f"Initialized population of size {self.population_size}")
        return pop

    def evaluate_population(self, population: List[PipelineConfig], metrics_fn) -> List[float]:
        scores = []
        for config in population:
            metrics = metrics_fn(config.to_dict())
            score = self.fitness_tracker.evaluate(metrics)
            scores.append(score)
        return scores

    def select(self, population: List[PipelineConfig], scores: List[float]) -> List[PipelineConfig]:
        # Roulette wheel selection
        total = sum(scores)
        if total == 0:
            return random.choices(population, k=self.population_size)
        probs = [s / total for s in scores]
        selected = random.choices(population, weights=probs, k=self.population_size)
        logger.info(f"Selected {len(selected)} configs for next generation")
        return selected

    def crossover(self, parent1: PipelineConfig, parent2: PipelineConfig) -> PipelineConfig:
        keys = list(PARAM_SPACE.keys())
        point = random.randint(1, len(keys) - 1)
        child_config = {}
        for i, k in enumerate(keys):
            child_config[k] = parent1.to_dict()[k] if i < point else parent2.to_dict()[k]
        logger.info(f"Crossover at {point}: {child_config}")
        return PipelineConfig(child_config)

    def mutate(self, config: PipelineConfig) -> PipelineConfig:
        conf = config.to_dict()
        for k in PARAM_SPACE:
            if random.random() < self.mutation_rate:
                conf[k] = random.choice(PARAM_SPACE[k])
        logger.info(f"Mutated config: {conf}")
        return PipelineConfig(conf)

    def run(self, metrics_fn) -> Dict[str, Any]:
        population = self.initialize_population()
        best_config = None
        best_score = -float("inf")
        history = []

        for gen in range(self.generations):
            scores = self.evaluate_population(population, metrics_fn)
            gen_data = [{"config": c.to_dict(), "score": s} for c, s in zip(population, scores)]
            self.logger.log({"generation": gen, "population": gen_data})
            # Track best
            for c, s in zip(population, scores):
                if s > best_score:
                    best_score = s
                    best_config = c
            # Selection
            selected = self.select(population, scores)
            # Crossover and mutation
            next_gen = []
            for i in range(0, self.population_size, 2):
                p1, p2 = selected[i], selected[(i+1) % self.population_size]
                child1 = self.crossover(p1, p2)
                child2 = self.crossover(p2, p1)
                next_gen.extend([self.mutate(child1), self.mutate(child2)])
            population = next_gen[:self.population_size]
            history.append(gen_data)
        logger.info(f"Best config: {best_config.to_dict()} with score {best_score}")
        return {
            "best_config": best_config.to_dict(),
            "best_score": best_score,
            "history": history
        } 