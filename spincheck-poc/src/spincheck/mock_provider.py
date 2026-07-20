"""Deterministic mock analyzer.

Builds a schema-conformant analysis *derived from the deterministic features*,
so the whole pipeline (validation, reconciliation, escalation, explanation)
exercises genuinely in offline mode, CI, and unit tests. It is intentionally
imperfect — e.g. Tier-1 mock under-reports confidence on implied causal
sentences — so escalation paths actually fire.
"""
from __future__ import annotations

import re

from .deterministic import Features

_CAUSAL = re.compile(r"\b(caused?|causes|leads? to|because|due to|thanks to|since)\b", re.I)
_PRED = re.compile(r"\b(will|going to|by 20\d\d)\b", re.I)
_OPINION = re.compile(r"\b(disaster|great|terrible|best|worst|inspiring|amazing|awful|failure)\b", re.I)
_REPORTING = re.compile(r"\b(said|says|according to|claimed|reported)\b", re.I)


def _sent_type(sent: str, feats: Features, a: int, b: int) -> tuple[str, bool, str]:
    """-> (claim_type, explicit, certainty)"""
    in_span = lambda spans: any(x >= a and y <= b for x, y in spans)  # noqa: E731
    boosters = in_span(feats.lexicon_hits.get("boosters", []))
    hedges = in_span(feats.lexicon_hits.get("hedges", []))
    certainty = "factual_certainty" if boosters else ("hedged" if hedges else "neutral")
    if sent.rstrip().endswith("?"):
        return "rhetorical_question_claim", False, certainty
    strong_causal = bool(re.search(r"\b(caused?|causes|leads? to|because|due to)\b", sent, re.I))
    if strong_causal:
        return "causal", True, certainty
    if in_span(feats.numeric_spans):
        return "statistical", True, certainty
    if _CAUSAL.search(sent):          # weak cue only (since/after/thanks to)
        return "causal", False, certainty
    if _PRED.search(sent):
        return "predictive", True, certainty
    if _OPINION.search(sent) and not in_span(feats.numeric_spans):
        return "opinion", True, "factual_certainty" if not hedges else "hedged"
    return "direct_factual", True, certainty


def build_analysis(feats: Features, tier: int = 1) -> dict:
    text = feats.text
    claims, rhetoric = [], []
    unnamed = feats.lexicon_hits.get("unnamed_authority", [])
    for a, b in feats.sentences:
        sent = text[a:b].strip()
        if len(sent) < 4:
            continue
        s = a + (len(text[a:b]) - len(text[a:b].lstrip()))
        e = s + len(sent)
        ctype, explicit, certainty = _sent_type(sent, feats, a, b)
        attribution = "author"
        evidence = "no_evidence"
        if any(x >= a and y <= b for x, y in unnamed):
            attribution, evidence, ctype = "unnamed", "unnamed_source", "attribution"
        elif _REPORTING.search(sent):
            attribution, evidence = "named", "named_source"
        if any(x >= a and y <= b for x, y in feats.numeric_spans) and evidence == "no_evidence":
            evidence = "numerical_support"
        conf = "high" if (explicit and ctype in ("direct_factual", "statistical")) else "medium"
        if ctype in ("causal", "rhetorical_question_claim") and not explicit:
            conf = "low" if tier == 1 else "medium"     # tier-2 mock resolves it
        vq = []
        if ctype == "statistical":
            vq = ["What is the source, baseline, and time window for the figure quoted?"]
        elif ctype == "attribution":
            vq = ["Which specific experts or sources, and where was this published?"]
        elif ctype == "causal":
            vq = ["What evidence beyond sequence or association supports the causal link?"]
        claims.append({
            "span": sent, "start": s, "end": e, "claim_type": ctype,
            "explicit": explicit, "attribution": attribution,
            "certainty": certainty, "evidence_type": evidence,
            "confidence": conf,
            "normalized": sent.rstrip(".?!"),
            "context_flags": (["missing_baseline", "missing_source"]
                              if ctype == "statistical" else []),
            "verification_questions": vq,
        })
    label_map = {"boosters": "certainty_amplification", "absolutist": "absolutist_language",
                 "unnamed_authority": "unnamed_authority", "emotion": "loaded_language"}
    for lex, label in label_map.items():
        for a, b in feats.lexicon_hits.get(lex, [])[:4]:
            rhetoric.append({"label": label, "span": text[a:b], "start": a, "end": b,
                             "confidence": "medium" if tier == 1 else "high"})
    return {
        "claims": claims[:12],
        "rhetoric": rhetoric,
        "overall": {
            "satire_possible": False,
            "injection_suspected": bool(feats.injection_spans),
            "extraction_confidence": "high" if claims else "low",
        },
    }


def build_explanation(doc: dict, text: str) -> str:
    n = len(doc.get("claims", []))
    parts = [f"This text contains {n} statement{'s' if n != 1 else ''} SpinCheck could analyze."]
    for c in doc.get("claims", [])[:3]:
        if c["claim_type"] == "statistical":
            parts.append(f'It presents a statistical claim — "{c["span"]}" — without a stated baseline or source in the text itself.')
        elif c["claim_type"] == "causal" and not c["explicit"]:
            parts.append(f'The wording "{c["span"]}" may imply a causal link, though the text does not state one directly.')
        elif c["claim_type"] == "attribution":
            parts.append(f'It attributes a view to an unnamed authority: "{c["span"]}".')
        elif c["claim_type"] == "opinion":
            parts.append(f'"{c["span"]}" is an evaluative statement expressed in factual-sounding language.')
    labels = sorted({r["label"].replace("_", " ") for r in doc.get("rhetoric", [])})
    if labels:
        parts.append("Observable wording features: " + ", ".join(labels) + ".")
    qs = [q for c in doc.get("claims", []) for q in c.get("verification_questions", [])][:3]
    if qs:
        parts.append("A careful reader could check: " + " ".join(qs))
    return " ".join(parts)
