from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import hmac
import json
from enum import Enum
from typing import Any

UTC = dt.timezone.utc


def _normalise(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        value = dataclasses.asdict(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dt.datetime):
        if value.tzinfo is None:
            raise ValueError("naive_datetime_not_allowed")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, dict):
        return {str(k): _normalise(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_normalise(v) for v in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_normalise(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(value: Any) -> str:
    raw = value if isinstance(value, bytes) else canonical_json(value).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def hmac_sha256(value: Any, secret: bytes) -> str:
    raw = value if isinstance(value, bytes) else canonical_json(value).encode("utf-8")
    return hmac.new(secret, raw, hashlib.sha256).hexdigest()


def constant_time_equal(left: str, right: str) -> bool:
    return hmac.compare_digest(left, right)
