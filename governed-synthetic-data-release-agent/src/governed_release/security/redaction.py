from __future__ import annotations

import re
from typing import Any

SENSITIVE_KEYS = {
    "account_number",
    "customer_id",
    "card_token",
    "device_id",
    "password",
    "secret",
    "token",
}
ACCOUNT_PATTERN = re.compile(r"\b\d{8,16}\b")
CUSTOMER_PATTERN = re.compile(r"\bCUST[-_A-Z0-9]{4,}\b", re.IGNORECASE)


def redact_value(value: Any, key: str | None = None) -> Any:
    if key and key.lower() in SENSITIVE_KEYS:
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(k): redact_value(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_value(v) for v in value]
    if isinstance(value, tuple):
        return tuple(redact_value(v) for v in value)
    if isinstance(value, str):
        value = ACCOUNT_PATTERN.sub("[REDACTED_ACCOUNT]", value)
        return CUSTOMER_PATTERN.sub("[REDACTED_CUSTOMER]", value)
    return value
