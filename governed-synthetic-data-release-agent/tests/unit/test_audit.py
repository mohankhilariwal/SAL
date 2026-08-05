from pathlib import Path

from governed_release.adapters.observability.audit import AuditLedger
from governed_release.adapters.persistence.repository import Database, SQLAlchemyAuditStore


def test_hash_chain_and_redaction(tmp_path: Path) -> None:
    database = Database(f"sqlite:///{tmp_path / 'audit.db'}")
    database.create()
    ledger = AuditLedger(SQLAlchemyAuditStore(database), tmp_path / "audit.jsonl")
    first = ledger.append(
        workflow_id="wf1",
        trace_id="trace1",
        event_type="test",
        payload={"account_number": "123456789012"},
    )
    second = ledger.append(
        workflow_id="wf1", trace_id="trace1", event_type="test2", payload={"ok": True}
    )
    assert first.payload["account_number"] == "[REDACTED]"
    assert second.previous_hash == first.event_hash
    assert ledger.verify() == (True, [])
