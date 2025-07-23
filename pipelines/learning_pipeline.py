"""
Unified Learning Pipeline (ZenML step)
"""
from zenml import step
from genesis.skill_learning import SkillLearning
from genesis.continual_learning import ContinualLearning
from skills.skill_discovery import SkillDiscovery
from skills.skill_executor import SkillExecutor

@step
def learning_step(config=None):
    """ZenML step for unified meta RL + continual + skill flow."""
    sl = SkillLearning(config)
    cl = ContinualLearning(config)
    sd = SkillDiscovery(config)
    se = SkillExecutor(config)
    return {
        "skill": sl.learn(),
        "continual": cl.update(),
        "discovered": sd.discover(),
        "executed": se.execute("sample_skill")
    }

def main():
    print(learning_step())

if __name__ == "__main__":
    main()
