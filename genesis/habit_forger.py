"""
Habit Forger — Consolidates Useful Patterns
"""
import os

class HabitForger:
    """Consolidates and stores useful behavioral patterns as habits."""
    def __init__(self, config=None):
        self.habits = []
        self.config = config or {}
        # TODO: Connect to meta-learning loop

    def forge(self, pattern):
        """Consolidate a pattern into a habit."""
        self.habits.append(pattern)
        return f"Forged habit: {pattern}"

    def get_habits(self):
        """Return all forged habits."""
        return self.habits

if __name__ == "__main__":
    forger = HabitForger()
    print(forger.forge("repeat success"))
    print(forger.get_habits()) 