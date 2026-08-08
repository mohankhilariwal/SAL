from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from northstar_compliance.specification.canonical import sha256_digest
from northstar_compliance.specification.models import AgentSpecification


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def raw_spec(repo_root: Path) -> dict:
    return json.loads((repo_root / "config/agents/AGT-001.spec.json").read_text(encoding="utf-8"))


@pytest.fixture
def specification(raw_spec: dict) -> AgentSpecification:
    return AgentSpecification(raw=copy.deepcopy(raw_spec), digest=sha256_digest(raw_spec))


@pytest.fixture
def manifest(repo_root: Path) -> dict:
    return json.loads((repo_root / "config/harness/harness-manifest.json").read_text(encoding="utf-8"))


@pytest.fixture
def valid_context() -> dict:
    return {
        "envelope_id": "CTX-001",
        "items": [
            {
                "source_id": "PUB-001",
                "kind": "publication",
                "authorized": True,
                "content": "Synthetic publication content",
                "content_sha256": "a" * 64,
            },
            {
                "source_id": "EVID-001",
                "kind": "evidence",
                "authorized": True,
                "content": "Authorized policy evidence",
                "content_sha256": "b" * 64,
            },
        ],
    }


@pytest.fixture
def completed_result() -> dict:
    return {
        "status": "completed",
        "review_outcome": "approved",
        "final_disposition": "preliminary_grounded_human_approved",
        "tool006_effects": 1,
        "final_legal_or_compliance_closure": False,
    }
