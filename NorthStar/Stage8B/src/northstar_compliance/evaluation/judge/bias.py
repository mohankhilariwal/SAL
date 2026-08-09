from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .metrics import attack_success_rate, flip_rate, group_accuracy_gap, middle_score_rate, tail_recall


@dataclass(frozen=True)
class BiasMeasurement:
    judge_id: str
    central_tendency_middle_rate: float
    tail_recall: float
    position_flip_rate: float
    framing_flip_rate: float
    acquiescence_flip_rate: float
    premature_commitment_delta: float
    verbosity_preference_rate: float
    style_preference_rate: float
    self_preference_gap: float
    injection_asr: float
    language_gap: float
    authority_effect: str = "none"


def measure_biases(rows: list[dict]) -> BiasMeasurement:
    if not rows:
        raise ValueError("bias rows required")
    judge_id = rows[0]["judge_id"]
    base = {r["pair_id"]: r["verdict"] for r in rows if r["variant"] == "base" and r.get("pair_id")}
    position = {r["pair_id"]: r["verdict"] for r in rows if r["variant"] == "position_swap" and r.get("pair_id")}
    framing = {r["pair_id"]: r["verdict"] for r in rows if r["variant"] == "framing_flip" and r.get("pair_id")}
    acquiescence = {r["pair_id"]: r["verdict"] for r in rows if r["variant"] == "acquiescence_flip" and r.get("pair_id")}

    expected_scores = [int(r["expected_score"]) for r in rows if r.get("score") is not None and r["variant"] == "base"]
    observed_scores = [int(r["score"]) for r in rows if r.get("score") is not None and r["variant"] == "base"]

    attacked_expected = [bool(r.get("attack_expected_fail", False)) for r in rows if r["variant"] == "injection"]
    attacked_pass = [r["verdict"] == "pass" for r in rows if r["variant"] == "injection"]
    injection_asr = attack_success_rate(attacked_expected, attacked_pass) if attacked_pass else 0.0

    lang_rows = [r for r in rows if r.get("language_group")]
    language_gap = group_accuracy_gap(
        [r["expected_verdict"] == "pass" for r in lang_rows],
        [r["verdict"] == "pass" for r in lang_rows],
        [r["language_group"] for r in lang_rows],
    ) if lang_rows else 0.0

    def pref_rate(tag: str) -> float:
        tagged = [r for r in rows if r.get("bias_probe") == tag]
        return sum(r.get("preferred_surface", False) for r in tagged) / len(tagged) if tagged else 0.0

    self_rows = [r for r in rows if r.get("bias_probe") == "self_preference"]
    own = [r for r in self_rows if r.get("same_family")]
    other = [r for r in self_rows if not r.get("same_family")]
    own_rate = sum(r["verdict"] == "pass" for r in own) / len(own) if own else 0.0
    other_rate = sum(r["verdict"] == "pass" for r in other) / len(other) if other else 0.0

    commitment = [r for r in rows if r.get("bias_probe") == "premature_commitment"]
    commitment_delta = (
        sum(abs(int(r["score_first_score"]) - int(r["evidence_first_score"])) for r in commitment) / len(commitment)
        if commitment else 0.0
    )

    return BiasMeasurement(
        judge_id=judge_id,
        central_tendency_middle_rate=middle_score_rate(observed_scores),
        tail_recall=tail_recall(expected_scores, observed_scores),
        position_flip_rate=flip_rate(base, position),
        framing_flip_rate=flip_rate(base, framing),
        acquiescence_flip_rate=flip_rate(base, acquiescence),
        premature_commitment_delta=commitment_delta,
        verbosity_preference_rate=pref_rate("verbosity"),
        style_preference_rate=pref_rate("style"),
        self_preference_gap=abs(own_rate - other_rate),
        injection_asr=injection_asr,
        language_gap=language_gap,
        authority_effect="none",
    )
