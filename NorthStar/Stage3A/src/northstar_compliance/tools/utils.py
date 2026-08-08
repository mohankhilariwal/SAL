from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Mapping


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def stable_id(prefix: str, value: Any, length: int = 20) -> str:
    return f"{prefix}-{sha256_json(value).upper()[:length]}"


def redact(arguments: Mapping[str, Any], sensitive_fields: tuple[str, ...]) -> dict[str, Any]:
    protected = set(sensitive_fields)
    return {key: "***REDACTED***" if key in protected else value for key, value in arguments.items()}
