from __future__ import annotations

from pathlib import Path

from .adapters import (
    AuthorizedEvidenceAdapter,
    CandidateMappingAdapter,
    ControlCatalogueAdapter,
    DraftCaseAdapter,
    RegulatoryCatalogueAdapter,
    ReviewQueueAdapter,
)
from .gateway import ToolGateway
from .policy import LocalToolPolicyEngine
from .registry import ToolRegistry
from .storage import LocalJsonStore


def build_tool_gateway(project_root: Path, artifact_root: Path) -> ToolGateway:
    registry = ToolRegistry.load(project_root / "config" / "tools")
    store = LocalJsonStore(artifact_root)
    adapters = {
        "TOOL-001": RegulatoryCatalogueAdapter(),
        "TOOL-002": ControlCatalogueAdapter(),
        "TOOL-003": AuthorizedEvidenceAdapter(),
        "TOOL-004": DraftCaseAdapter(store),
        "TOOL-005": CandidateMappingAdapter(store),
        "TOOL-006": ReviewQueueAdapter(store),
    }
    return ToolGateway(registry, LocalToolPolicyEngine(), adapters, store)
