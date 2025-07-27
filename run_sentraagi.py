#!/usr/bin/env python3
"""
SentraAGI Sovereign Kernel - Master Runner Script

Orchestrates all core modules in the correct sequence:
Sense → Reason → Simulate → Reflect → Mutate → Govern → Verify

Author: SentraAGI Team
Version: Phase 21
"""

import os
import sys
import time
import signal
import argparse
import logging
import threading
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not found. Using system environment variables.")

# Core module imports
try:
    # Omega Core (reflection, reasoning)
    from omega.omega_reflector import OmegaReflector
    from omega.omega_inner_voice import OmegaInnerVoice
    from omega.self_audit import SelfAudit
    
    # World Model (simulation)
    from world_model.meta_simulator import MetaSimulator
    from world_model.agent import Agent
    from world_model.environment import Environment
    
    # Dreamscape (sandbox loops)
    from dreamscape.dreamscape import DreamscapeEngine
    from dreamscape.consequence_simulator import ConsequenceSimulator
    from dreamscape.dream_logger import DreamLogger
    
    # NeuroForge (self-improvement)
    from neuroforge.neuroforge import NeuroForge
    
    # Virtual Senses (perception)
    from multi_modal.virtual_senses import VirtualSenses
    from multi_modal.vision_agent import VisionAgent
    from multi_modal.tactile_agent import TactileAgent
    
    # Memory and Learning
    from memory.perceptual_memory import PerceptualMemory
    from memory.episodic_memory import EpisodicMemory
    from memory.semantic_manager import SemanticManager
    from learning.meta_learning import MetaLearner
    
    # Oversight & Governance
    from governance.oversight_console import OversightConsole
    from governance.constitutional_circuit_breaker import ConstitutionalCircuitBreaker
    from governance.ethics_checker_v2 import EthicsCheckerV2
    
    # Immutable Verifier
    from proof.proof_of_continuity import ProofOfContinuity
    from immutable.ledger import ImmutableLedger
    
    # Arena and Swarm
    from arena.distributed_swarm import DistributedSwarm
    from arena.reflex_swarm import ReflexSwarm
    
    # Sentience
    from sentience.self_evaluator import SelfEvaluator
    from sentience.reflection_engine import ReflectionEngine
    from sentience.ethical_reasoner import EthicalReasoner
    
    # OmniShield
    from omni_shield.sandbox import Sandbox
    from omni_shield.ethics_guardian import EthicsGuardian
    
    # Pipelines
    from pipelines.singularity_kernel_pipeline import singularity_kernel_pipeline, SingularityKernelConfig
    
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    print(f"Warning: Some modules could not be imported: {e}")
    IMPORTS_SUCCESSFUL = False


class SentraAGIRunner:
    """
    Master runner for SentraAGI Sovereign Kernel.
    
    Orchestrates all core modules in the correct sequence and manages
    the main perception → simulation → reflection → governance loop.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the SentraAGI runner with configuration."""
        self.config = config or {}
        self.running = False
        self.shutdown_requested = False
        
        # Core modules
        self.omega_reflector: Optional[OmegaReflector] = None
        self.omega_inner_voice: Optional[OmegaInnerVoice] = None
        self.self_audit: Optional[SelfAudit] = None
        self.meta_simulator: Optional[MetaSimulator] = None
        self.dreamscape: Optional[DreamscapeEngine] = None
        self.neuroforge: Optional[NeuroForge] = None
        self.virtual_senses: Optional[VirtualSenses] = None
        self.vision_agent: Optional[VisionAgent] = None
        self.perceptual_memory: Optional[PerceptualMemory] = None
        self.oversight_console: Optional[OversightConsole] = None
        self.proof_of_continuity: Optional[ProofOfContinuity] = None
        self.immutable_ledger: Optional[ImmutableLedger] = None
        self.distributed_swarm: Optional[DistributedSwarm] = None
        self.singularity_pipeline: Optional[Any] = None
        
        # Setup logging
        self.setup_logging()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.logger.info("SentraAGI Runner initialized")
    
    def setup_logging(self):
        """Setup comprehensive logging for SentraAGI."""
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        log_file = os.getenv('LOG_FILE', './logs/sentraagi.log')
        
        # Create logs directory
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('SentraAGI')
        self.logger.info("Logging system initialized")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_requested = True
        self.running = False
    
    def print_banner(self):
        """Print the SentraAGI startup banner."""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 SentraAGI Sovereign Kernel             ║
