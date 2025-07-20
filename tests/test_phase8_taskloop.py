from planner.goal_manager import GoalManager
from planner.planner_engine import PlannerEngine
from taskloop.auto_loop import AutoLoop
from taskloop.watchdog import Watchdog
import time

class DummyAgent:
    def __init__(self):
        self.handled = []
    def handle_task(self, task):
        self.handled.append(task)
        task["handled_by"] = "dummy"

class DummyPlugin:
    def __init__(self):
        self.handled = []
    def handle_task(self, task):
        self.handled.append(task)
        task["handled_by"] = "plugin"

def test_goal_manager_crud():
    """Test CRUD operations and history in GoalManager."""
    gm = GoalManager()
    gid = gm.create_goal("Test goal.")
    assert gid in gm.goals
    gm.update_goal(gid, status="in_progress")
    assert gm.goals[gid]["status"] == "in_progress"
    hist = gm.get_history(gid)
    assert any(h["action"] == "update" for h in hist)
    gm.delete_goal(gid)
    assert gid not in gm.goals

def test_planner_engine_plan_and_update():
    """Test planning and task status update in PlannerEngine."""
    gm = GoalManager()
    pe = PlannerEngine()
    gid = gm.create_goal("Do A. Then do B.")
    goal = gm.get_goal(gid)
    plan = pe.plan_goal(goal)
    assert len(plan["tasks"]) == 2
    tid = plan["tasks"][0]["task_id"]
    assert pe.update_task_status(gid, tid, "completed")
    assert plan["tasks"][0]["status"] == "completed"

def test_auto_loop_executes_tasks():
    """Test that AutoLoop executes tasks and marks goals complete."""
    gm = GoalManager()
    pe = PlannerEngine()
    agent = DummyAgent()
    gid = gm.create_goal("Task 1. Task 2.")
    loop = AutoLoop(gm, pe, agents=[agent], loop_interval=0.1)
    loop.start()
    time.sleep(0.5)
    loop.stop()
    goal = gm.get_goal(gid)
    assert goal["status"] == "completed"
    plan = pe.get_plan(gid)
    assert all(t["status"] == "completed" for t in plan["tasks"])
    assert len(agent.handled) >= 2

def test_watchdog_restarts_loop():
    """Test that Watchdog restarts the loop if unhealthy."""
    class Loop:
        def __init__(self):
            self.started = 0
            self.healthy = False
        def start(self):
            self.started += 1
            self.healthy = True
        def stop(self):
            self.healthy = False
    loop = Loop()
    def check(): return loop.healthy
    def restart(): loop.start()
    wd = Watchdog(check, restart, interval=0.1, max_failures=2)
    loop.stop()
    wd.start()
    time.sleep(0.3)
    wd.stop()
    assert loop.started >= 1 