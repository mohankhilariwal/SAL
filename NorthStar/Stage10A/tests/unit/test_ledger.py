import json
from pathlib import Path

import pytest

from northstar_compliance.audit import AuditActor, AuditUnavailable, HashChainedAuditLedger
from northstar_compliance.observability import CorrelationContext


def context(run_id="RUN-1"):
    return CorrelationContext.new_root(
        session_id="SES", run_id=run_id, task_id="TASK", case_id="CASE", tenant_id="TEN"
    )


def actor():
    return AuditActor(actor_type="workload", actor_id="northstar-runtime", workload_id="WL-001")


def ledger(tmp_path: Path):
    return HashChainedAuditLedger(tmp_path / "audit.jsonl", key=b"test-key")


def append_one(instance, *, key="IDEM-1", event="task.started", payload=None):
    return instance.append(
        event_type=event,
        actor=actor(),
        context=context(),
        component_id="CMP-003",
        payload=payload or {"status": "started"},
        idempotency_key=key,
    )


def test_919_append_creates_first_chain_record(tmp_path):
    event = append_one(ledger(tmp_path))
    assert event["sequence"] == 1
    assert event["previous_hash"] == "0" * 64


def test_920_second_record_links_to_first(tmp_path):
    instance = ledger(tmp_path)
    first = append_one(instance)
    second = append_one(instance, key="IDEM-2", event="task.disposed")
    assert second["previous_hash"] == first["record_hash"]


def test_921_valid_chain_verifies(tmp_path):
    instance = ledger(tmp_path)
    append_one(instance)
    report = instance.verify()
    assert report.valid and report.event_count == 1


def test_922_idempotent_append_returns_same_event(tmp_path):
    instance = ledger(tmp_path)
    first = append_one(instance)
    second = append_one(instance)
    assert first["audit_event_id"] == second["audit_event_id"]
    assert instance.event_count == 1


def test_923_secret_payload_is_redacted(tmp_path):
    event = append_one(ledger(tmp_path), payload={"access_token": "abc"})
    assert event["payload"]["access_token"] == "[REDACTED]"


def test_924_missing_idempotency_key_is_rejected(tmp_path):
    instance = ledger(tmp_path)
    with pytest.raises(ValueError):
        instance.append(
            event_type="task.started", actor=actor(), context=context(), component_id="CMP-003", payload={}, idempotency_key=""
        )


def test_925_write_failure_raises_audit_unavailable(tmp_path):
    instance = HashChainedAuditLedger(tmp_path / "audit.jsonl", key=b"test", fail_writes=True)
    with pytest.raises(AuditUnavailable):
        append_one(instance)


def test_926_checkpoint_is_signed(tmp_path):
    instance = ledger(tmp_path)
    append_one(instance)
    checkpoint = instance.create_checkpoint()
    assert checkpoint["event_count"] == 1
    assert checkpoint["signature"]


@pytest.mark.parametrize("field,new_value", [
    ("payload", {"status": "tampered"}),
    ("previous_hash", "f" * 64),
    ("record_hash", "e" * 64),
    ("signature", "bad"),
])
def test_927_to_930_tampering_is_detected(tmp_path, field, new_value):
    path = tmp_path / "audit.jsonl"
    instance = HashChainedAuditLedger(path, key=b"test-key")
    append_one(instance)
    record = json.loads(path.read_text().strip())
    record[field] = new_value
    path.write_text(json.dumps(record) + "\n")
    reloaded = HashChainedAuditLedger(path, key=b"test-key")
    assert not reloaded.verify().valid


def test_931_wrong_key_detects_signature_failure(tmp_path):
    path = tmp_path / "audit.jsonl"
    instance = HashChainedAuditLedger(path, key=b"key-one")
    append_one(instance)
    reloaded = HashChainedAuditLedger(path, key=b"key-two")
    assert not reloaded.verify().valid


def test_932_reload_preserves_chain_state(tmp_path):
    path = tmp_path / "audit.jsonl"
    instance = HashChainedAuditLedger(path, key=b"test-key")
    first = append_one(instance)
    reloaded = HashChainedAuditLedger(path, key=b"test-key")
    second = append_one(reloaded, key="IDEM-2", event="task.disposed")
    assert second["previous_hash"] == first["record_hash"]


def test_933_actor_is_recorded_without_credentials(tmp_path):
    event = append_one(ledger(tmp_path))
    assert event["actor"]["actor_id"] == "northstar-runtime"
    assert "token" not in event["actor"]


def test_934_audit_event_has_no_authority_effect(tmp_path):
    assert append_one(ledger(tmp_path))["authority_effect"] == "none"


def test_935_sequence_is_monotonic(tmp_path):
    instance = ledger(tmp_path)
    for i in range(5):
        append_one(instance, key=f"IDEM-{i}", event=f"event.{i}")
    assert [r["sequence"] for r in instance.records()] == [1, 2, 3, 4, 5]


def test_936_duplicate_idempotency_is_not_reappended_after_reload(tmp_path):
    path = tmp_path / "audit.jsonl"
    instance = HashChainedAuditLedger(path, key=b"test-key")
    first = append_one(instance)
    reloaded = HashChainedAuditLedger(path, key=b"test-key")
    second = append_one(reloaded)
    assert second["audit_event_id"] == first["audit_event_id"]
    assert reloaded.event_count == 1