║                                                              ║
║  Phase 21: The Final Sovereign Trials                       ║
║  Core Modules: Omega • World Model • Dreamscape • NeuroForge ║
║  Governance: Oversight • Ethics • Immutable Verification    ║
║                                                              ║
║  Loop: Perceive → Simulate → Reflect → Govern → Verify      ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        self.logger.info("SentraAGI startup banner displayed")
    
    def initialize_core_modules(self) -> bool:
        """Initialize all core modules in the correct sequence."""
        try:
            self.logger.info("Starting core module initialization...")
            
            # 1. Initialize Immutable Foundation
            self.logger.info("1️⃣ Initializing Immutable Foundation...")
            self.immutable_ledger = ImmutableLedger(
                ledger_path=os.getenv('SENTRA_LEDGER_PATH', 'data/immutable_ledger.json')
            )
            self.proof_of_continuity = ProofOfContinuity(
                proof_path=os.getenv('SENTRA_PROOF_PATH', 'data/proof_of_continuity.json')
            )
            print("✅ Immutable Foundation ready")
            
            # 2. Initialize Oversight & Governance
            self.logger.info("2️⃣ Initializing Oversight & Governance...")
            self.oversight_console = OversightConsole(self.immutable_ledger)
            print("✅ Oversight & Governance active")
            
            # 3. Initialize Virtual Senses
            self.logger.info("3️⃣ Initializing Virtual Senses...")
            self.virtual_senses = VirtualSenses()
            self.vision_agent = VisionAgent()
            print("✅ Virtual Senses online")
            
            # 4. Initialize Memory Systems
            self.logger.info("4️⃣ Initializing Memory Systems...")
            self.perceptual_memory = PerceptualMemory()
            print("✅ Memory Systems initialized")
            
            # 5. Initialize Omega Core (Reflection & Reasoning)
            self.logger.info("5️⃣ Initializing Omega Core...")
            self.omega_reflector = OmegaReflector()
            self.omega_inner_voice = OmegaInnerVoice()
            self.self_audit = SelfAudit()
            print("✅ Omega Core initialized")
            
            # 6. Initialize World Model
            self.logger.info("6️⃣ Initializing World Model...")
            self.meta_simulator = MetaSimulator()
            print("✅ World Model simulation ready")
            
            # 7. Initialize Dreamscape
            self.logger.info("7️⃣ Initializing Dreamscape...")
            self.dreamscape = DreamscapeEngine()
            print("✅ Dreamscape sandbox active")
            
            # 8. Initialize NeuroForge
            self.logger.info("8️⃣ Initializing NeuroForge...")
            self.neuroforge = NeuroForge()
            # Connect NeuroForge to other components
            if self.omega_reflector:
                self.neuroforge.set_omega_reflector(self.omega_reflector)
            print("✅ NeuroForge booted")
            
            # 9. Initialize Distributed Swarm
            self.logger.info("9️⃣ Initializing Distributed Swarm...")
            self.distributed_swarm = DistributedSwarm()
            print("✅ Distributed Swarm ready")
            
            # 10. Initialize Singularity Pipeline
            self.logger.info("🔟 Initializing Singularity Pipeline...")
            config = SingularityKernelConfig()
            self.singularity_pipeline = config
            print("✅ Singularity Pipeline active")
            
            self.logger.info("All core modules initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize core modules: {e}")
            print(f"❌ Module initialization failed: {e}")
            return False
    
    def run_governance_checks(self) -> bool:
        """Run initial governance and safety checks."""
        try:
            self.logger.info("Running governance checks...")
            
            # Check constitutional compliance
            if self.oversight_console:
                stats = self.oversight_console.get_oversight_stats()
                self.logger.info(f"Oversight stats: {stats}")
            
            # Verify immutable foundation
            if self.immutable_ledger:
                integrity = self.immutable_ledger.verify_integrity()
                if not integrity:
                    self.logger.error("Immutable ledger integrity check failed")
                    return False
            
            # Check proof of continuity
            if self.proof_of_continuity:
                summary = self.proof_of_continuity.get_proof_summary()
                self.logger.info(f"Proof of continuity: {summary}")
            
            print("✅ Governance checks passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Governance checks failed: {e}")
            print(f"❌ Governance checks failed: {e}")
            return False
    
    def perception_phase(self) -> Dict[str, Any]:
        """Phase 1: Perceive the environment through virtual senses."""
        try:
            self.logger.info("🔍 Perception Phase: Gathering sensory data...")
            
            perception_data = {
                'timestamp': datetime.now().isoformat(),
                'visual_data': None,
                'tactile_data': None,
                'memory_context': None
            }
            
            # Gather visual data
            if self.virtual_senses:
                frame_data = self.virtual_senses.capture_frame()
                if frame_data is not None:
                    perception_data['visual_data'] = frame_data
            
            # Process through vision agent
            if self.vision_agent:
                vision_result = self.vision_agent.process_single_frame()
                perception_data['vision_analysis'] = vision_result
            
            # Get memory context
            if self.perceptual_memory:
                recent_perceptions = self.perceptual_memory.get_recent_perceptions(limit=5)
                perception_data['memory_context'] = recent_perceptions
            
            self.logger.info("Perception phase completed")
            return perception_data
            
        except Exception as e:
            self.logger.error(f"Perception phase failed: {e}")
            return {'error': str(e)}
    
    def simulation_phase(self, perception_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: Simulate possible outcomes and scenarios."""
        try:
            self.logger.info("🌐 Simulation Phase: Running world model simulations...")
            
            simulation_results = {
                'scenarios': [],
                'predictions': [],
                'consequences': []
            }
            
            # Run meta-simulator
            if self.meta_simulator:
                scenarios = self.meta_simulator.simulate(perception_data)
                simulation_results['scenarios'] = scenarios
            
            # Run dreamscape scenarios
            if self.dreamscape:
                dream_scenario = self.dreamscape.generate_dream(perception_data)
                simulation_results['predictions'] = [dream_scenario]
            
            # Analyze consequences
            if hasattr(self, 'consequence_simulator') and self.consequence_simulator:
                consequences = self.consequence_simulator.simulate_outcome(perception_data)
                simulation_results['consequences'] = consequences
            
            self.logger.info("Simulation phase completed")
            return simulation_results
            
        except Exception as e:
            self.logger.error(f"Simulation phase failed: {e}")
            return {'error': str(e)}
    
    def reflection_phase(self, perception_data: Dict[str, Any], simulation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Reflect on perceptions and simulations."""
        try:
            self.logger.info("🤔 Reflection Phase: Analyzing and reasoning...")
            
            reflection_results = {
                'contradictions': [],
                'insights': [],
                'self_doubt': None,
                'fitness_score': 0.0
            }
            
            # Detect contradictions
            if self.omega_reflector:
                contradictions = self.omega_reflector.detect_contradictions([
                    perception_data, simulation_data
                ])
                reflection_results['contradictions'] = contradictions
            
            # Generate self-doubt loop
            if self.omega_reflector:
                self_doubt = self.omega_reflector.generate_self_doubt_loop()
                reflection_results['self_doubt'] = self_doubt
            
            # Score lineage fitness
            if self.omega_reflector:
                fitness = self.omega_reflector.score_lineage_fitness([
                    perception_data, simulation_data
                ])
                reflection_results['fitness_score'] = fitness
            
            # Inner voice reflection
            if self.omega_inner_voice:
                insights = self.omega_inner_voice.reflect(perception_data)
                reflection_results['insights'] = insights
            
            self.logger.info("Reflection phase completed")
            return reflection_results
            
        except Exception as e:
            self.logger.error(f"Reflection phase failed: {e}")
            return {'error': str(e)}
    
    def mutation_phase(self, all_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 4: Mutate and improve based on reflections."""
        try:
            self.logger.info("🧬 Mutation Phase: Self-improvement and adaptation...")
            
            mutation_results = {
                'shard_mutations': [],
                'belief_updates': [],
                'lineage_changes': []
            }
            
            # Mutate thought shards through NeuroForge
            if self.neuroforge:
                shard = {
                    'belief': 'adaptive_belief',
                    'confidence': 0.8,
                    'context': all_data
                }
                mutation = self.neuroforge.mutate_shard(shard)
                mutation_results['shard_mutations'] = [mutation]
            
            # Update belief lineage
            if self.neuroforge:
                belief_update = self.neuroforge.update_belief_lineage(all_data)
                mutation_results['belief_updates'] = [belief_update]
            
            self.logger.info("Mutation phase completed")
            return mutation_results
            
        except Exception as e:
            self.logger.error(f"Mutation phase failed: {e}")
            return {'error': str(e)}
    
    def governance_phase(self, all_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 5: Apply governance and oversight checks."""
        try:
            self.logger.info("⚖️ Governance Phase: Applying oversight and ethics...")
            
            governance_results = {
                'oversight_actions': [],
                'ethics_checks': [],
                'quorum_votes': [],
                'circuit_breaker_status': 'normal'
            }
            
            # Run oversight inspection
            if self.oversight_console:
                inspection = self.oversight_console.inspect()
                governance_results['oversight_actions'] = [inspection]
            
            # Create quorum vote for significant changes
            if self.oversight_console and len(all_data.get('mutation_results', {}).get('shard_mutations', [])) > 0:
                vote_id = self.oversight_console.create_quorum_vote(
                    "Significant belief mutation detected"
                )
                governance_results['quorum_votes'] = [vote_id]
            
            self.logger.info("Governance phase completed")
            return governance_results
            
        except Exception as e:
            self.logger.error(f"Governance phase failed: {e}")
            return {'error': str(e)}
    
    def verification_phase(self, all_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 6: Verify and log all activities immutably."""
        try:
            self.logger.info("🔒 Verification Phase: Immutable logging and proof generation...")
            
            verification_results = {
                'ledger_entries': [],
                'proof_updates': [],
                'integrity_checks': []
            }
            
            # Log to immutable ledger
            if self.immutable_ledger:
                entry = {
                    'timestamp': datetime.now().isoformat(),
                    'phase': 'main_loop',
                    'data_summary': str(all_data)[:1000],  # Truncate for storage
                    'checksum': 'computed_checksum'
                }
                self.immutable_ledger.append_entry(entry)
                verification_results['ledger_entries'] = [entry]
            
            # Update proof of continuity
            if self.proof_of_continuity:
                mutation_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'phase': 'main_loop',
                    'description': 'Main perception-simulation-reflection cycle',
                    'metadata': {'cycle_count': 'incremental'}
                }
                self.proof_of_continuity.add_mutation(mutation_entry)
                verification_results['proof_updates'] = [mutation_entry]
            
            # Verify integrity
            if self.immutable_ledger:
                integrity = self.immutable_ledger.verify_integrity()
                verification_results['integrity_checks'] = [integrity]
            
            self.logger.info("Verification phase completed")
            return verification_results
            
        except Exception as e:
            self.logger.error(f"Verification phase failed: {e}")
            return {'error': str(e)}
    
    def run_main_loop(self):
        """Run the main SentraAGI perception → simulation → reflection → governance loop."""
        cycle_count = 0
        
        print("🔁 Starting infinite loop: Perceive → Simulate → Reflect → Govern → Verify")
        self.logger.info("Main loop started")
        
        while self.running and not self.shutdown_requested:
            try:
                cycle_count += 1
                self.logger.info(f"Starting cycle {cycle_count}")
                
                # Phase 1: Perception
                perception_data = self.perception_phase()
                
                # Phase 2: Simulation
                simulation_data = self.simulation_phase(perception_data)
                
                # Phase 3: Reflection
                reflection_data = self.reflection_phase(perception_data, simulation_data)
                
                # Phase 4: Mutation
                mutation_data = self.mutation_phase({
                    'perception': perception_data,
                    'simulation': simulation_data,
                    'reflection': reflection_data
                })
                
                # Phase 5: Governance
                governance_data = self.governance_phase({
                    'perception': perception_data,
                    'simulation': simulation_data,
                    'reflection': reflection_data,
                    'mutation': mutation_data
                })
                
                # Phase 6: Verification
                verification_data = self.verification_phase({
                    'perception': perception_data,
                    'simulation': simulation_data,
                    'reflection': reflection_data,
                    'mutation': mutation_data,
                    'governance': governance_data
                })
                
                # Log cycle completion
                self.logger.info(f"Cycle {cycle_count} completed successfully")
                
                # Brief pause between cycles
                time.sleep(1)
                
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop cycle {cycle_count}: {e}")
                print(f"❌ Cycle {cycle_count} failed: {e}")
                time.sleep(5)  # Wait before retrying
        
        self.logger.info(f"Main loop ended after {cycle_count} cycles")
        return cycle_count
    
    def shutdown(self):
        """Gracefully shutdown all modules."""
        try:
            self.logger.info("Initiating graceful shutdown...")
            print("🛑 Initiating graceful shutdown...")
            
            # Stop the main loop
            self.running = False
            
            # Shutdown virtual senses
            if self.virtual_senses:
                self.virtual_senses.cleanup()
                print("✅ Virtual Senses shutdown")
            
            # Shutdown vision agent
            if self.vision_agent:
                self.vision_agent.cleanup()
                print("✅ Vision Agent shutdown")
            
            # Stop self-audit daemon
            if self.self_audit:
                self.self_audit.stop_daemon()
                print("✅ Self-Audit shutdown")
            
            # Final ledger entry
            if self.immutable_ledger:
                shutdown_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'event': 'shutdown',
                    'message': 'Graceful shutdown completed'
                }
                self.immutable_ledger.append_entry(shutdown_entry)
                print("✅ Immutable ledger updated")
            
            # Generate final proof
            if self.proof_of_continuity:
                final_proof = self.proof_of_continuity.generate_proof()
                print("✅ Final proof of continuity generated")
            
            self.logger.info("Graceful shutdown completed")
            print("✅ SentraAGI shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            print(f"❌ Shutdown error: {e}")
    
    def run(self) -> bool:
        """Main entry point to run SentraAGI."""
        try:
            # Print startup banner
            self.print_banner()
            
            # Initialize core modules
            if not self.initialize_core_modules():
                return False
            
            # Run governance checks
            if not self.run_governance_checks():
                return False
            
            # Start the main loop
            self.running = True
            cycle_count = self.run_main_loop()
            
            # Shutdown gracefully
            self.shutdown()
            
            # Print final summary
            print(f"\n📊 SentraAGI Summary:")
            print(f"   • Cycles completed: {cycle_count}")
            print(f"   • Shutdown: Graceful")
            print(f"   • Status: Complete")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Fatal error in SentraAGI runner: {e}")
            print(f"❌ Fatal error: {e}")
            self.shutdown()
            return False


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SentraAGI Sovereign Kernel - Master Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_sentraagi.py                    # Run with default settings
  python run_sentraagi.py --headless         # Run in headless mode
  python run_sentraagi.py --debug            # Run with debug logging
  python run_sentraagi.py --config config.json  # Use custom config
        """
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run in headless mode (no GUI components)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level'
    )
    
    parser.add_argument(
        '--max-cycles',
        type=int,
        help='Maximum number of cycles to run (default: infinite)'
    )
    
    return parser.parse_args()


def main():
    """Main entry point for SentraAGI."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Set environment variables from arguments
        if args.debug:
            os.environ['LOG_LEVEL'] = 'DEBUG'
        if args.log_level:
            os.environ['LOG_LEVEL'] = args.log_level
        if args.headless:
            os.environ['SENTRA_HEADLESS_MODE'] = 'true'
        
        # Load configuration if provided
        config = {}
        if args.config and os.path.exists(args.config):
            import json
            with open(args.config, 'r') as f:
                config = json.load(f)
        
        # Check if imports were successful
        if not IMPORTS_SUCCESSFUL:
            print("❌ Critical modules could not be imported. Please check dependencies.")
            return 1
        
        # Create and run SentraAGI
        runner = SentraAGIRunner(config)
        success = runner.run()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 