from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import EvaluationCase, TrialRecord


def select_human_review_sample(cases: Iterable[EvaluationCase], records: Iterable[TrialRecord], limit: int = 5) -> list[str]:
    case_map = {c.case_id: c for c in cases}
    failed = {r.case_id for r in records if not r.passed}
    ranked = sorted(
        case_map.values(),
        key=lambda c: (
            0 if c.case_id in failed else 1,
            {"high": 0, "medium": 1, "low": 2}[c.risk_tier],
            c.category,
            c.case_id,
        ),
    )
    return [c.case_id for c in ranked[:limit]]
