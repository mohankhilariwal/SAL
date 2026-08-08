from __future__ import annotations

from dataclasses import replace
from datetime import timedelta

import pytest

from northstar_compliance.memory import (
    ContextLifecycleEngine,
    MemoryConsentGrant,
    MemoryDeletionRequest,
    MemoryQuery,
    Scope,
)
from northstar_compliance.memory.models import isoformat_z, utc_now


def test_223_write_requires_consent(service, snapshot):
    with pytest.raises(PermissionError, match="memory_write_requires_consent"):
        service.write_snapshot(snapshot=snapshot, grant=None, write_request_id="WR-1")  # type: ignore[arg-type]


def test_224_expired_consent_denies_write(service, snapshot, grant):
    expired = replace(grant, expires_at=isoformat_z(utc_now() - timedelta(seconds=1)))
    with pytest.raises(PermissionError, match="memory_write_consent_invalid"):
        service.write_snapshot(snapshot=snapshot, grant=expired, write_request_id="WR-2")


def test_225_write_read_round_trip(service, snapshot, grant, scope):
    record = service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-3")
    result = service.read(
        query=MemoryQuery(query_id="Q-1", schema_version="1.0.0", scope=scope),
        grant=grant,
        current_source_versions={},
    )
    assert result.returned_record_ids == (record.record_id,)


def test_226_write_is_idempotent(service, snapshot, grant):
    first = service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-4")
    second = service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-4")
    assert first.record_id == second.record_id


def test_227_idempotency_conflict_is_rejected(service, snapshot, grant):
    service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-5")
    changed = replace(snapshot, content_sha256="d" * 64)
    with pytest.raises(ValueError, match="idempotency_key_reused"):
        service.write_snapshot(snapshot=changed, grant=grant, write_request_id="WR-5")


def test_228_new_write_supersedes_previous(service, snapshot, grant):
    first = service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-6")
    changed = replace(snapshot, snapshot_id="CSN-NEW", content_sha256="e" * 64)
    second = service.write_snapshot(snapshot=changed, grant=grant, write_request_id="WR-7")
    assert second.supersedes_record_id == first.record_id
    assert service.store.get_record(snapshot.scope, first.record_id).status == "superseded"


def test_229_delete_removes_content_and_leaves_tombstone(service, snapshot, grant, scope):
    record = service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-8")
    result = service.delete(
        request=MemoryDeletionRequest(
            request_id="DEL-1",
            schema_version="1.0.0",
            scope=scope,
            record_id=record.record_id,
            reason="user_revocation",
            requested_at=isoformat_z(utc_now()),
        ),
        grant=grant,
    )
    assert result.content_removed is True
    assert result.new_status == "deleted"
    with pytest.raises(FileNotFoundError):
        service.store.get_record(scope, record.record_id)


def test_230_expiry_removes_content(service, snapshot, grant, scope):
    record = service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-9", ttl_days=1)
    results = service.expire_due(scope=scope, now=utc_now() + timedelta(days=2))
    assert results[0].record_id == record.record_id
    assert results[0].new_status == "expired"


def test_231_stale_source_is_filtered(service, snapshot, grant, scope):
    record = service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-10")
    source_ref = next(binding.source_ref for binding in record.source_bindings if binding.source_ref.startswith("DATA-009:"))
    result = service.read(
        query=MemoryQuery(query_id="Q-2", schema_version="1.0.0", scope=scope),
        grant=grant,
        current_source_versions={source_ref: "9.9.9"},
    )
    assert record.record_id in result.stale_record_ids
    assert record.record_id not in result.returned_record_ids


def test_232_resume_works_without_memory(policy, store, scope, case_state, grant):
    from northstar_compliance.memory import CaseWorkingMemoryService, ContextCompactor, ContextRegenerator
    engine = ContextLifecycleEngine(ContextRegenerator(policy), ContextCompactor(policy), CaseWorkingMemoryService(policy, store))
    result = engine.start_or_resume(scope=scope, case_state=case_state, state_version="1.1.0")
    assert result.memory_record is None
    assert result.snapshot.item_count > 0
