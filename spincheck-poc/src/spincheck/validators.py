"""Validation layer: JSON Schema enforcement + verbatim-span verification.

Uses the `jsonschema` library when installed; ships a minimal structural
fallback (required keys / enums / types for our schema subset) so the POC and
its tests run in a bare environment. Span verification is the anti-hallucination
gate: every quoted span must appear verbatim in the input at its stated offsets
(with a small tolerance search window to auto-correct off-by-a-few offsets).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

try:  # pragma: no cover
    import jsonschema as _js
except Exception:  # noqa: BLE001
    _js = None


@dataclass
class ValidationReport:
    ok: bool
    schema_errors: list[str] = field(default_factory=list)
    span_errors: list[str] = field(default_factory=list)
    dropped_items: list[str] = field(default_factory=list)


# ------------------------------------------------------------- JSON parsing
_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.M)


def parse_json(raw: str) -> dict | None:
    """Bounded repair: strip code fences, trim to outermost braces, parse."""
    for candidate in (raw, _FENCE.sub("", raw).strip()):
        try:
            return json.loads(candidate)
        except Exception:  # noqa: BLE001
            pass
    a, b = raw.find("{"), raw.rfind("}")
    if 0 <= a < b:
        try:
            return json.loads(raw[a : b + 1])
        except Exception:  # noqa: BLE001
            return None
    return None


# ---------------------------------------------------------- schema validation
def _fallback_schema_check(doc: dict, schema: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(doc, dict):
        return ["root: not an object"]
    for key in schema.get("required", []):
        if key not in doc:
            errs.append(f"root: missing '{key}'")
    props = schema.get("properties", {})

    def check_items(name: str):
        spec = props.get(name, {}).get("items", {})
        req = spec.get("required", [])
        enums = {k: v.get("enum") for k, v in spec.get("properties", {}).items() if "enum" in v}
        for i, item in enumerate(doc.get(name, []) or []):
            for k in req:
                if k not in item:
                    errs.append(f"{name}[{i}]: missing '{k}'")
            for k, allowed in enums.items():
                if k in item and item[k] not in allowed:
                    errs.append(f"{name}[{i}].{k}: '{item[k]}' not in enum")
    check_items("claims")
    check_items("rhetoric")
    ov = doc.get("overall", {})
    for k in props.get("overall", {}).get("required", []):
        if k not in ov:
            errs.append(f"overall: missing '{k}'")
    return errs


def schema_errors(doc: dict, schema: dict) -> list[str]:
    if _js is not None:
        v = _js.Draft202012Validator(schema)
        return [f"{'/'.join(map(str, e.path))}: {e.message}" for e in v.iter_errors(doc)]
    return _fallback_schema_check(doc, schema)


# ------------------------------------------------------------ span verifier
def verify_spans(doc: dict, text: str, tolerance: int = 24) -> ValidationReport:
    """Verify every quoted span exists verbatim; fix small offset drift;
    DROP any item whose span cannot be located (anti-hallucination veto)."""
    rep = ValidationReport(ok=True)

    def locate(item: dict) -> bool:
        span = item.get("span", "")
        if not span:
            return False
        s, e = int(item.get("start", -1)), int(item.get("end", -1))
        if 0 <= s < e <= len(text) and text[s:e] == span:
            return True
        lo = max(0, s - tolerance)
        idx = text.find(span, lo, min(len(text), (e if e > 0 else len(text)) + tolerance))
        if idx < 0:
            idx = text.find(span)  # global rescue
        if idx >= 0:
            item["start"], item["end"] = idx, idx + len(span)
            return True
        return False

    for name in ("claims", "rhetoric"):
        kept = []
        for item in doc.get(name, []) or []:
            if locate(item):
                kept.append(item)
            else:
                rep.ok = False
                lbl = item.get("claim_type") or item.get("label") or "?"
                rep.span_errors.append(f"{name}: span not found verbatim ({lbl})")
                rep.dropped_items.append(f"{name}:{lbl}")
        doc[name] = kept
    return rep


def validate(doc: dict, schema: dict, text: str) -> ValidationReport:
    errs = schema_errors(doc, schema)
    rep = verify_spans(doc, text)
    rep.schema_errors = errs
    rep.ok = rep.ok and not errs
    return rep
