import json
import pytest
from northstar_compliance.agent.models import AgentGoal, AgentRunState
from northstar_compliance.state.checkpoint import CheckpointError, LocalCheckpointStore


def test_091_checkpoint_round_trip(tmp_path):
    store = LocalCheckpointStore(tmp_path)
    state = AgentRunState("1.1.0", "RUN-1", "AGT-001", AgentGoal("G", "P", "O"))
    store.save(state)
    loaded = store.load("RUN-1")
    assert loaded.run_id == "RUN-1"
    assert loaded.resumed_from_checkpoint is True


def test_092_checkpoint_tamper_detected(tmp_path):
    store = LocalCheckpointStore(tmp_path)
    state = AgentRunState("1.1.0", "RUN-2", "AGT-001", AgentGoal("G", "P", "O"))
    path = store.save(state)
    data = json.loads(path.read_text())
    data["state"]["agent_id"] = "AGT-999"
    path.write_text(json.dumps(data))
    with pytest.raises(CheckpointError, match="checksum"):
        store.load("RUN-2")
