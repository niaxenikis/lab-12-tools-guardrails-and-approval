# fake_model.py
# Author: Antonia Xenikis


class FakeModel:
    """A model that returns the decisions it was given, one at a time. Used in tests."""

    def __init__(self, decisions):
        """Store the decisions to hand out and start at the first one."""
        self.decisions = decisions
        self.position = 0

    def decide(self, instructions, history, tools):
        """Return the next decision, or None when there are no more."""
        if self.position >= len(self.decisions):
            return None
        decision = self.decisions[self.position]
        self.position += 1
        return decision
