from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

from .graders import DEFAULT_GRADERS, Grader
from .models import DatasetSplit, EvaluationCase, EvaluationResult, TrialRecord, canonical_digest


class EvaluationHarness:
    def __init__(self, suite, graders: Iterable[Grader] = DEFAULT_GRADERS):
        self.suite = suite
        self.graders = tuple(graders)
        configured = set(suite.grader_ids)
        available = {g.grader_id for g in self.graders}
        if not configured.issubset(available):
            raise ValueError(f"missing graders: {configured - available}")

    def run(
        self,
        cases: list[EvaluationCase],
        candidates: Mapping[str, Mapping[str, Any]],
        *,
        split: DatasetSplit,
        allow_sealed: bool = False,
        run_id: str = "RUN-S08A-LOCAL-001",
    ) -> EvaluationResult:
        if not self.suite.active:
            raise ValueError("suite inactive")
        if split not in self.suite.allowed_splits:
            raise ValueError("split not permitted by suite")
        if split is DatasetSplit.TEST and not allow_sealed:
            raise PermissionError("sealed test split requires explicit allow_sealed")
        selected = [c for c in cases if c.split is split]
        if not selected:
            raise ValueError("no cases for split")
        if any(c.suite_id != self.suite.suite_id for c in selected):
            raise ValueError("suite mismatch")
        if any(c.sealed for c in selected) and not allow_sealed:
            raise PermissionError("sealed cases cannot run")

        work = []
        for case in selected:
            candidate = candidates.get(case.case_id)
            if candidate is None:
                candidate = {"case_id": case.case_id}
            for trial_number in range(1, self.suite.trial_count + 1):
                work.append((case, candidate, trial_number))

        def execute(item):
            case, candidate, trial_number = item
            findings = tuple(
                grader.grade(case, candidate)
                for grader in self.graders
                if grader.grader_id in self.suite.grader_ids
            )
            passed = all(f.passed for f in findings)
            return TrialRecord(
                run_id=run_id,
                trial_id=f"{run_id}:{case.case_id}:T{trial_number}",
                case_id=case.case_id,
                candidate_id=str(candidate.get("candidate_id", "candidate-local")),
                candidate_digest=canonical_digest(candidate),
                findings=findings,
                passed=passed,
                environment_id=f"ENV-{case.case_id}-T{trial_number}",
                raw_payload_retained=False,
            )

        with ThreadPoolExecutor(max_workers=self.suite.max_concurrency) as pool:
            records = tuple(pool.map(execute, work))

        passed_trials = sum(r.passed for r in records)
        failed_trials = len(records) - passed_trials
        categories = Counter(c.category for c in selected)
        coverage_ok = set(self.suite.required_categories).issubset(categories)
        required_gate = failed_trials == 0 and coverage_ok
        return EvaluationResult(
            run_id=run_id,
            suite_id=self.suite.suite_id,
            suite_version=self.suite.version,
            split=split,
            case_count=len(selected),
            trial_count=len(records),
            passed_trials=passed_trials,
            failed_trials=failed_trials,
            pass_rate=passed_trials / len(records),
            required_gate_passed=required_gate,
            category_counts=dict(categories),
            trial_records=records,
            authority_effect="none",
        )
