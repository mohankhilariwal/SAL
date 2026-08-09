from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any

from northstar_compliance.common import canonical_dumps

DEFAULT_SECRET_KEYS = {
    "password",
    "secret",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "authorization",
    "private_key",
    "client_secret",
    "raw_prompt",
    "raw_response",
    "chain_of_thought",
    "reasoning_content",
}

PATTERNS = {
    "bearer": re.compile(r"(?i)bearer\s+[a-z0-9._~+\-/]+=*"),
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "credit_card_like": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


@dataclass(slots=True)
class RedactionResult:
    sanitized: Any
    redacted_paths: list[str] = field(default_factory=list)
    digests: dict[str, str] = field(default_factory=dict)
    authority_effect: str = "none"


class TelemetryRedactor:
    def __init__(self, *, secret_keys: set[str] | None = None) -> None:
        self.secret_keys = {k.lower() for k in (secret_keys or DEFAULT_SECRET_KEYS)}

    @staticmethod
    def digest(value: Any) -> str:
        return hashlib.sha256(canonical_dumps(value).encode("utf-8")).hexdigest()

    def redact(self, value: Any) -> RedactionResult:
        paths: list[str] = []
        digests: dict[str, str] = {}

        def visit(node: Any, path: str) -> Any:
            if isinstance(node, dict):
                result: dict[str, Any] = {}
                for key, child in node.items():
                    child_path = f"{path}.{key}" if path else str(key)
                    if str(key).lower() in self.secret_keys:
                        paths.append(child_path)
                        digests[child_path] = self.digest(child)
                        result[str(key)] = "[REDACTED]"
                    else:
                        result[str(key)] = visit(child, child_path)
                return result
            if isinstance(node, list):
                return [visit(child, f"{path}[{index}]") for index, child in enumerate(node)]
            if isinstance(node, str):
                sanitized = node
                for name, pattern in PATTERNS.items():
                    if pattern.search(sanitized):
                        paths.append(path or "$value")
                        digests[path or "$value"] = self.digest(node)
                        sanitized = pattern.sub(f"[REDACTED:{name}]", sanitized)
                return sanitized
            return node

        return RedactionResult(visit(value, ""), sorted(set(paths)), digests)
