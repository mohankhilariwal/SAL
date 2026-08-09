"""Local durable checkpoint store used by the Stage 7A reference runtime."""

from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path
import tempfile
import time
from typing import Any

from .models import BranchExecutionRecord, ResumptionCheckpoint


class JsonCheckpointStore:
    """Atomic JSON checkpointing for a single coordinator instance.

    This is a local reference, not a production distributed transaction store.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = asyncio.Lock()

    async def save_record(self, record: BranchExecutionRecord, graph_version: str) -> None:
        async with self._lock:
            payload = self._read_unlocked()
            key = f"{record.case_id}:{record.run_id}"
            run = payload.setdefault(
                key,
                {
                    "case_id": record.case_id,
                    "run_id": record.run_id,
                    "graph_version": graph_version,
                    "records": {},
                },
            )
            run["records"][record.branch_id] = record.to_dict()
            run["updated_epoch_s"] = time.time()
            self._write_unlocked(payload)

    async def load_run(self, case_id: str, run_id: str) -> ResumptionCheckpoint | None:
        async with self._lock:
            payload = self._read_unlocked()
            run = payload.get(f"{case_id}:{run_id}")
            if run is None:
                return None
            records = tuple(
                run["records"][key] for key in sorted(run["records"], key=lambda k: run["records"][k]["ordinal"])
            )
            canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
            digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            return ResumptionCheckpoint(
                case_id=case_id,
                run_id=run_id,
                graph_version=run["graph_version"],
                records=records,
                checkpoint_digest=digest,
                written_epoch_s=run.get("updated_epoch_s", 0.0),
            )

    def _read_unlocked(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write_unlocked(self, payload: dict[str, Any]) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self.path.parent,
            prefix=f".{self.path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            json.dump(payload, handle, sort_keys=True, indent=2)
            handle.flush()
            temp_path = Path(handle.name)
        temp_path.replace(self.path)
