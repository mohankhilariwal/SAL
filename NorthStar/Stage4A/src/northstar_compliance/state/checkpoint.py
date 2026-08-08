from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from northstar_compliance.graph.models import TypedGraphExecutionState


class CheckpointError(RuntimeError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


class LocalCheckpointStore:
    """DATA-050 checksummed atomic current-state checkpoint; not event sourcing."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def path_for(self, run_id: str) -> Path:
        return self.directory / f"{run_id}.json"

    def save(self, state: TypedGraphExecutionState) -> Path:
        state.run_state.checkpoint_sequence += 1
        raw_state = state.to_dict()
        envelope = {
            "checkpoint_schema": "1.0.0",
            "graph_id": state.graph_id,
            "graph_version": state.graph_version,
            "sha256": hashlib.sha256(_canonical(raw_state)).hexdigest(),
            "state": raw_state,
        }
        target = self.path_for(state.run_state.run_id)
        tmp = target.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(envelope, f, sort_keys=True, indent=2)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, target)
        return target

    def load(self, run_id: str, *, graph_id: str, graph_version: str) -> TypedGraphExecutionState:
        envelope = json.loads(self.path_for(run_id).read_text(encoding="utf-8"))
        if envelope.get("checkpoint_schema") != "1.0.0":
            raise CheckpointError("checkpoint_schema_mismatch")
        if envelope.get("graph_id") != graph_id:
            raise CheckpointError("graph_id_mismatch")
        if envelope.get("graph_version") != graph_version:
            raise CheckpointError("graph_version_mismatch")
        raw_state = envelope["state"]
        digest = hashlib.sha256(_canonical(raw_state)).hexdigest()
        if digest != envelope.get("sha256"):
            raise CheckpointError("checkpoint_checksum_mismatch")
        state = TypedGraphExecutionState.from_dict(raw_state)
        state.run_state.resumed_from_checkpoint = True
        return state
