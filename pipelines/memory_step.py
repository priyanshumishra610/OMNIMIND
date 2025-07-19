from memory.memory_logger import MemoryLogger

def memory_step(data: dict, embed_fn=None):
    """
    Pipeline step: stores memory snapshot and updates index.
    """
    logger = MemoryLogger()
    memory_id = logger.log_memory(data, embed_fn=embed_fn)
    return {"memory_id": memory_id} 