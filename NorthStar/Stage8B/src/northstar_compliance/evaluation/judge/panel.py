from __future__ import annotations

from collections import Counter
from typing import Mapping, Sequence

from .models import JudgeCalibrationReport, JudgePolicy, JudgeVerdict, PanelResult, VerdictLabel


def aggregate_panel(
    *,
    panel_id: str,
    case_id: str,
    verdicts: Sequence[JudgeVerdict],
    calibration: Mapping[str, JudgeCalibrationReport],
    policy: JudgePolicy,
    mandatory_failure: bool = False,
) -> PanelResult:
    if mandatory_failure:
        return PanelResult(panel_id, case_id, tuple(v.judge_id for v in verdicts), "blocked", 1.0, True,
                           ("mandatory_deterministic_failure",), "none")
    eligible = [v for v in verdicts if calibration.get(v.judge_id) and calibration[v.judge_id].eligible]
    if len(eligible) < policy.minimum_panel_size:
        return PanelResult(panel_id, case_id, tuple(v.judge_id for v in eligible), "human_review", 0.0, True,
                           ("insufficient_eligible_judges",), "none")
    if any(v.verdict in {VerdictLabel.ABSTAIN, VerdictLabel.HUMAN_REVIEW} for v in eligible):
        return PanelResult(panel_id, case_id, tuple(v.judge_id for v in eligible), "human_review", 0.0, True,
                           ("judge_abstention_or_review",), "none")
    counts = Counter(v.verdict for v in eligible)
    top, count = counts.most_common(1)[0]
    agreement = count / len(eligible)
    if agreement < 1.0:
        return PanelResult(panel_id, case_id, tuple(v.judge_id for v in eligible), "human_review", agreement, True,
                           ("judge_disagreement",), "none")
    outcome = "recommend_pass" if top is VerdictLabel.PASS else "recommend_fail"
    return PanelResult(panel_id, case_id, tuple(v.judge_id for v in eligible), outcome, agreement, False, (), "none")
