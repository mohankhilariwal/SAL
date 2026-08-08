from __future__ import annotations

from dataclasses import asdict
from datetime import timedelta
import json
from pathlib import Path
import tempfile

from northstar_compliance.memory import (
    CaseWorkingMemoryService,
    ContextCompactor,
    ContextLifecycleEngine,
    ContextRegenerator,
    LocalCaseMemoryStore,
    MemoryConsentGrant,
    MemoryPolicy,
    Scope,
)
from northstar_compliance.memory.models import isoformat_z, utc_now


def sample_state(scope: Scope) -> dict:
    return {
        "tenant_id": scope.tenant_id,
        "case_id": scope.case_id,
        "principal_user_id": scope.user_id,
        "revision": 12,
        "status": "waiting_for_human_review",
        "publication_id": "PUB-OSFI-2026-17",
        "jurisdictions": ["CA", "US"],
        "risk_level": "high",
        "preliminary_disposition": "unapproved",
        "human_review": {
            "status": "pending",
            "review_request_id": "REV-0001",
            "expires_at": "2026-08-05T17:00:00Z",
            "callback_token": "NEVER-PERSIST"
        },
        "unresolved_questions": [
            "Confirm whether payment-token retention changes.",
            "Obtain Aisha's control-owner response."
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
            }
        ]
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    policy = MemoryPolicy.from_file(root / "config/memory/policy.json")
    scope = Scope("TENANT-NORTHSTAR", "CASE-2026-0001", "maya.chen")
    now = utc_now()
    grant = MemoryConsentGrant(
        grant_id="MCG-DEMO-001",
        schema_version="1.0.0",
        scope=scope,
        purpose="case_session_continuity",
        allowed_operations=("write", "read", "delete"),
        issued_at=isoformat_z(now),
        expires_at=isoformat_z(now + timedelta(days=7)),
    )
    with tempfile.TemporaryDirectory(prefix="northstar-stage5b-") as tmp:
        service = CaseWorkingMemoryService(policy, LocalCaseMemoryStore(Path(tmp) / "memory"))
        engine = ContextLifecycleEngine(ContextRegenerator(policy), ContextCompactor(policy), service)
        first = engine.start_or_resume(
            scope=scope,
            case_state=sample_state(scope),
            state_version="1.1.0",
            grant=grant,
            write_memory=True,
            write_request_id="WR-DEMO-001",
        )
        second = engine.start_or_resume(
            scope=scope,
            case_state=sample_state(scope),
            state_version="1.1.0",
            grant=grant,
            read_memory=True,
            current_source_versions={
                f"DATA-009:{scope.case_id}": "1.1.0",
                "POL-PAY-014:lines-22-31": "3.2",
                "CTRL-LEND-118:record": "5.0",
            },
        )
        output = {
            "stage": "S05B",
            "architecture_version": "1.2.0",
            "snapshot": asdict(first.snapshot),
            "memory_record": asdict(first.memory_record) if first.memory_record else None,
            "resume": {
                "memory_record_ids": list(second.memory_read_result.returned_record_ids) if second.memory_read_result else [],
                "snapshot_id": second.snapshot.snapshot_id,
                "context_chars": second.snapshot.char_count,
                "contains_callback_token": "NEVER-PERSIST" in second.snapshot.rendered_context,
            },
            "future_memory_enabled": False,
        }
        print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
