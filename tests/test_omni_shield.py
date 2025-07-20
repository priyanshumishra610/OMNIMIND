from omni_shield.sandbox import Sandbox
from omni_shield.permission_manager import PermissionManager
from omni_shield.ethics_guardian import EthicsGuardian
from omni_shield.output_verifier import OutputVerifier
from omni_shield.intrusion_detector import IntrusionDetector
from logger.shield_logger import ShieldLogger

def test_sandbox_blocks_unsafe():
    """Test Sandbox blocks unsafe sys ops (stub)."""
    sandbox = Sandbox()
    result = sandbox.execute("import os\nos.system('echo unsafe')")
    assert "error" in result
    safe = sandbox.execute("result = 2 + 2")
    assert safe == 4

def test_permission_manager():
    """Test PermissionManager enforces scopes."""
    pm = PermissionManager()
    pm.set_permission("user1", "read", True)
    assert pm.check_permission("user1", "read")
    pm.revoke_permission("user1", "read")
    assert not pm.check_permission("user1", "read")

def test_ethics_guardian():
    """Test EthicsGuardian checks output vs policy (stub)."""
    eg = EthicsGuardian(policy={"no_hate": True})
    result = eg.check_output("hello world")
    assert result["compliant"]

def test_output_verifier():
    """Test OutputVerifier fact-checks output (stub)."""
    ov = OutputVerifier()
    result = ov.verify("The sky is blue.")
    assert result["verified"]

def test_intrusion_detector():
    """Test IntrusionDetector records and detects suspicious events."""
    idet = IntrusionDetector()
    idet.record_event({"suspicious": True, "type": "syscall"})
    assert idet.detect_intrusion()
    assert idet.get_events()[0]["type"] == "syscall"

def test_shield_logger_hash():
    """Test ShieldLogger logs and hashes entries."""
    logger = ShieldLogger(log_path="logs/test_shield_logger.jsonl")
    h = logger.log("test", {"foo": "bar"})
    assert isinstance(h, str) and len(h) == 64 