"""Reconciliation engine (pure functions, data plane).

Deterministic signals can VETO LLM labels and CAP confidence — never raise it.
Escalation/abstention *policy* comes from policy.yaml (control plane); this
module only executes it.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .deterministic import Features

BUCKETS = ["low", "medium", "high"]
_NUM = {b: i for i, b in enumerate(BUCKETS)}


def _cap(conf: str, cap: str) -> str:
    return BUCKETS[min(_NUM.get(conf, 0), _NUM.get(cap, 0))]


def _lower(conf: str, n: int = 1) -> str:
    return BUCKETS[max(0, _NUM.get(conf, 0) - n)]


@dataclass
class Decision:
    doc: dict
    escalate: bool = False
    abstain: bool = False
    reasons: list[str] = field(default_factory=list)
    disagreements: int = 0
    notes: list[str] = field(default_factory=list)


# --------------------------------------------------------------- escalation
def escalation_check(doc: dict, feats: Features, policy: dict,
                     repairs_used: int, span_errors: int) -> Decision:
    d = Decision(doc=doc)
    esc = policy["escalation"]
    tau = esc["confidence_tau"]
    tau_bucket = "medium" if tau > 0.5 else "low"

    if policy["flags"].get("force_tier2_always"):
        d.escalate = True; d.reasons.append("flag:force_tier2_always")
    low_items = [c for c in doc.get("claims", []) if _NUM[c["confidence"]] < _NUM[tau_bucket]]
    if low_items:
        d.escalate = True; d.reasons.append(f"low_confidence_items:{len(low_items)}")
    d.disagreements = _count_disagreements(doc, feats)
    if d.disagreements >= esc["max_disagreements"]:
        d.escalate = True; d.reasons.append(f"lexicon_llm_disagreements:{d.disagreements}")
    if repairs_used > esc["max_json_repairs"] or span_errors:
        d.escalate = True; d.reasons.append("validation_failures")
    if feats.injection_spans or doc.get("overall", {}).get("injection_suspected"):
        d.escalate = True; d.reasons.append("injection_suspected")
    if doc.get("overall", {}).get("satire_possible"):
        d.escalate = True; d.reasons.append("satire_flag")
    if len(feats.text) > esc["max_chars_tier1"] or len(doc.get("claims", [])) > esc["max_claims_tier1"]:
        d.escalate = True; d.reasons.append("size_over_tier1_limits")
    return d


def _count_disagreements(doc: dict, feats: Features) -> int:
    """Lexicon vs LLM certainty conflicts, per claim."""
    n = 0
    hedge_spans = feats.lexicon_hits.get("hedges", [])
    boost_spans = feats.lexicon_hits.get("boosters", [])
    for c in doc.get("claims", []):
        s, e = c.get("start", 0), c.get("end", 0)
        has_hedge = any(a >= s and b <= e for a, b in hedge_spans)
        has_boost = any(a >= s and b <= e for a, b in boost_spans)
        if has_hedge and c.get("certainty") == "factual_certainty":
            n += 1
        if has_boost and c.get("certainty") == "hedged":
            n += 1
    return n


# ------------------------------------------------------------ reconciliation
def reconcile(doc: dict, feats: Features, policy: dict, cal_map: dict[str, str]) -> Decision:
    d = Decision(doc=doc)
    conf, rhet = policy["confidence"], policy["rhetoric"]

    # 1) rhetoric vetoes: disabled labels + (span requirement already enforced upstream)
    disabled = set(policy["flags"].get("disabled_rhetoric_labels", []))
    allowed = set(rhet["assertive_labels"]) - disabled
    kept = []
    for r in doc.get("rhetoric", []):
        if r["label"] in allowed:
            kept.append(r)
        else:
            d.notes.append(f"veto:rhetoric:{r['label']}")
    doc["rhetoric"] = kept

    # 2) confidence arithmetic (deterministic; caps only)
    satire = doc.get("overall", {}).get("satire_possible", False)
    for c in doc.get("claims", []):
        if not c.get("explicit", True):
            c["confidence"] = _lower(c["confidence"], conf["implied_penalty_buckets"])
        if satire:
            c["confidence"] = _cap(c["confidence"], conf["satire_cap"])
    if d.disagreements:
        for c in doc.get("claims", []):
            c["confidence"] = _cap(c["confidence"], conf["disagreement_cap"])

    # 3) offline-fitted calibration map -> displayed buckets
    for c in doc.get("claims", []):
        c["confidence"] = cal_map.get(c["confidence"], c["confidence"])
    for r in doc.get("rhetoric", []):
        r["confidence"] = cal_map.get(r["confidence"], r["confidence"])

    # 4) abstention checks (terminal)
    ab = policy["abstention"]
    if policy["flags"].get("kill_switch_safe_mode"):
        d.abstain = True; d.reasons.append("flag:safe_mode")
    if feats.language not in ("en",):
        d.abstain = True; d.reasons.append(f"language:{feats.language}")
    ext = doc.get("overall", {}).get("extraction_confidence", "low")
    if _NUM[ext] == 0 and ab["extraction_tau"] >= 0.4:
        d.abstain = True; d.reasons.append("extraction_confidence_low")
    if feats.injection_spans:
        inj = sum(b - a for a, b in feats.injection_spans)
        if 1 - inj / max(1, len(feats.text)) < ab["min_analyzable_fraction"]:
            d.abstain = True; d.reasons.append("injection_pervasive")
    return d
