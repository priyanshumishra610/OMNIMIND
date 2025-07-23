"""
Somatic Core — Tracks Virtual Body State
"""
import os

class SomaticCore:
    """Tracks energy, posture, and simulated sensors for the virtual body."""
    def __init__(self, config=None):
        self.energy = 100
        self.posture = "upright"
        self.sensors = {}
        self.config = config or {}
        # TODO: Initialize more detailed body state

    def update_state(self, energy_delta=0, posture=None, sensors=None):
        """Update body state parameters."""
        self.energy += energy_delta
        if posture:
            self.posture = posture
        if sensors:
            self.sensors.update(sensors)
        return self.get_status()

    def get_status(self):
        """Return current body state."""
        return {
            "energy": self.energy,
            "posture": self.posture,
            "sensors": self.sensors
        }

if __name__ == "__main__":
    core = SomaticCore()
    print(core.update_state(-10, "sitting", {"touch": "active"}))
    print(core.get_status()) 