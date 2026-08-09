from __future__ import annotations
import hashlib, json
from dataclasses import asdict, is_dataclass
from typing import Any

def canonical_json(value: Any) -> str:
    if is_dataclass(value): value = asdict(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
