"""
XAI Pipeline (ZenML step)
"""
from zenml import step
from genesis.explainability import Explainability

@step
def xai_step(config=None):
    """ZenML step for explainability."""
    xai = Explainability(config)
    return xai.explain()

def main():
    print(xai_step())

if __name__ == "__main__":
    main() 