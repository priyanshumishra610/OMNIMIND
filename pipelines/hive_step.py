from zenml import step
from hive.hive_controller import HiveController
from hive.hive_monitor import HiveMonitor
from hive.hive_registry import HiveRegistry
from hive.hive_comm import HiveComm
from logger.hive_logger import HiveLogger
from supervisor.hive_supervisor import HiveSupervisor

@step(enable_cache=False)
def hive_step() -> None:
    """
    ZenML pipeline step to initialize and run the OMNIMIND Hive orchestration.
    This step can be versioned and orchestrated as part of a ZenML pipeline.
    """
    controller = HiveController()
    monitor = HiveMonitor()
    registry = HiveRegistry()
    comm = HiveComm()
    logger = HiveLogger()
    supervisor = HiveSupervisor(controller, monitor, registry, logger)
    supervisor.start()
    # For demonstration, stop immediately (real use: would run indefinitely)
    supervisor.stop() 