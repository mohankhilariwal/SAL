from pathlib import Path
import pytest

from northstar_compliance.agent.decision import DeterministicDecisionProvider
from northstar_compliance.agent.models import AgentGoal
from northstar_compliance.agent.runtime import AgentRuntime
from northstar_compliance.state.checkpoint import LocalCheckpointStore
from northstar_compliance.tools.gateway import Principal, ToolGateway
from northstar_compliance.tools.local_tools import FailureInjector, LocalStores, NorthStarLocalTools

@pytest.fixture
def goal():
    return AgentGoal("GOAL-TEST", "PUB-TEST", "Prepare package")

@pytest.fixture
def principal():
    return Principal("maya.chen")


def make_runtime(tmp_path: Path, plans=None, providers=None, no_progress_window=2, repeated_action_limit=2):
    stores = LocalStores()
    primary = NorthStarLocalTools(stores=stores, failures=FailureInjector(plans))
    fallback = NorthStarLocalTools(stores=stores, fallback=True)
    gateway = ToolGateway(
        {f"TOOL-{i:03d}": primary.adapter for i in range(1, 7)},
        {f"TOOL-{i:03d}": fallback.adapter for i in range(1, 4)},
    )
    runtime = AgentRuntime(
        gateway,
        providers or [DeterministicDecisionProvider()],
        LocalCheckpointStore(tmp_path / "checkpoints"),
        reconciler=primary.reconcile,
        no_progress_window=no_progress_window,
        repeated_action_limit=repeated_action_limit,
    )
    return runtime, primary, fallback
