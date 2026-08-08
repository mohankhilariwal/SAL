from __future__ import annotations

import hashlib
from datetime import datetime

from northstar_compliance.durable.store import DurableStore


class ToolGateway:
    """Constrained Stage 4B gateway retaining TOOL-006 idempotency."""
    def __init__(self, store: DurableStore):
        self.store = store

    def queue_review(self, *, run_id: str, case_id: str, now: datetime) -> dict:
        key = hashlib.sha256(f"TOOL-006:{run_id}:{case_id}".encode()).hexdigest()
        review_request_id = "REV-" + key[:16].upper()
        result = {
            "tool_id": "TOOL-006",
            "status": "queued",
            "review_request_id": review_request_id,
            "case_id": case_id,
            "requires_human_review": True,
            "idempotency_key": key,
        }
        stored, created = self.store.ensure_tool_effect(key, "TOOL-006", result, now)
        stored["created"] = created
        return stored
