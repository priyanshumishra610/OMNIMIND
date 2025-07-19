from simulator.simulator import WorldSimulator

def simulation_step(input_data: dict):
    """
    ZenML pipeline step: runs the WorldSimulator on input facts.
    """
    query = input_data.get("query")
    facts = input_data.get("facts", {})
    simulator = WorldSimulator()
    scenarios = simulator.simulate(facts, query)
    return {"simulation_scenarios": scenarios} 