from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from northstar_compliance.common.canonical import canonical_json, sha256_digest, utc_now_iso


class CheckpointCorrupt(RuntimeError):
    pass


class CheckpointStore:
    """Local atomic checkpoints for workflow resumption only.

    Loading a checkpoint returns structured workflow state. It never writes to
    DATA-106 and therefore cannot be used as business-state replay.
    """

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, *, run_id: str, graph_version: str, sequence: int, state: dict[str, Any]) -> Path:
        payload = {
            "schema_id": "DATA-244",
            "run_id": run_id,
            "graph_version": graph_version,
            "sequence": sequence,
            "created_at": utc_now_iso(),
            "state": state,
            "authority_effect": "none",
        }
        payload["state_digest"] = sha256_digest(state)
        payload["record_digest"] = sha256_digest(payload)
        target = self.directory / f"{run_id}-{sequence:08d}.json"
        temp = target.with_suffix(".tmp")
        temp.write_text(canonical_json(payload), encoding="utf-8")
        os.replace(temp, target)
        return target

    def load(self, path: Path) -> dict[str, Any]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        supplied_record_digest = payload.pop("record_digest", None)
        expected_record_digest = sha256_digest(payload)
        payload["record_digest"] = supplied_record_digest
        if supplied_record_digest != expected_record_digest:
            raise CheckpointCorrupt("checkpoint record digest mismatch")
        if payload.get("state_digest") != sha256_digest(payload.get("state")):
            raise CheckpointCorrupt("checkpoint state digest mismatch")
        if payload.get("authority_effect") != "none":
            raise CheckpointCorrupt("checkpoint cannot have authority effect")
        return payload
