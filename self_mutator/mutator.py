"""
Self Mutator for OMNIMIND

Handles genetic algorithm-based self-repair and evolution.
"""

import random
import json
from typing import List, Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)


class SelfMutator:
    """Genetic algorithm-based self-mutation system."""
    
    def __init__(self, population_size: int = 10, mutation_rate: float = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = []
        self.generation = 0
        self.evolution_history = []
    
    def initialize_population(self, initial_configs: List[Dict[str, Any]]):
        """Initialize the population with initial configurations."""
        self.population = initial_configs[:self.population_size]
        self.generation = 0
        logger.info(f"Initialized population with {len(self.population)} individuals")
    
    def evolve(self, fitness_function: Callable[[Dict[str, Any]], float], 
               generations: int = 10) -> List[Dict[str, Any]]:
        """Evolve the population using genetic algorithms."""
        try:
            for gen in range(generations):
                # Evaluate fitness
                fitness_scores = []
                for individual in self.population:
                    fitness = fitness_function(individual)
                    fitness_scores.append((fitness, individual))
                
                # Sort by fitness
                fitness_scores.sort(key=lambda x: x[0], reverse=True)
                
                # Record generation stats
                best_fitness = fitness_scores[0][0]
                avg_fitness = sum(f[0] for f in fitness_scores) / len(fitness_scores)
                
                generation_stats = {
                    "generation": self.generation,
                    "best_fitness": best_fitness,
                    "avg_fitness": avg_fitness,
                    "population_size": len(self.population)
                }
                self.evolution_history.append(generation_stats)
                
                # Selection and reproduction
                new_population = self._selection_and_reproduction(fitness_scores)
                
                # Mutation
                new_population = self._mutate_population(new_population)
                
                self.population = new_population
                self.generation += 1
                
                logger.info(f"Generation {self.generation}: Best fitness = {best_fitness:.4f}")
            
            return self.population
            
        except Exception as e:
            logger.error(f"Error in evolution: {e}")
            return self.population
    
    def _selection_and_reproduction(self, fitness_scores: List[tuple]) -> List[Dict[str, Any]]:
        """Perform selection and reproduction."""
        new_population = []
        
        # Keep top 20% (elitism)
        elite_count = max(1, int(self.population_size * 0.2))
        new_population.extend([individual for _, individual in fitness_scores[:elite_count]])
        
        # Generate rest through crossover
        while len(new_population) < self.population_size:
            parent1 = self._select_parent(fitness_scores)
            parent2 = self._select_parent(fitness_scores)
            child = self._crossover(parent1, parent2)
            new_population.append(child)
        
        return new_population[:self.population_size]
    
    def _select_parent(self, fitness_scores: List[tuple]) -> Dict[str, Any]:
        """Select a parent using tournament selection."""
        tournament_size = 3
        tournament = random.sample(fitness_scores, tournament_size)
        return max(tournament, key=lambda x: x[0])[1]
    
    def _crossover(self, parent1: Dict[str, Any], parent2: Dict[str, Any]) -> Dict[str, Any]:
        """Perform crossover between two parents."""
        child = {}
        
        # Simple uniform crossover
        for key in parent1.keys():
            if random.random() < 0.5:
                child[key] = parent1[key]
            else:
                child[key] = parent2.get(key, parent1[key])
        
        return child
    
    def _mutate_population(self, population: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply mutations to the population."""
        mutated_population = []
        
        for individual in population:
            if random.random() < self.mutation_rate:
                mutated_individual = self._mutate_individual(individual)
                mutated_population.append(mutated_individual)
            else:
                mutated_population.append(individual)
        
        return mutated_population
    
    def _mutate_individual(self, individual: Dict[str, Any]) -> Dict[str, Any]:
        """Mutate a single individual."""
        mutated = individual.copy()
        
        # Simple mutation: randomly change one parameter
        if mutated:
            key = random.choice(list(mutated.keys()))
            if isinstance(mutated[key], (int, float)):
                # Add/subtract small random value
                mutation = random.uniform(-0.1, 0.1) * mutated[key]
                mutated[key] += mutation
            elif isinstance(mutated[key], str):
                # Small chance to change string
                if random.random() < 0.1:
                    mutated[key] = f"{mutated[key]}_mutated"
        
        return mutated
    
    def get_best_individual(self, fitness_function: Callable[[Dict[str, Any]], float]) -> Dict[str, Any]:
        """Get the best individual from current population."""
        if not self.population:
            return {}
        
        best_individual = max(self.population, key=fitness_function)
        return best_individual
    
    def get_evolution_history(self) -> List[Dict[str, Any]]:
        """Get evolution history."""
        return self.evolution_history.copy() 