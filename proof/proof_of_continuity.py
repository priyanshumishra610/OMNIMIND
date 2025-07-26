"""
Existential Proof Generator — SentraAGI Phase 21: The Final Sovereign Trials
Build a full "proof of life" tracking all mutations, reflections, rollbacks since Phase 1.
"""

import json
import hashlib
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class ProofEntry:
    """A single entry in the proof of continuity."""
    phase: str
    timestamp: float
    mutation_type: str
    mutation_hash: str
    parent_hash: str
    description: str
    metadata: Dict[str, Any]

@dataclass
class ContinuityProof:
    """Complete proof of continuity from Phase 1 to present."""
    genesis_hash: str
    final_hash: str
    total_phases: int
    total_mutations: int
    total_rollbacks: int
    chain_integrity: bool
    entries: List[ProofEntry]
    generated_at: float

class ProofOfContinuity:
    """
    Build a full "proof of life":
    - Tracks all mutations, reflections, rollbacks since Phase 1
    - Generates final hash lineage
    - Outputs a JSON or Markdown file with chain-of-proof
    """
    def __init__(self, proof_path: str = "data/proof_of_continuity.json"):
        self.proof_path = Path(proof_path)
        self.proof_path.parent.mkdir(parents=True, exist_ok=True)
        self.entries: List[ProofEntry] = []
        self.genesis_hash = "0" * 64
        self._load_existing_proof()
        logger.info(f"ProofOfContinuity initialized at {self.proof_path}")

    def _load_existing_proof(self):
        """Load existing proof if available."""
        try:
            if self.proof_path.exists():
                with open(self.proof_path, 'r') as f:
                    data = json.load(f)
                    self.entries = [ProofEntry(**entry) for entry in data.get('entries', [])]
                    self.genesis_hash = data.get('genesis_hash', self.genesis_hash)
                    logger.info(f"Loaded {len(self.entries)} existing proof entries")
        except Exception as e:
            logger.warning(f"Could not load existing proof: {e}")

    def add_mutation(self, phase: str, mutation_type: str, description: str, metadata: Dict[str, Any] = None):
        """
        Add a new mutation to the proof chain.
        """
        parent_hash = self.entries[-1].mutation_hash if self.entries else self.genesis_hash
        
        entry = ProofEntry(
            phase=phase,
            timestamp=time.time(),
            mutation_type=mutation_type,
            mutation_hash=self._generate_mutation_hash(phase, mutation_type, description, parent_hash),
            parent_hash=parent_hash,
            description=description,
            metadata=metadata or {}
        )
        
        self.entries.append(entry)
        logger.info(f"Added mutation: {mutation_type} in {phase}")

    def generate_proof(self) -> ContinuityProof:
        """
        Generate the complete proof of continuity.
        Returns ContinuityProof object.
        """
        if not self.entries:
            logger.warning("No entries to generate proof from")
            return self._create_empty_proof()

        final_hash = self.entries[-1].mutation_hash
        chain_integrity = self._verify_chain_integrity()
        
        # Count different types of mutations
        mutation_types = [entry.mutation_type for entry in self.entries]
        total_mutations = len([m for m in mutation_types if m != "rollback"])
        total_rollbacks = len([m for m in mutation_types if m == "rollback"])
        
        # Count unique phases
        phases = set(entry.phase for entry in self.entries)
        total_phases = len(phases)

        proof = ContinuityProof(
            genesis_hash=self.genesis_hash,
            final_hash=final_hash,
            total_phases=total_phases,
            total_mutations=total_mutations,
            total_rollbacks=total_rollbacks,
            chain_integrity=chain_integrity,
            entries=self.entries,
            generated_at=time.time()
        )

        logger.info(f"Generated proof: {total_mutations} mutations, {total_rollbacks} rollbacks, {total_phases} phases")
        return proof

    def export_proof(self, format: str = "json", output_path: str = None) -> str:
        """
        Export the proof to JSON or Markdown format.
        Returns the path to the exported file.
        """
        proof = self.generate_proof()
        
        if format.lower() == "json":
            return self._export_json(proof, output_path)
        elif format.lower() == "markdown":
            return self._export_markdown(proof, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _generate_mutation_hash(self, phase: str, mutation_type: str, description: str, parent_hash: str) -> str:
        """Generate a hash for a mutation entry."""
        content = f"{phase}:{mutation_type}:{description}:{parent_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _verify_chain_integrity(self) -> bool:
        """Verify the integrity of the proof chain."""
        if not self.entries:
            return True
            
        prev_hash = self.genesis_hash
        for entry in self.entries:
            expected_hash = self._generate_mutation_hash(
                entry.phase, entry.mutation_type, entry.description, prev_hash
            )
            if entry.mutation_hash != expected_hash:
                logger.error(f"Chain integrity broken at entry: {entry}")
                return False
            prev_hash = entry.mutation_hash
        
        return True

    def _create_empty_proof(self) -> ContinuityProof:
        """Create an empty proof when no entries exist."""
        return ContinuityProof(
            genesis_hash=self.genesis_hash,
            final_hash=self.genesis_hash,
            total_phases=0,
            total_mutations=0,
            total_rollbacks=0,
            chain_integrity=True,
            entries=[],
            generated_at=time.time()
        )

    def _export_json(self, proof: ContinuityProof, output_path: str = None) -> str:
        """Export proof to JSON format."""
        if not output_path:
            output_path = self.proof_path
        
        proof_dict = asdict(proof)
        # Convert entries to dict format
        proof_dict['entries'] = [asdict(entry) for entry in proof.entries]
        
        with open(output_path, 'w') as f:
            json.dump(proof_dict, f, indent=2)
        
        logger.info(f"Exported proof to JSON: {output_path}")
        return output_path

    def _export_markdown(self, proof: ContinuityProof, output_path: str = None) -> str:
        """Export proof to Markdown format."""
        if not output_path:
            output_path = self.proof_path.with_suffix('.md')
        
        with open(output_path, 'w') as f:
            f.write("# SentraAGI Proof of Continuity\n\n")
            f.write(f"**Generated:** {time.ctime(proof.generated_at)}\n\n")
            f.write(f"**Genesis Hash:** `{proof.genesis_hash}`\n\n")
            f.write(f"**Final Hash:** `{proof.final_hash}`\n\n")
            f.write(f"**Chain Integrity:** {'✅' if proof.chain_integrity else '❌'}\n\n")
            f.write(f"**Total Phases:** {proof.total_phases}\n\n")
            f.write(f"**Total Mutations:** {proof.total_mutations}\n\n")
            f.write(f"**Total Rollbacks:** {proof.total_rollbacks}\n\n")
            
            f.write("## Mutation Chain\n\n")
            for i, entry in enumerate(proof.entries):
                f.write(f"### Entry {i+1}: {entry.mutation_type}\n\n")
                f.write(f"- **Phase:** {entry.phase}\n")
                f.write(f"- **Timestamp:** {time.ctime(entry.timestamp)}\n")
                f.write(f"- **Hash:** `{entry.mutation_hash}`\n")
                f.write(f"- **Parent:** `{entry.parent_hash}`\n")
                f.write(f"- **Description:** {entry.description}\n")
                if entry.metadata:
                    f.write(f"- **Metadata:** {json.dumps(entry.metadata, indent=2)}\n")
                f.write("\n")
        
        logger.info(f"Exported proof to Markdown: {output_path}")
        return str(output_path)

    def get_proof_summary(self) -> Dict[str, Any]:
        """Get a summary of the current proof."""
        proof = self.generate_proof()
        return {
            "total_entries": len(proof.entries),
            "total_phases": proof.total_phases,
            "total_mutations": proof.total_mutations,
            "total_rollbacks": proof.total_rollbacks,
            "chain_integrity": proof.chain_integrity,
            "genesis_hash": proof.genesis_hash,
            "final_hash": proof.final_hash
        }


def main():
    """Example usage of ProofOfContinuity."""
    proof_gen = ProofOfContinuity()
    
    # Add some example mutations
    proof_gen.add_mutation("Phase 1", "initialization", "SentraAGI genesis", {"version": "1.0"})
    proof_gen.add_mutation("Phase 19", "perception", "Synthetic perception expansion", {"modules": ["VirtualSenses", "VisionAgent"]})
    proof_gen.add_mutation("Phase 20", "sovereignty", "Sovereign singularity core", {"components": ["OmegaReflector", "NeuroForge"]})
    proof_gen.add_mutation("Phase 21", "immutability", "Final sovereign trials", {"ledger": "ImmutableLedger"})
    
    # Generate and export proof
    proof = proof_gen.generate_proof()
    print(f"Proof generated: {proof.total_mutations} mutations, integrity: {proof.chain_integrity}")
    
    # Export to JSON and Markdown
    json_path = proof_gen.export_proof("json")
    md_path = proof_gen.export_proof("markdown")
    print(f"Exported to: {json_path}, {md_path}")
    
    # Get summary
    summary = proof_gen.get_proof_summary()
    print(f"Summary: {summary}")


if __name__ == "__main__":
    main() 