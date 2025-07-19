import pytest
from agents.base_agent import BaseAgent
from agents.fact_checker_agent import FactCheckerAgent
from agents.skeptic_agent import SkepticAgent
from agents.swarm_orchestrator import SwarmOrchestrator
from plugins.plugin_manager import PluginManager
from verifier.immutable_verifier import ImmutableVerifier

def test_base_agent_output():
    agent = BaseAgent()
    context = [{"text": "The sky is blue."}]
    result = agent.run("What color is the sky?", context)
    assert "answer" in result

def test_fact_checker_flags():
    agent = FactCheckerAgent()
    context = [{"text": "The sky is blue."}]
    verdict = agent.run("What color is the sky?", "The sky is blue.", context)
    assert verdict["verdict"] in ["supported", "unsupported"]

def test_skeptic_challenge():
    agent = SkepticAgent()
    context = [{"text": "The sky is blue."}]
    challenge = agent.run("What color is the sky?", "The sky is blue.", context)
    assert "challenge" in challenge

def test_swarm_consensus_and_fallback():
    plugin_manager = PluginManager()
    swarm = SwarmOrchestrator(plugin_manager=plugin_manager, consensus_threshold=0.9)
    context = [{"text": "The sky is blue."}]
    result = swarm.run_swarm("What color is the sky?", context)
    assert "consensus" in result
    if result["consensus_score"] < 0.9:
        assert result["plugin_result"] is not None

def test_immutable_verifier_hash():
    verifier = ImmutableVerifier()
    answer = "The sky is blue."
    proof = verifier.hash_answer(answer)
    assert len(proof) == 64 