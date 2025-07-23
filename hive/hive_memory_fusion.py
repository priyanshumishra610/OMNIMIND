"""
Hive Memory Fusion — Merges Experiences Back to Kernel
"""
import os

class HiveMemoryFusion:
    """Merges node experiences back to the kernel memory."""
    def __init__(self, config=None):
        self.fused_memory = []
        self.config = config or {}
        # TODO: Connect to kernel memory

    def fuse(self, memories):
        """Merge a list of node memories into the kernel."""
        # TODO: Real fusion logic
        self.fused_memory.extend(memories)
        return self.fused_memory

    def get_fused_memory(self):
        """Return current fused memory."""
        return self.fused_memory

if __name__ == "__main__":
    fusion = HiveMemoryFusion()
    print(fusion.fuse(["exp1", "exp2"]))
    print(fusion.get_fused_memory()) 