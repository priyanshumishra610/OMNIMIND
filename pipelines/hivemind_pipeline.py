"""
Hivemind Pipeline (ZenML)
"""
from zenml import step
from hive.alien_agent import AlienAgent
from hive.hivemind_translator import HivemindTranslator

@step
def hivemind_step(config=None):
    """ZenML step for hivemind processing."""
    agent = AlienAgent(config)
    translator = HivemindTranslator(config)
    
    alien_result = agent.reason("test_input")
    translation = translator.translate_concept(alien_result)
    consensus = translator.build_consensus(["view1", "view2"])
    
    return {
        "alien_result": alien_result,
        "translation": translation,
        "consensus": consensus
    }

def main():
    print(hivemind_step())

if __name__ == "__main__":
    main() 