"""
Unit tests for Sentience Modules
-------------------------------
Verifies instantiation and stub flows for each core sentience module.
"""
import pytest
from sentience.intent_model import IntentModel
from sentience.self_evaluator import SelfEvaluator
from sentience.chain_of_thought import ChainOfThoughtReasoner
from sentience.emotional_layer import EmotionalLayer
from sentience.ethical_reasoner import EthicalReasoner
from sentience.embodiment import Embodiment
from sentience.sensors import Sensors
from sentience.tool_autodiscovery import ToolAutodiscovery
from sentience.visual_perception import VisualPerception
from sentience.l2l_engine import L2LEngine
from sentience.reflection_engine import ReflectionEngine
from sentience.auto_prompt import AutoPrompt
from sentience.plugin_synthesizer import PluginSynthesizer
from sentience.life_loop import LifeLoop
from sentience.other_mind_simulator import OtherMindSimulator
from sentience.self_updater import SelfUpdater

def test_intent_model():
    """Test IntentModel instantiation and goal stack."""
    model = IntentModel()
    model.add_goal('Test Goal', urgency=0.7)
    assert len(model.get_goals()) == 1

def test_self_evaluator():
    """Test SelfEvaluator basic evaluation."""
    evaluator = SelfEvaluator()
    result = evaluator.evaluate('output', expected='output')
    assert result['success']

def test_chain_of_thought():
    """Test ChainOfThoughtReasoner stub reasoning."""
    cot = ChainOfThoughtReasoner()
    steps = cot.reason('Test prompt')
    assert isinstance(steps, list)

def test_emotional_layer():
    """Test EmotionalLayer state update."""
    emotion = EmotionalLayer()
    emotion.update({'stress_delta': 0.1})
    state = emotion.get_state()
    assert 'stress' in state

def test_ethical_reasoner():
    """Test EthicalReasoner dilemma evaluation."""
    ethics = EthicalReasoner()
    result = ethics.evaluate_dilemma({'situation': 'test'})
    assert 'decision' in result

def test_embodiment():
    """Test Embodiment state update."""
    body = Embodiment()
    body.update({'energy_delta': -0.1})
    state = body.get_state()
    assert 'energy' in state

def test_sensors():
    """Test Sensors reading."""
    sensors = Sensors()
    reading = sensors.read()
    assert 'fatigue' in reading

def test_tool_autodiscovery():
    """Test ToolAutodiscovery cataloging."""
    autodiscovery = ToolAutodiscovery()
    autodiscovery.discover('test_tool', {'desc': 'A test tool'})
    catalog = autodiscovery.get_catalog()
    assert 'test_tool' in catalog

def test_visual_perception():
    """Test VisualPerception stub."""
    vision = VisualPerception()
    result = vision.perceive(None)
    assert 'description' in result

def test_l2l_engine():
    """Test L2LEngine adaptation."""
    l2l = L2LEngine()
    result = l2l.adapt({'experience': 'test'})
    assert 'adapted' in result

def test_reflection_engine():
    """Test ReflectionEngine stub reflection."""
    reflection = ReflectionEngine()
    result = reflection.reflect('action', 'result')
    assert 'reflection' in result

def test_auto_prompt():
    """Test AutoPrompt optimization."""
    autoprompt = AutoPrompt()
    result = autoprompt.optimize('prompt')
    assert result.startswith('[Optimized]')

def test_plugin_synthesizer():
    """Test PluginSynthesizer stub synthesis."""
    synth = PluginSynthesizer()
    result = synth.synthesize({'requirement': 'test'})
    assert 'plugin_created' in result

def test_life_loop():
    """Test LifeLoop step and state."""
    life = LifeLoop()
    life.step('active')
    state = life.get_state()
    assert 'energy' in state

def test_other_mind_simulator():
    """Test OtherMindSimulator stub simulation."""
    sim = OtherMindSimulator()
    result = sim.simulate({'scenario': 'test'})
    assert 'simulated_agents' in result

def test_self_updater():
    """Test SelfUpdater check and log."""
    updater = SelfUpdater()
    status = updater.check_for_updates()
    assert 'update_available' in status
    success = updater.download_update()
    assert success is False 