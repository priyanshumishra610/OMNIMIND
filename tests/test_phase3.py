import pytest
from simulator.simulator import WorldSimulator
from simulator.symbolic_engine import SymbolicEngine
from logger.hypothetical_logger import HypotheticalLogger

def test_symbolic_engine_rules():
    engine = SymbolicEngine()
    engine.add_rule({"if": [("A", True)], "then": ("B", True)})
    facts = {"A": True}
    result, trace = engine.infer(facts)
    assert result["B"] is True
    assert trace

def test_world_simulator_scenarios():
    sim = WorldSimulator(rules=[{"if": [("A", True)], "then": ("B", True)}])
    facts = {"A": None}
    scenarios = sim.simulate(facts, "If A is true, what about B?")
    assert isinstance(scenarios, list)
    assert any("result" in s for s in scenarios)

def test_hypothetical_logger():
    logger = HypotheticalLogger(log_path="logs/test_hypotheticals.jsonl")
    entry = {"query": "test", "scenarios": [{"result": {"A": True}}]}
    logger.log(entry)
    logs = logger.get_logs(limit=1)
    assert logs and logs[0]["query"] == "test" 