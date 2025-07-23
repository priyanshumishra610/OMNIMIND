"""
Omni Ledger — Immutable Log for Lawful/Unlawful Actions
"""
import os

class OmniLedger:
    """Immutable log for every lawful vs unlawful action."""
    def __init__(self, config=None):
        self.log = []
        self.config = config or {}
        # TODO: Connect to circuit breaker

    def log_action(self, action, lawful=True):
        """Log an action as lawful or unlawful."""
        entry = {"action": action, "lawful": lawful}
        self.log.append(entry)
        return entry

    def get_log(self):
        """Return the full action log."""
        return self.log

if __name__ == "__main__":
    ledger = OmniLedger()
    print(ledger.log_action("test action", lawful=True))
    print(ledger.get_log()) 