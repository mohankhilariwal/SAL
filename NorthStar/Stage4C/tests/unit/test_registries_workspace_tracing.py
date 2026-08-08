import json
import pytest

from northstar_compliance.harness.registries import RegistryError, VersionedRegistry
from northstar_compliance.harness.tracing import JsonlTracer
from northstar_compliance.harness.workspace import WorkspaceError, WorkspaceManager


def test_165_registry_is_frozen_and_rejects_duplicates():
    reg = VersionedRegistry("tools")
    reg.register("TOOL-001@1.0.0", object())
    with pytest.raises(RegistryError, match="duplicate_registration"):
        reg.register("TOOL-001@1.0.0", object())
    reg.freeze()
    with pytest.raises(RegistryError, match="registry_frozen"):
        reg.register("TOOL-002@1.0.0", object())
    with pytest.raises(RegistryError, match="unregistered"):
        reg.resolve("TOOL-999@1.0.0")


def test_166_workspace_prevents_path_escape_and_sensitive_fields(tmp_path, now):
    ws = WorkspaceManager(tmp_path).create("SESSION-ABCD", now.isoformat())
    with pytest.raises(WorkspaceError, match="workspace_path_escape"):
        ws.write_json("../escape.json", {"ok": True})
    with pytest.raises(WorkspaceError, match="forbidden_sensitive_field"):
        ws.write_json("bad.json", {"approval_token": "secret"})


def test_167_trace_redacts_sensitive_attributes(tmp_path, now):
    ws = WorkspaceManager(tmp_path).create("SESSION-TRACE", now.isoformat())
    tracer = JsonlTracer(ws, session_id="SESSION-TRACE")
    tracer.emit(event_type="test", now=now, attributes={"approval_token": "abc", "chain_of_thought": "private", "safe": "ok"})
    row = json.loads((ws.root / "trace.jsonl").read_text().strip())
    assert row["attributes"]["approval_token"] == "[REDACTED]"
    assert row["attributes"]["chain_of_thought"] == "[REDACTED]"
    assert row["attributes"]["safe"] == "ok"
