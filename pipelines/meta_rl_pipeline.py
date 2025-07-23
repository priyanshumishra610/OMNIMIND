"""
Meta RL Pipeline (ZenML step)
"""
from zenml import step
from genesis.skill_learning import SkillLearning

@step
def meta_rl_step(config=None):
    """ZenML step for meta RL skill learning."""
    agent = SkillLearning(config)
    return agent.learn()

def main():
    print(meta_rl_step())

if __name__ == "__main__":
    main() 