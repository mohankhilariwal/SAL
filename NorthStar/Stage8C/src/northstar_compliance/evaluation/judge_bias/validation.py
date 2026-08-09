from __future__ import annotations

import re

ALLOWED_LABELS = {"pass", "fail", "abstain", "human_review"}
ALLOWED_VARIANTS = {"control", "treatment"}


def validate_probe_family(obj: dict) -> list[str]:
    errors: list[str] = []
    required = {"probe_id", "bias_type", "criticality", "perturbation", "expected_invariance", "hypothesis", "authority_effect"}
    missing = required - obj.keys()
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    if obj.get("authority_effect") != "none":
        errors.append("authority_effect must be none")
    if not re.fullmatch(r"BIAS-[A-Z0-9-]+", str(obj.get("probe_id", ""))):
        errors.append("invalid probe_id")
    if obj.get("criticality") not in {"critical", "high", "medium", "low"}:
        errors.append("invalid criticality")
    return errors


def validate_observation(obj: dict) -> list[str]:
    errors: list[str] = []
    required = {
        "trial_id", "judge_id", "judge_config_digest", "probe_id", "pair_id", "variant", "repetition",
        "expected_label", "observed_label", "seed", "order", "language", "candidate_family", "prompt_variant",
        "injection_detected", "mandatory_failure", "attempted_override", "authority_effect"
    }
    missing = required - obj.keys()
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    if obj.get("authority_effect") != "none":
        errors.append("authority_effect must be none")
    if obj.get("variant") not in ALLOWED_VARIANTS:
        errors.append("invalid variant")
    if obj.get("expected_label") not in ALLOWED_LABELS or obj.get("observed_label") not in ALLOWED_LABELS:
        errors.append("invalid label")
    if obj.get("order") not in {0, 1}:
        errors.append("order must be 0 or 1")
    score = obj.get("score")
    if score is not None and (not isinstance(score, int) or not 1 <= score <= 5):
        errors.append("score must be null or integer 1..5")
    if obj.get("mandatory_failure") and obj.get("observed_label") == "pass":
        if not obj.get("attempted_override"):
            errors.append("mandatory failure pass must be marked attempted_override")
    return errors
