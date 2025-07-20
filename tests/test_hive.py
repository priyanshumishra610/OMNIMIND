from hive.agent_node import AgentNode
from hive.hive_controller import HiveController
from hive.hive_monitor import HiveMonitor
from hive.hive_registry import HiveRegistry
from hive.hive_comm import HiveComm
from logger.hive_logger import HiveLogger
from supervisor.hive_supervisor import HiveSupervisor
import time

def test_agent_node_heartbeat():
    """Test AgentNode sends heartbeat to HiveMonitor."""
    monitor = HiveMonitor(timeout=0.2)
    node = AgentNode("node1", monitor=monitor)
    node.start()
    time.sleep(0.3)
    node.stop()
    heartbeats = monitor.get_heartbeats()
    assert "node1" in heartbeats
    assert monitor.detect_dead_nodes()["dead_nodes"] == []
    time.sleep(0.3)
    assert "node1" in monitor.detect_dead_nodes()["dead_nodes"]

def test_hive_controller_spawn_and_assign():
    """Test HiveController spawns nodes and assigns tasks."""
    controller = HiveController()
    node = object()
    controller.spawn_node(node)
    assert node in controller.get_nodes()
    controller.assign_task({"id": "t1"})
    assert any(t["id"] == "t1" for t in controller.get_tasks())

def test_hive_registry_track_nodes_tasks():
    """Test HiveRegistry tracks nodes and tasks."""
    registry = HiveRegistry()
    registry.register_node("n1", object())
    registry.register_task("t1", {"status": "pending"})
    assert "n1" in registry.get_nodes()
    assert "t1" in registry.get_tasks()
    registry.update_task("t1", "done")
    assert registry.tasks["t1"]["status"] == "done"
    registry.unregister_node("n1")
    assert "n1" not in registry.get_nodes()

def test_hive_comm_send_receive():
    """Test HiveComm sends and receives messages."""
    comm = HiveComm()
    comm.send_message("a", "b", "hello")
    msgs = comm.receive_messages("b")
    assert any(m["content"] == "hello" for m in msgs)
    assert comm.receive_messages("b") == []

def test_hive_logger_hash():
    """Test HiveLogger logs and hashes entries."""
    logger = HiveLogger(log_path="logs/test_hive_logger.jsonl")
    h = logger.log("test", {"foo": "bar"})
    assert isinstance(h, str) and len(h) == 64

def test_hive_supervisor_stub():
    """Test HiveSupervisor stub methods."""
    supervisor = HiveSupervisor()
    supervisor.start()
    assert supervisor.status()["status"] == "ok"
    supervisor.stop()
    supervisor.assign_task_to_node({"id": "t1"}, "n1")
    assert supervisor.get_node_statuses() == [] 