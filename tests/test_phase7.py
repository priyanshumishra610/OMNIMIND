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
    """Test logging and hashability of supervisor actions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = os.path.join(tmpdir, "supervisor.jsonl")
        logger = SupervisorLogger(log_path=log_path)
        h = logger.log("test_action", {"foo": "bar"})
        assert isinstance(h, str) and len(h) == 64

def test_supervisor_core_status_and_control():
    """Test SupervisorCore status, metrics, and control interface."""
    sup = SupervisorCore(agents=[DummyAgent()])
    tid = sup.submit_task({"name": "coretask"})
    status = sup.get_status()
    assert status["active_agents"] == 1
    assert status["active_tasks"] >= 1
    metrics = sup.get_metrics()
    assert "system_health" in metrics
    res = sup.control("pause", {"task_id": tid})
    assert res["status"] == "paused" 