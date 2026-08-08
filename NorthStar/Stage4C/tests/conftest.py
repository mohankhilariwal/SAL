from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from northstar_compliance.harness.context import ContextSource
from northstar_compliance.harness.factory import build_harness
from northstar_compliance.harness.runtime import HarnessRequest


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def now() -> datetime:
    return datetime(2026, 7, 31, 20, 0, tzinfo=timezone.utc)


@pytest.fixture
def harness(tmp_path: Path, repo_root: Path):
    return build_harness(
        repository_root=repo_root,
        runtime_root=tmp_path / "runtime",
        approval_secret=b"stage4c-test-secret-material-32-bytes-minimum",
        approval_ttl_seconds=60,
    )


@pytest.fixture
def harness_request() -> HarnessRequest:
    return HarnessRequest(
        initiator_id="maya.chen",
        context_sources=[
            ContextSource("PUB-001", "publication", "PUBLIC", "regulatory_analysis", True, 1, lambda: "Regulatory publication text."),
            ContextSource("EVID-001", "evidence", "INTERNAL", "regulatory_analysis", True, 2, lambda: "Authorized NorthStar policy evidence."),
        ],
    )
