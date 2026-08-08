from __future__ import annotations

from pathlib import Path

from .decision import DeterministicDecisionProvider
from .runtime import AgentRuntime
from northstar_compliance.state.checkpoint import LocalCheckpointStore
from northstar_compliance.tools.gateway import ToolGateway
from northstar_compliance.tools.local_tools import LocalStores, NorthStarLocalTools


def build_local_runtime(base_dir: str | Path):
    base = Path(base_dir)
    stores = LocalStores()
    primary = NorthStarLocalTools(stores=stores)
    fallback = NorthStarLocalTools(stores=stores, fallback=True)
    gateway = ToolGateway(
        adapters={f"TOOL-{i:03d}": primary.adapter for i in range(1, 7)},
        fallback_adapters={f"TOOL-{i:03d}": fallback.adapter for i in range(1, 4)},
    )
    runtime = AgentRuntime(
        gateway,
        [DeterministicDecisionProvider()],
        LocalCheckpointStore(base / "checkpoints"),
        reconciler=primary.reconcile,
    )
    return runtime, primary, fallback
