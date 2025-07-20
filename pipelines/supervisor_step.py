from zenml import step
from supervisor.supervisor_core import SupervisorCore

@step(enable_cache=False)
def supervisor_step(agents=None, plugins=None) -> None:
    """
    ZenML pipeline step to initialize and run the OMNIMIND Supervisor Core.
    This step can be versioned and orchestrated as part of a ZenML pipeline.
    Args:
        agents: List of agent instances to supervise.
        plugins: List of plugins to load.
    """
    supervisor = SupervisorCore(agents=agents, plugins=plugins)
    supervisor.run() 