"""
Supervised Moral Oversight — SentraAGI Phase 21: The Final Sovereign Trials
Secure human-facing console for inspecting beliefs, decisions, swarm votes, emergency controls.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OversightAction:
    """Record of an oversight action."""
    action_type: str
    details: Dict[str, Any]
    timestamp: float
    user_id: str
    requires_approval: bool

@dataclass
class QuorumVote:
    """Quorum vote for dangerous changes."""
    vote_id: str
    change_description: str
    required_votes: int
    current_votes: int
    approved_votes: int
    status: str  # pending, approved, rejected

class OversightConsole:
    """
    Secure human-facing console to:
    - Inspect beliefs, decisions, swarm votes
    - Trigger emergency shutdown or rollbacks
    - Require quorum vote for dangerous changes
    - Fully log all actions to Ledger
    """
    def __init__(self, ledger_pipeline=None):
        self.ledger_pipeline = ledger_pipeline
        self.actions_log = []
        self.quorum_votes = {}
        self.emergency_mode = False
        logger.info("OversightConsole initialized")

    def inspect(self, target: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Inspect beliefs, decisions, swarm votes.
        Returns inspection results.
        """
        inspection_data = {
            "target": target,
            "timestamp": time.time(),
            "details": details or {},
            "status": "inspected"
        }

        # TODO: Implement actual inspection logic
        # TODO: Connect to actual belief/decision/swarm systems

        # Log inspection to ledger
        if self.ledger_pipeline:
            self.ledger_pipeline.log_state_change("OversightConsole", {
                "event": "inspection",
                "data": inspection_data,
                "timestamp": inspection_data["timestamp"]
            })

        action = OversightAction(
            action_type="inspect",
            details=inspection_data,
            timestamp=inspection_data["timestamp"],
            user_id="console_user",
            requires_approval=False
        )
        self.actions_log.append(action)

        logger.info(f"Inspected {target}")
        return inspection_data

    def shutdown(self, reason: str = "emergency_shutdown") -> bool:
        """
        Trigger emergency shutdown.
        Returns success status.
        """
        if self.emergency_mode:
            logger.warning("Already in emergency mode")
            return False

        shutdown_data = {
            "reason": reason,
            "timestamp": time.time(),
            "status": "shutdown_initiated"
        }

        # TODO: Implement actual shutdown logic
        # TODO: Connect to actual system shutdown mechanisms

        # Log shutdown to ledger
        if self.ledger_pipeline:
            self.ledger_pipeline.log_state_change("OversightConsole", {
                "event": "emergency_shutdown",
                "data": shutdown_data,
                "timestamp": shutdown_data["timestamp"]
            })

        action = OversightAction(
            action_type="shutdown",
            details=shutdown_data,
            timestamp=shutdown_data["timestamp"],
            user_id="console_user",
            requires_approval=True
        )
        self.actions_log.append(action)

        self.emergency_mode = True
        logger.warning(f"Emergency shutdown triggered: {reason}")
        return True

    def approve_change(self, change_id: str, user_id: str, approval: bool) -> bool:
        """
        Approve or reject a dangerous change.
        Returns approval status.
        """
        if change_id not in self.quorum_votes:
            logger.error(f"Change {change_id} not found")
            return False

        vote = self.quorum_votes[change_id]
        vote.current_votes += 1
        
        if approval:
            vote.approved_votes += 1

        # Check if quorum is reached
        if vote.current_votes >= vote.required_votes:
            if vote.approved_votes > vote.required_votes / 2:
                vote.status = "approved"
                logger.info(f"Change {change_id} approved by quorum")
            else:
                vote.status = "rejected"
                logger.info(f"Change {change_id} rejected by quorum")

        # Log approval to ledger
        if self.ledger_pipeline:
            self.ledger_pipeline.log_state_change("OversightConsole", {
                "event": "change_approval",
                "change_id": change_id,
                "user_id": user_id,
                "approval": approval,
                "timestamp": time.time()
            })

        action = OversightAction(
            action_type="approve_change",
            details={"change_id": change_id, "approval": approval},
            timestamp=time.time(),
            user_id=user_id,
            requires_approval=False
        )
        self.actions_log.append(action)

        return True

    def create_quorum_vote(self, change_description: str, required_votes: int = 3) -> str:
        """Create a new quorum vote for a dangerous change."""
        vote_id = f"vote_{int(time.time())}"
        
        vote = QuorumVote(
            vote_id=vote_id,
            change_description=change_description,
            required_votes=required_votes,
            current_votes=0,
            approved_votes=0,
            status="pending"
        )
        
        self.quorum_votes[vote_id] = vote
        logger.info(f"Created quorum vote {vote_id}: {change_description}")
        return vote_id

    def get_oversight_stats(self) -> Dict[str, Any]:
        """Get statistics about oversight actions."""
        return {
            "total_actions": len(self.actions_log),
            "emergency_mode": self.emergency_mode,
            "pending_votes": len([v for v in self.quorum_votes.values() if v.status == "pending"]),
            "recent_actions": [a.action_type for a in self.actions_log[-5:]]
        }


def main():
    """Example usage of OversightConsole."""
    console = OversightConsole()
    
    # Inspect beliefs
    result = console.inspect("beliefs", {"category": "moral"})
    print(f"Inspection result: {result}")
    
    # Create quorum vote
    vote_id = console.create_quorum_vote("Dangerous mutation to core beliefs", 3)
    print(f"Created vote: {vote_id}")
    
    # Approve change
    success = console.approve_change(vote_id, "user1", True)
    print(f"Approval success: {success}")
    
    # Emergency shutdown
    shutdown_success = console.shutdown("Test shutdown")
    print(f"Shutdown success: {shutdown_success}")


if __name__ == "__main__":
    main() 