"""
Governance Pipeline (ZenML)
"""
from zenml import step
from governance.constitution import Constitution
from governance.vote_engine import VoteEngine
from governance.rollback_guard import RollbackGuard

@step
def governance_step(config=None):
    """ZenML step for governance processing."""
    constitution = Constitution(config)
    vote = VoteEngine(config)
    guard = RollbackGuard(config)
    
    alignment = constitution.verify_alignment("test_action")
    proposal = vote.propose("test_proposal")
    checkpoint = guard.checkpoint()
    
    return {
        "alignment": alignment,
        "proposal": proposal,
        "checkpoint": checkpoint
    }

def main():
    print(governance_step())

if __name__ == "__main__":
    main() 