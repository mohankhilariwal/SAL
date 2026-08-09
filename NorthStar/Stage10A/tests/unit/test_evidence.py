import json

import pytest

from northstar_compliance.audit import AuditActor, AuditIntegrityError, EvidencePackageBuilder, HashChainedAuditLedger
from northstar_compliance.observability import CorrelationContext


def prepare(tmp_path, run_id="RUN-1"):
    path = tmp_path / "audit.jsonl"
    ledger = HashChainedAuditLedger(path, key=b"test-key")
    ctx = CorrelationContext.new_root(
        session_id="SES", run_id=run_id, task_id="TASK", case_id="CASE", tenant_id="TEN"
    )
    actor = AuditActor(actor_type="human", actor_id="MAYA", role="analyst")
    for i, event in enumerate(["task.started", "human.approval.decided", "task.disposed"]):
        ledger.append(
            event_type=event,
            actor=actor,
            context=ctx,
            component_id="CMP-006" if "approval" in event else "CMP-003",
            payload={"index": i},
            idempotency_key=f"{run_id}:{i}",
        )
    return path, ledger, EvidencePackageBuilder(ledger)


def test_937_builds_package_for_run(tmp_path):
    _, _, builder = prepare(tmp_path)
    package = builder.build(run_id="RUN-1")
    assert package["manifest"]["event_count"] == 3


def test_938_package_digest_verifies(tmp_path):
    _, _, builder = prepare(tmp_path)
    package = builder.build(run_id="RUN-1")
    assert builder.verify_package(package)


def test_939_modified_package_fails_digest(tmp_path):
    _, _, builder = prepare(tmp_path)
    package = builder.build(run_id="RUN-1")
    package["manifest"]["event_count"] = 999
    assert not builder.verify_package(package)


def test_940_package_excludes_hidden_chain_of_thought(tmp_path):
    _, _, builder = prepare(tmp_path)
    package = builder.build(run_id="RUN-1")
    assert package["manifest"]["contains_hidden_chain_of_thought"] is False
    assert '"chain_of_thought":' not in json.dumps(package).lower()


def test_941_package_includes_artefact_digests(tmp_path):
    _, _, builder = prepare(tmp_path)
    package = builder.build(run_id="RUN-1", artefact_digests={"assessment": "abc"})
    assert package["manifest"]["artefact_digests"]["assessment"] == "abc"


def test_942_package_includes_release_refs(tmp_path):
    _, _, builder = prepare(tmp_path)
    package = builder.build(run_id="RUN-1", release_refs={"GR-BUNDLE-001": "1.0.0"})
    assert package["manifest"]["release_refs"]["GR-BUNDLE-001"] == "1.0.0"


def test_943_unknown_run_is_rejected(tmp_path):
    _, _, builder = prepare(tmp_path)
    with pytest.raises(ValueError):
        builder.build(run_id="RUN-404")


def test_944_invalid_chain_blocks_package(tmp_path):
    path, _, builder = prepare(tmp_path)
    lines = path.read_text().splitlines()
    record = json.loads(lines[0])
    record["payload"] = {"tampered": True}
    lines[0] = json.dumps(record)
    path.write_text("\n".join(lines) + "\n")
    reloaded = HashChainedAuditLedger(path, key=b"test-key")
    with pytest.raises(AuditIntegrityError):
        EvidencePackageBuilder(reloaded).build(run_id="RUN-1")


def test_945_package_is_non_authorizing(tmp_path):
    _, _, builder = prepare(tmp_path)
    assert builder.build(run_id="RUN-1")["authority_effect"] == "none"


def test_946_manifest_sequences_are_ordered(tmp_path):
    _, _, builder = prepare(tmp_path)
    manifest = builder.build(run_id="RUN-1")["manifest"]
    assert manifest["first_sequence"] < manifest["last_sequence"]
