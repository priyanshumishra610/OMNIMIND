"""
Test Simulation Components
"""
import pytest
from simulator.simulator import SimulationEngine
from world_model.environment import Environment
from world_model.predictor import Predictor

def test_simulation_engine():
    """Test simulation engine functionality."""
    engine = SimulationEngine()
    
    scenario = {
        "initial_state": {
            "efficiency": 0.7,
            "error_rate": 0.3
        },
        "proposed_changes": [
            "optimize_performance",
            "reduce_errors"
        ]
    }
    
    result = engine.run_simulation(scenario)
    assert isinstance(result, dict)
    assert "improvements" in result
    assert "risks" in result

def test_environment_generation():
    """Test environment generation and state management."""
    env = Environment()
    
    config = {
        "complexity": "medium",
        "variables": ["code_quality", "system_load"],
        "constraints": {"resources": "limited"}
    }
    
    result = env.generate(config)
    assert isinstance(result, dict)
    assert "state" in result
    assert "variables" in result
    assert "constraints" in result

def test_consequence_prediction():
    """Test consequence prediction functionality."""
    predictor = Predictor()
    
    actions = [
        {"type": "refactor", "target": "error_handling"},
        {"type": "optimize", "target": "performance"}
    ]
    
    current_state = {
        "code_quality": 0.6,
        "system_performance": 0.7,
        "technical_debt": 0.4
    }
    
    result = predictor.predict_consequences(actions, current_state)
    assert isinstance(result, dict)
    assert "future_states" in result
    assert "risks" in result
    assert "opportunities" in result 