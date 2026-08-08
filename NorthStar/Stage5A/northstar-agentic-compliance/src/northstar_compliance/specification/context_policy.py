from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


class ContextPolicyViolation(RuntimeError):
    pass


def enforce_context_profile(profile: Mapping[str, Any], envelope: Mapping[str, Any]) -> None:
    """Enforce DATA-077 against a previously authorized DATA-065 envelope."""
    if profile.get("memory_enabled") is not False:
        raise ContextPolicyViolation("memory_must_be_disabled")
    items = envelope.get("items")
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
        raise ContextPolicyViolation("context_items_required")
    if len(items) > int(profile["max_items"]):
        raise ContextPolicyViolation("context_item_budget_exceeded")

    total_characters = 0
    allowed = set(profile["allowed_kinds"])
    prohibited = set(profile["prohibited_kinds"])
    for item in items:
        if not isinstance(item, Mapping):
            raise ContextPolicyViolation("context_item_must_be_object")
        kind = item.get("kind")
        if kind in prohibited or kind not in allowed:
            raise ContextPolicyViolation(f"context_kind_not_allowed:{kind}")
        if item.get("authorized") is not True:
            raise ContextPolicyViolation("unauthorized_context_item")
        if not item.get("source_id") or not item.get("content_sha256"):
            raise ContextPolicyViolation("context_provenance_required")
        total_characters += len(str(item.get("content", "")))
    if total_characters > int(profile["max_characters"]):
        raise ContextPolicyViolation("context_character_budget_exceeded")
