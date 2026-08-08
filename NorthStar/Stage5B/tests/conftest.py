from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest

from northstar_compliance.memory import (
    CaseWorkingMemoryService,
    ContextCompactor,
    ContextRegenerator,
    LocalCaseMemoryStore,
    MemoryConsentGrant,
    MemoryPolicy,
    Scope,
)
from northstar_compliance.memory.models import isoformat_z, utc_now


@pytest.fixture
def policy_path() -> Path:
    return Path("config/memory/policy.json")


@pytest.fixture
def policy(policy_path: Path) -> MemoryPolicy:
    return MemoryPolicy.from_file(policy_path)


@pytest.fixture
def scope() -> Scope:
    return Scope(tenant_id="TENANT-NORTHSTAR", case_id="CASE-2026-0001", user_id="maya.chen")


@pytest.fixture
def case_state(scope: Scope) -> dict:
    return {
        "tenant_id": scope.tenant_id,
        "case_id": scope.case_id,
        "principal_user_id": scope.user_id,
        "revision": 7,
        "status": "waiting_for_human_review",
        "publication_id": "PUB-OSFI-2026-17",
        "jurisdictions": ["CA", "US"],
        "risk_level": "high",
        "preliminary_disposition": "unapproved",
        "human_review": {
            "status": "pending",
            "review_request_id": "REV-0001",
            "expires_at": "2026-08-05T17:00:00Z",
            "callback_token": "MUST-NOT-PERSIST"
        },
        "unresolved_questions": [
            "Does the publication alter payment-token retention?",
            "Which lending controls require owner confirmation?"
        ],
        "evidence_refs": [
            {
                "source_ref": "POL-PAY-014:lines-22-31",
                "source_version": "3.2",
                "source_sha256": "a" * 64,
                "classification": "confidential",
                "authorized": True
            },
            {
                "source_ref": "CTRL-LEND-118:record",
                "source_version": "5.0",
                "source_sha256": "b" * 64,
                "classification": "confidential",
                "authorized": True
            },
            {
                "source_ref": "CASE-OTHER-SECRET:record",
                "source_version": "1.0",
                "source_sha256": "c" * 64,
                "classification": "restricted",
                "authorized": False
            }
        ]
    }


@pytest.fixture
def grant(scope: Scope) -> MemoryConsentGrant:
    now = utc_now()
    return MemoryConsentGrant(
        grant_id="MCG-0001",
        schema_version="1.0.0",
        scope=scope,
        purpose="case_session_continuity",
        allowed_operations=("write", "read", "delete"),
        issued_at=isoformat_z(now),
        expires_at=isoformat_z(now + timedelta(days=7)),
    )


@pytest.fixture
def store(tmp_path: Path) -> LocalCaseMemoryStore:
    return LocalCaseMemoryStore(tmp_path / "memory")


@pytest.fixture
def service(policy: MemoryPolicy, store: LocalCaseMemoryStore) -> CaseWorkingMemoryService:
    return CaseWorkingMemoryService(policy, store)


@pytest.fixture
def regenerator(policy: MemoryPolicy) -> ContextRegenerator:
    return ContextRegenerator(policy)


@pytest.fixture
def compactor(policy: MemoryPolicy) -> ContextCompactor:
    return ContextCompactor(policy)


@pytest.fixture
def snapshot(scope, case_state, regenerator, compactor):
    regenerated = regenerator.regenerate(scope=scope, case_state=case_state, state_version="1.1.0")
    return compactor.compact(regenerated)
