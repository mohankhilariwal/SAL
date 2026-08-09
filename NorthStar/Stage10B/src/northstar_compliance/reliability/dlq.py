from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from northstar_compliance.common.canonical import canonical_json, sha256_digest, utc_now_iso


class DeadLetterQueue:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(
        self,
        *,
        message_id: str,
        reason: str,
        payload: dict[str, Any],
        idempotency_key: str | None,
        retry_count: int,
    ) -> dict[str, Any]:
        record = {
            "schema_id": "DATA-243",
            "message_id": message_id,
            "reason": reason,
            "payload_digest": sha256_digest(payload),
            "idempotency_key": idempotency_key,
            "retry_count": retry_count,
            "status": "quarantined",
            "created_at": utc_now_iso(),
            "authority_effect": "none",
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(record) + "\n")
        return record

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line]

    def authorize_redrive(self, *, message_id: str, approved_by: str, approval_id: str) -> dict[str, Any]:
        if not approved_by or not approval_id:
            raise PermissionError("manual redrive requires authenticated approver and approval reference")
        event = {
            "schema_id": "DATA-243",
            "message_id": message_id,
            "status": "redrive_authorized",
            "approved_by": approved_by,
            "approval_id": approval_id,
            "created_at": utc_now_iso(),
            "authority_effect": "none",
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(event) + "\n")
        return event
