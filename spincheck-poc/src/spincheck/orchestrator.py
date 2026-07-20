"""Data-plane orchestrator: the per-request state machine.

validate -> deterministic features -> Tier-1 LLM -> validate/verify -> escalate?
-> Tier-2 -> reconcile (vetoes, confidence, abstention) -> explain -> lint ->
respond + version-stamped telemetry.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from . import mock_provider
from .config import ControlPlane
from .deterministic import Features, extract_features, normalize, validate_input
from .gateway import Gateway, LLMResult
from .reconcile import escalation_check, reconcile
from .validators import parse_json, validate

BANNED = re.compile(r"\b(misinformation|disinformation|this is (true|false)|lying|"
                    r"manipulat(ing|ive|ion)|propaganda)\b", re.I)


@dataclass
class AnalysisResponse:
    request_id: str
    status: str                      # ok | abstained | rejected
    analysis: dict | None
    explanation: str | None
    abstain_reasons: list[str] = field(default_factory=list)
    escalated: bool = False
    escalation_reasons: list[str] = field(default_factory=list)
    dropped_items: list[str] = field(default_factory=list)
    latency_s: float = 0.0
    cost_usd: float = 0.0
    version_vector: dict = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


class Orchestrator:
    def __init__(self, cp: ControlPlane, gateway: Gateway | None = None):
        self.cp = cp
        self.gw = gateway or Gateway(cp.models)

    # ------------------------------------------------------------- LLM calls
    def _analysis_prompt(self, prompt_family: str, text: str, feats: Features,
                         extra: dict | None = None) -> str:
        p = self.cp.prompt(prompt_family)
        kw = {
            "schema": json.dumps(self.cp.schema, separators=(",", ":")),
            "rhetoric_labels": ", ".join(self.cp.policy["rhetoric"]["assertive_labels"]),
            "signals": json.dumps(feats.summary(), separators=(",", ":")),
            "text": text,
        }
        kw.update(extra or {})
        return p.render(**kw)

    def _call_analysis(self, layer: str, family: str, text: str, feats: Features,
                       extra: dict | None = None) -> tuple[dict | None, LLMResult, int]:
        prompt = self._analysis_prompt(family, text, feats, extra)
        mock = mock_provider.build_analysis(feats, tier=2 if layer == "tier2" else 1)
        res = self.gw.complete(layer, prompt, mock_payload=mock)
        doc = parse_json(res.text)
        repairs = 0 if doc is not None and res.text.strip().startswith("{") else 1
        return doc, res, repairs

    # --------------------------------------------------------------- explain
    def _explain(self, doc: dict, text: str) -> tuple[str, float]:
        prompt = self.cp.prompt("explainer").render(
            analysis_json=json.dumps(doc, separators=(",", ":")), text=text)
        res = self.gw.complete("explainer", prompt,
                               mock_payload=mock_provider.build_explanation(doc, text))
        expl = res.text.strip()
        # grounding lint: quoted spans must exist in JSON; banned phrases forbidden
        quoted = re.findall(r'"([^"]{4,200})"', expl)
        spans = {c["span"] for c in doc.get("claims", [])} | {r["span"] for r in doc.get("rhetoric", [])}
        grounded = all(any(q in s or s in q for s in spans) or q in text for q in quoted)
        if BANNED.search(expl) or not grounded:
            expl = self._template_explanation(doc)   # guaranteed-safe fallback
        return expl, res.cost_usd

    @staticmethod
    def _template_explanation(doc: dict) -> str:
        n = len(doc.get("claims", []))
        labels = sorted({r["label"].replace("_", " ") for r in doc.get("rhetoric", [])})
        out = [f"SpinCheck identified {n} analyzable statement(s) in this text."]
        if labels:
            out.append("Observable wording features: " + ", ".join(labels) + ".")
        qs = [q for c in doc.get("claims", []) for q in c.get("verification_questions", [])][:3]
        if qs:
            out.append("A careful reader could check: " + " ".join(qs))
        return " ".join(out)

    # ------------------------------------------------------------------- run
    def analyze(self, raw_text: str) -> AnalysisResponse:
        t0 = time.time()
        rid = uuid.uuid4().hex[:12]
        vv = self.cp.version_vector()
        resp = AnalysisResponse(rid, "ok", None, None, version_vector=vv)

        rej = validate_input(raw_text or "", self.cp.policy)
        if rej:
            resp.status, resp.abstain_reasons = "rejected", [f"{rej.code}: {rej.message}"]
            resp.latency_s = time.time() - t0
            return resp

        text = normalize(raw_text)
        feats = extract_features(text, self.cp)
        cost = 0.0

        # --- Tier 1 ---
        doc, r1, repairs = self._call_analysis("tier1", "tier1_analysis", text, feats)
        cost += r1.cost_usd
        span_errs = 0
        if doc is not None:
            rep = validate(doc, self.cp.schema, text)
            span_errs = len(rep.span_errors)
            resp.dropped_items += rep.dropped_items
            if rep.schema_errors:
                repairs += 1
        if doc is None:
            repairs = 99  # force escalation

        dec = escalation_check(doc or {"claims": [], "rhetoric": [], "overall": {
            "satire_possible": False, "injection_suspected": bool(feats.injection_spans),
            "extraction_confidence": "low"}}, feats, self.cp.policy, repairs, span_errs)

        # --- Tier 2 (escalation) ---
        if dec.escalate:
            resp.escalated, resp.escalation_reasons = True, dec.reasons
            doc2, r2, rep2 = self._call_analysis(
                "tier2", "tier2_escalation", text, feats,
                extra={"reasons": ", ".join(dec.reasons),
                       "tier1_json": json.dumps(doc or {}, separators=(",", ":"))[:4000]})
            cost += r2.cost_usd
            if doc2 is not None:
                rep = validate(doc2, self.cp.schema, text)
                resp.dropped_items += rep.dropped_items
                if not rep.schema_errors:
                    doc = doc2
                elif doc is None:
                    doc = None
            if doc is None:
                resp.status = "abstained"
                resp.abstain_reasons = ["tier2_output_invalid"]
                resp.latency_s, resp.cost_usd = time.time() - t0, cost
                return resp

        # --- Reconcile + abstention ---
        final = reconcile(doc, feats, self.cp.policy, self.cp.calibration_map())
        resp.dropped_items += final.notes
        if final.abstain:
            resp.status, resp.abstain_reasons = "abstained", final.reasons
            resp.latency_s, resp.cost_usd = time.time() - t0, cost
            return resp

        # --- Explanation ---
        expl, c = self._explain(doc, text)
        cost += c
        resp.analysis, resp.explanation = doc, expl
        resp.latency_s, resp.cost_usd = time.time() - t0, cost
        return resp
