from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from northstar_compliance.agent.models import AgentRunState

class CheckpointError(RuntimeError):
    pass

class LocalCheckpointStore:
    """Atomic local checkpoint store. It is not an audit ledger or enterprise record."""

    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, run_id: str) -> Path:
        return self.directory / f"{run_id}.checkpoint.json"

    def save(self, state: AgentRunState) -> Path:
        state.checkpoint_sequence += 1
        body = state.to_dict()
        body_bytes = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        envelope: dict[str, Any] = {
            "checkpoint_schema": "1.0.0",
            "sha256": hashlib.sha256(body_bytes).hexdigest(),
            "state": body,
        }
        target = self._path(state.run_id)
        temp = target.with_suffix(".tmp")
        temp.write_text(json.dumps(envelope, indent=2, sort_keys=True), encoding="utf-8")
        with temp.open("rb") as fh:
            os.fsync(fh.fileno())
        os.replace(temp, target)
        return target

    def load(self, run_id: str) -> AgentRunState:
        target = self._path(run_id)
        if not target.exists():
            raise CheckpointError(f"checkpoint not found: {run_id}")
        envelope = json.loads(target.read_text(encoding="utf-8"))
        if envelope.get("checkpoint_schema") != "1.0.0":
            raise CheckpointError("unsupported checkpoint schema")
        body = envelope["state"]
        body_bytes = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        if hashlib.sha256(body_bytes).hexdigest() != envelope.get("sha256"):
            raise CheckpointError("checkpoint checksum mismatch")
        state = AgentRunState.from_dict(body)
        if state.schema_version != "1.1.0":
            raise CheckpointError("unsupported run state schema")
        state.resumed_from_checkpoint = True
        return state
