from zenml import step
from planner.goal_manager import GoalManager
from planner.planner_engine import PlannerEngine
from taskloop.auto_loop import AutoLoop

@step(enable_cache=False)
def taskloop_step(agents=None, plugins=None, loop_interval: float = 2.0) -> None:
    """
    ZenML pipeline step to initialize and run the OMNIMIND Autonomous Task Loop.
    This step can be versioned and orchestrated as part of a ZenML pipeline.
    Args:
        agents: List of agent instances to use.
        plugins: List of plugins to use.
        loop_interval: Loop interval in seconds.
    """
    goal_manager = GoalManager()
    planner = PlannerEngine()
    loop = AutoLoop(goal_manager, planner, agents=agents, plugins=plugins, loop_interval=loop_interval)
    loop.start()
    # Let the loop run for a short time for demonstration (in real use, this would run indefinitely)
    import time
    time.sleep(5)
    loop.stop() 