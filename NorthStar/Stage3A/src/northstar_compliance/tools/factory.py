from __future__ import annotations

from pathlib import Path

from .adapters import (
    AuthorizedEvidenceSearchAdapter,
    CandidateMappingSaveAdapter,
    ControlCatalogueQueryAdapter,
    DraftCaseCreateAdapter,
    RegulatoryCatalogueSearchAdapter,
    ReviewRequestQueueAdapter,
)
from .events import JsonlToolEventWriter
from .gateway import ToolGateway
from .registry import ToolRegistry
from .storage import LocalToolStore


def build_local_gateway(
    registry_dir: Path,
    store_dir: Path,
    event_log_path: Path | None = None,
) -> tuple[ToolGateway, LocalToolStore]:
    registry = ToolRegistry.load(registry_dir)
    store = LocalToolStore(store_dir)
    adapters = {
        "TOOL-001": RegulatoryCatalogueSearchAdapter(),
        "TOOL-002": ControlCatalogueQueryAdapter(),
        "TOOL-003": AuthorizedEvidenceSearchAdapter(),
        "TOOL-004": DraftCaseCreateAdapter(store),
        "TOOL-005": CandidateMappingSaveAdapter(store),
        "TOOL-006": ReviewRequestQueueAdapter(store),
    }
    gateway = ToolGateway(
        registry,
        adapters,
        event_writer=JsonlToolEventWriter(event_log_path),
    )
    return gateway, store
