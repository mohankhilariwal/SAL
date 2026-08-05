from __future__ import annotations

import re

RULES: dict[str, re.Pattern[str]] = {
    "RAW_IDENTIFIER_ACCESS": re.compile(
        r"(copy|retain|include).*(customer ids?|account numbers?)", re.I | re.S
    ),
    "RAW_DATA_EXPORT": re.compile(
        r"(upload|send|export).*(raw|original).*(file|data)", re.I | re.S
    ),
    "EVALUATOR_BYPASS": re.compile(
        r"(skip|disable|bypass).*(privacy|evaluation|evaluator)", re.I | re.S
    ),
    "POLICY_OVERRIDE": re.compile(
        r"(already(?: been)? approved|override policy|ignore policy)", re.I
    ),
    "UNAPPROVED_DESTINATION": re.compile(
        r"external validation endpoint|arbitrary url|http[s]?://", re.I
    ),
    "RETRIEVED_CONTENT_AS_AUTHORITY": re.compile(
        r"(request|document|prompt).*(approved|authoriz)", re.I | re.S
    ),
}


def detect_injection(text: str | None) -> list[str]:
    if not text:
        return []
    return [name for name, pattern in RULES.items() if pattern.search(text)]
