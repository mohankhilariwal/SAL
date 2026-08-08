from __future__ import annotations

import hashlib
import json
import re
import secrets
from datetime import datetime, timezone
from typing import Any

_ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]{2,63}$")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_text(canonical_json(value))


def new_id(prefix: str) -> str:
    if not _ID_RE.fullmatch(prefix):
        raise ValueError(f"invalid ID prefix: {prefix}")
    return f"{prefix}-{secrets.token_hex(8).upper()}"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_utc(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
