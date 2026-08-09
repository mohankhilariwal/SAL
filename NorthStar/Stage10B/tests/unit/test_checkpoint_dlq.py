import json
from pathlib import Path

import pytest

from northstar_compliance.reliability.checkpoint import CheckpointCorrupt, CheckpointStore
from northstar_compliance.reliability.dlq import DeadLetterQueue


def test_checkpoint_roundtrip(tmp_path):
    store = CheckpointStore(tmp_path)
    path = store.save(run_id="R", graph_version="G", sequence=1, state={"node": "x"})
    loaded = store.load(path)
    assert loaded["state"] == {"node": "x"} and loaded["authority_effect"] == "none"


def test_checkpoint_detects_tamper(tmp_path):
    store = CheckpointStore(tmp_path)
    path = store.save(run_id="R", graph_version="G", sequence=1, state={"node": "x"})
    data = json.loads(path.read_text()); data["state"]["node"] = "y"; path.write_text(json.dumps(data))
    with pytest.raises(CheckpointCorrupt): store.load(path)


def test_checkpoint_is_atomic_no_tmp_left(tmp_path):
    store = CheckpointStore(tmp_path)
    store.save(run_id="R", graph_version="G", sequence=1, state={})
    assert not list(tmp_path.glob("*.tmp"))


def test_dlq_minimizes_payload(tmp_path):
    q = DeadLetterQueue(tmp_path / "q.jsonl")
    record = q.append(message_id="M", reason="bad", payload={"secret": "do-not-store"}, idempotency_key=None, retry_count=2)
    text = (tmp_path / "q.jsonl").read_text()
    assert "do-not-store" not in text and record["authority_effect"] == "none"


def test_dlq_read_all(tmp_path):
    q = DeadLetterQueue(tmp_path / "q.jsonl")
    q.append(message_id="M", reason="bad", payload={}, idempotency_key="K", retry_count=2)
    assert len(q.read_all()) == 1


def test_dlq_redrive_requires_approval(tmp_path):
    q = DeadLetterQueue(tmp_path / "q.jsonl")
    with pytest.raises(PermissionError): q.authorize_redrive(message_id="M", approved_by="", approval_id="")


def test_dlq_redrive_records_approval(tmp_path):
    q = DeadLetterQueue(tmp_path / "q.jsonl")
    event = q.authorize_redrive(message_id="M", approved_by="Maya", approval_id="APR-1")
    assert event["status"] == "redrive_authorized"
