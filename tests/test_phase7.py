import os
import tempfile
from supervisor.supervisor_core import SupervisorCore
from supervisor.task_manager import TaskManager
from supervisor.scheduler import Scheduler
from supervisor.interrupt_handler import InterruptHandler
from supervisor.logs.supervisor_logger import SupervisorLogger

class DummyAgent:
    def __init__(self):
        self.handled = []
    def handle_task(self, task):
        self.handled.append(task)
        task["handled_by"] = "dummy"

def test_task_manager():
    """Test adding, dispatching, and lineage of tasks."""
    tm = TaskManager()
    tid = tm.add_task({"name": "t1"})
    assert tid in tm.tasks
    agent = DummyAgent()
    tm.dispatch_tasks([agent])
    assert tm.tasks[tid]["status"] == "completed"
    tid2 = tm.add_task({"name": "t2"}, parent_id=tid)
    assert tm.get_lineage(tid2) == [tid]

def test_scheduler():
    """Test scheduling and watchdogs."""
    sch = Scheduler()
    tm = TaskManager()
    sch.schedule_task({"name": "scheduled"}, delay=0.01)
    sch.check_and_schedule(tm)
    import time; time.sleep(0.02)
    sch.check_and_schedule(tm)
    assert any(t["name"] == "scheduled" for t in tm.tasks.values())
    # Watchdog
    triggered = {"flag": False}
    sch.add_watchdog(lambda: False, lambda: triggered.update({"flag": True}))
    sch._run_watchdogs()
    assert triggered["flag"]

def test_interrupt_handler():
    """Test pausing, killing, and rerouting tasks."""
    tm = TaskManager()
    tid = tm.add_task({"name": "interrupt"})
    ih = InterruptHandler()
    ih.handle_command("pause", {"task_id": tid}, tm)
    ih.check_interrupts(tm)
    assert tm.tasks[tid]["status"] == "paused"
    ih.handle_command("kill", {"task_id": tid}, tm)
    ih.check_interrupts(tm)
    assert tm.tasks[tid]["status"] == "killed"
    ih.handle_command("reroute", {"task_id": tid}, tm)
    ih.check_interrupts(tm)
    assert tm.tasks[tid]["status"] == "pending"
    ih.handle_command("resume", {"task_id": tid}, tm)
    assert tm.tasks[tid]["status"] == "pending"

def test_supervisor_logger():
    """Test logging and structured output of supervisor actions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        logger = SupervisorLogger(log_dir=tmpdir)
        # Test different log levels
        logger.info("test info", {"foo": "bar"})
        logger.warning("test warning", {"alert": "high"})
        logger.error("test error", Exception("test exception"))
        logger.debug("test debug", {"detail": "verbose"})
        
        # Verify log file exists and has content
        log_file = os.path.join(tmpdir, "supervisor.log")
        assert os.path.exists(log_file)
        with open(log_file, 'r') as f:
            content = f.read()
            assert "test info" in content
            assert "test warning" in content
            assert "test error" in content
            assert "test exception" in content

def test_supervisor_core_status_and_control():
    """Test SupervisorCore status and component management."""
    sup = SupervisorCore()
    
    # Register a test component
    sup.register_component("test_component", {
        "type": "service",
        "health_check": lambda: True
    })
    
    # Start supervision
    sup.start_supervision()
    
    # Check component status
    status = sup.get_component_status("test_component")
    assert status is not None
    assert status["status"] in ["registered", "healthy"]
    
    # Get all statuses
    all_statuses = sup.get_all_statuses()
    assert "test_component" in all_statuses
    
    # Stop supervision
    sup.stop_supervision() 