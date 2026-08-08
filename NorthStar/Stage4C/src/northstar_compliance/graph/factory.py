from __future__ import annotations

from pathlib import Path

from northstar_compliance.approval.service import ApprovalService
from northstar_compliance.approval.token import ApprovalTokenService
from northstar_compliance.durable.store import DurableStore
from northstar_compliance.graph.runtime import DurableGraphRuntime
from northstar_compliance.tools.gateway import ToolGateway


def build_graph_runtime(db_path: str | Path, approval_secret: bytes, *, approval_ttl_seconds: int = 3600) -> DurableGraphRuntime:
    store = DurableStore(db_path)
    gateway = ToolGateway(store)
    approvals = ApprovalService(store, ApprovalTokenService(approval_secret))
    return DurableGraphRuntime(store, gateway, approvals, approval_ttl_seconds=approval_ttl_seconds)
