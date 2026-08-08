from __future__ import annotations

from dataclasses import replace
from datetime import datetime
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Iterable

from .canonical import canonical_json, sha256_hex
from .models import (
    CaseWorkingMemoryRecord,
    MemoryFact,
    Scope,
    SourceBinding,
    dataclass_to_dict,
    parse_datetime,
)

_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")


class LocalCaseMemoryStore:
    """Local tutorial store with atomic files and strict scope partitioning.

    This is not an enterprise record system, event store, WORM log, or KMS-backed
    database. It is intentionally narrow and dependency-free.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def list_records(self, scope: Scope) -> list[CaseWorkingMemoryRecord]:
        case_dir = self._case_dir(scope)
        if not case_dir.exists():
            return []
        records = []
        for path in sorted(case_dir.glob("*.record.json")):
            records.append(self._load_record(path))
        return records

    def get_record(self, scope: Scope, record_id: str) -> CaseWorkingMemoryRecord:
        path = self._record_path(scope, record_id)
        if not path.exists():
            raise FileNotFoundError(record_id)
        return self._load_record(path)

    def save_record(self, record: CaseWorkingMemoryRecord) -> None:
        path = self._record_path(record.scope, record.record_id)
        self._atomic_json_write(path, dataclass_to_dict(record))

    def delete_record_content(self, scope: Scope, record_id: str, tombstone: dict) -> str:
        record_path = self._record_path(scope, record_id)
        if not record_path.exists():
            raise FileNotFoundError(record_id)
        record_path.unlink()
        tombstone_path = self._case_dir(scope) / f"{record_id}.tombstone.json"
        self._atomic_json_write(tombstone_path, tombstone)
        return str(tombstone_path.relative_to(self.root))

    def find_by_write_request(self, scope: Scope, write_request_id: str) -> CaseWorkingMemoryRecord | None:
        for record in self.list_records(scope):
            if record.write_request_id == write_request_id:
                return record
        return None

    def supersede_active(self, scope: Scope, *, except_record_id: str | None = None) -> str | None:
        superseded = None
        for record in self.list_records(scope):
            if record.status == "active" and record.record_id != except_record_id:
                updated = replace(record, status="superseded")
                updated = replace(updated, content_sha256=self.compute_record_digest(updated))
                self.save_record(updated)
                superseded = record.record_id
        return superseded

    @staticmethod
    def compute_record_digest(record: CaseWorkingMemoryRecord) -> str:
        payload = dataclass_to_dict(record)
        payload.pop("content_sha256", None)
        return sha256_hex(payload)

    @staticmethod
    def verify_record_digest(record: CaseWorkingMemoryRecord) -> None:
        expected = LocalCaseMemoryStore.compute_record_digest(record)
        if expected != record.content_sha256:
            raise ValueError("memory_record_digest_mismatch")

    def _case_dir(self, scope: Scope) -> Path:
        for value in (scope.tenant_id, scope.case_id):
            if not _SAFE_ID.fullmatch(value):
                raise ValueError("unsafe_scope_identifier")
        case_dir = (self.root / scope.tenant_id / scope.case_id).resolve()
        if self.root not in case_dir.parents:
            raise ValueError("memory_path_escape")
        return case_dir

    def _record_path(self, scope: Scope, record_id: str) -> Path:
        if not _SAFE_ID.fullmatch(record_id):
            raise ValueError("unsafe_record_identifier")
        path = (self._case_dir(scope) / f"{record_id}.record.json").resolve()
        if self.root not in path.parents:
            raise ValueError("memory_path_escape")
        return path

    @staticmethod
    def _atomic_json_write(path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=".tmp-", dir=path.parent, text=True)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, sort_keys=True, ensure_ascii=False, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @staticmethod
    def _load_record(path: Path) -> CaseWorkingMemoryRecord:
        raw = json.loads(path.read_text(encoding="utf-8"))
        scope = Scope(**raw["scope"])
        bindings = tuple(SourceBinding(**item) for item in raw["source_bindings"])
        facts = tuple(
            MemoryFact(
                fact_id=item["fact_id"],
                field_name=item["field_name"],
                value=item["value"],
                source=SourceBinding(**item["source"]),
                origin=item["origin"],
            )
            for item in raw["facts"]
        )
        record = CaseWorkingMemoryRecord(
            record_id=raw["record_id"],
            schema_version=raw["schema_version"],
            memory_kind=raw["memory_kind"],
            scope=scope,
            authorized_user_ids=tuple(raw["authorized_user_ids"]),
            purpose=raw["purpose"],
            consent_grant_id=raw["consent_grant_id"],
            source_snapshot_id=raw["source_snapshot_id"],
            source_bindings=bindings,
            facts=facts,
            unresolved_questions=tuple(raw["unresolved_questions"]),
            created_at=raw["created_at"],
            expires_at=raw["expires_at"],
            status=raw["status"],
            write_request_id=raw["write_request_id"],
            supersedes_record_id=raw.get("supersedes_record_id"),
            content_sha256=raw["content_sha256"],
        )
        LocalCaseMemoryStore.verify_record_digest(record)
        return record
