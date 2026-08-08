from __future__ import annotations

from pathlib import Path

from northstar_compliance.approval.service import ApprovalService
from northstar_compliance.approval.token import ApprovalTokenService
from northstar_compliance.durable.store import DurableStore
from northstar_compliance.graph.definition import load_graph
from northstar_compliance.graph.runtime import DurableGraphRuntime
from northstar_compliance.tools.gateway import ToolGateway


def build_runtime(db_path: str | Path, *, secret: bytes = b"stage4b-local-demo-secret-32-bytes-minimum!!",
                  wait_timeout_seconds: int = 3600, lease_seconds: int = 30) -> DurableGraphRuntime:
    root = Path(__file__).resolve().parents[3]
    graph = load_graph(root / "config/graph/stage4b-regulatory-impact-graph.json")
    store = DurableStore(db_path)
    tokens = ApprovalTokenService(secret)
    approvals = ApprovalService(store, tokens)
    return DurableGraphRuntime(
        graph=graph, store=store, gateway=ToolGateway(store), approvals=approvals,
        wait_timeout_seconds=wait_timeout_seconds, lease_seconds=lease_seconds,
    )
