import hashlib
import json
import logging

logger = logging.getLogger(__name__)

class ImmutableVerifier:
    @staticmethod
    def hash_config(config: dict, fitness: float) -> str:
        """
        Returns a SHA256 hash of the config and its fitness score.
        """
        h = hashlib.sha256()
        h.update(json.dumps({"config": config, "fitness": fitness}, sort_keys=True).encode("utf-8"))
        proof = h.hexdigest()
        logger.info(f"Immutable proof hash for config+fitness: {proof}")
        return proof 