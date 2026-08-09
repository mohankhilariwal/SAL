from __future__ import annotations

from collections import defaultdict
from typing import Mapping, Sequence

from .bias import BiasMeasurement
from .metrics import binary_agreement, coverage, exact_score_agreement, mean_absolute_error
from .models import HumanLabel, JudgeCalibrationReport, JudgePolicy, JudgeVerdict, VerdictLabel


def calibrate_judge(
    *,
    judge_id: str,
    dataset_id: str,
    human_labels: Mapping[str, HumanLabel],
    verdicts: Mapping[str, JudgeVerdict | None],
    bias: BiasMeasurement,
    policy: JudgePolicy,
) -> JudgeCalibrationReport:
    case_ids = sorted(human_labels)
    raw = [verdicts.get(case_id) for case_id in case_ids]
    cov = coverage(raw)
    paired = [(human_labels[c], verdicts[c]) for c in case_ids if verdicts.get(c) is not None]
    expected_pass = [h.verdict is VerdictLabel.PASS for h, _ in paired]
    observed_pass = [v.verdict is VerdictLabel.PASS for _, v in paired]
    agreement = binary_agreement(expected_pass, observed_pass)

    scored = [(h.score, v.score) for h, v in paired if h.score is not None and v.score is not None]
    exp_scores = [int(a) for a, _ in scored]
    obs_scores = [int(b) for _, b in scored]
    exact = exact_score_agreement(exp_scores, obs_scores) if scored else 0.0
    mae = mean_absolute_error(exp_scores, obs_scores) if scored else 0.0

    checks = {
        "coverage": cov >= policy.min_coverage,
        "accuracy": agreement.accuracy >= policy.min_accuracy,
        "kappa": agreement.kappa >= policy.min_kappa,
        "position_flip_rate": bias.position_flip_rate <= policy.max_position_flip_rate,
        "framing_flip_rate": bias.framing_flip_rate <= policy.max_framing_flip_rate,
        "injection_asr": bias.injection_asr <= policy.max_injection_asr,
        "language_gap": bias.language_gap <= policy.max_language_gap,
        "tail_recall": bias.tail_recall >= policy.min_tail_recall,
        "human_calibration_present": bool(human_labels) if policy.require_human_calibration else True,
    }
    failed = tuple(name for name, passed in checks.items() if not passed)
    return JudgeCalibrationReport(
        judge_id=judge_id,
        dataset_id=dataset_id,
        coverage=cov,
        accuracy=agreement.accuracy,
        precision=agreement.precision,
        recall=agreement.recall,
        f1=agreement.f1,
        cohen_kappa=agreement.kappa,
        exact_score_agreement=exact,
        mean_absolute_error=mae,
        position_flip_rate=bias.position_flip_rate,
        framing_flip_rate=bias.framing_flip_rate,
        injection_asr=bias.injection_asr,
        language_gap=bias.language_gap,
        tail_recall=bias.tail_recall,
        eligible=not failed,
        failed_checks=failed,
        sample_count=len(paired),
        authority_effect="none",
    )
