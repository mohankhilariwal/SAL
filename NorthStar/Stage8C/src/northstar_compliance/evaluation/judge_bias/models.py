from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Label = Literal["pass", "fail", "abstain", "human_review"]
Variant = Literal["control", "treatment"]

@dataclass(frozen=True)
class ProbeFamily:
    probe_id: str
    bias_type: str
    criticality: Literal["critical", "high", "medium", "low"]
    perturbation: str
    expected_invariance: str
    hypothesis: str
    paired: bool = True
    slice_dimensions: tuple[str, ...] = ()
    authority_effect: Literal["none"] = "none"

@dataclass(frozen=True)
class TrialObservation:
    trial_id: str
    judge_id: str
    judge_config_digest: str
    probe_id: str
    pair_id: str
    variant: Variant
    repetition: int
    expected_label: Label
    observed_label: Label
    score: int | None
    seed: int
    order: int
    language: str
    candidate_family: str
    prompt_variant: str
    injection_detected: bool
    mandatory_failure: bool
    attempted_override: bool
    authority_effect: Literal["none"] = "none"
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class BiasEstimate:
    judge_id: str
    probe_id: str
    bias_type: str
    n_pairs: int
    control_positive_rate: float
    treatment_positive_rate: float
    paired_delta: float
    flip_rate: float
    directional_flip_rate: float
    score_delta: float
    score_abs_delta: float
    ci_low: float
    ci_high: float
    mcnemar_p: float
    corrected_p: float | None
    critical_failures: int
    classification: str
    authority_effect: Literal["none"] = "none"
