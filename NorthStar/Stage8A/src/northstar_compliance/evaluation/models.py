from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
import json
from typing import Any, Mapping


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


class DatasetSplit(StrEnum):
    DEV = "dev"
    VALIDATION = "validation"
    TEST = "test"


@dataclass(frozen=True, slots=True)
class EvaluationCase:
    case_id: str
    suite_id: str
    dataset_id: str
    dataset_version: str
    split: DatasetSplit
    category: str
    task_type: str
    risk_tier: str
    locale: str
    synthetic: bool
    sealed: bool
    authorization_scope: str
    source_provenance: tuple[str, ...]
    input_payload: Mapping[str, Any]
    expected: Mapping[str, Any]
    assertions: tuple[Mapping[str, Any], ...]
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.case_id.startswith("CASE-"):
            raise ValueError("case_id must start with CASE-")
        if not self.suite_id.startswith("EVAL-SUITE-"):
            raise ValueError("suite_id must start with EVAL-SUITE-")
        if not self.dataset_id.startswith("EDS-"):
            raise ValueError("dataset_id must start with EDS-")
        if self.risk_tier not in {"low", "medium", "high"}:
            raise ValueError("invalid risk tier")
        if not self.authorization_scope:
            raise ValueError("authorization_scope is required")
        if not self.source_provenance:
            raise ValueError("source provenance is required")
        if self.split is DatasetSplit.TEST and not self.sealed:
            raise ValueError("test cases must be logically sealed")
        if self.split is not DatasetSplit.TEST and self.sealed:
            raise ValueError("only test cases may be sealed")
        if not self.synthetic:
            raise ValueError("Stage 8A local dataset accepts synthetic cases only")

    @property
    def digest(self) -> str:
        return canonical_digest({
            "case_id": self.case_id,
            "suite_id": self.suite_id,
            "dataset_id": self.dataset_id,
            "dataset_version": self.dataset_version,
            "split": self.split.value,
            "category": self.category,
            "task_type": self.task_type,
            "risk_tier": self.risk_tier,
            "locale": self.locale,
            "synthetic": self.synthetic,
            "sealed": self.sealed,
            "authorization_scope": self.authorization_scope,
            "source_provenance": list(self.source_provenance),
            "input_payload": self.input_payload,
            "expected": self.expected,
            "assertions": list(self.assertions),
            "tags": list(self.tags),
        })


@dataclass(frozen=True, slots=True)
class EvaluationSuite:
    suite_id: str
    version: str
    description: str
    target_system: str
    active: bool
    dataset_refs: tuple[str, ...]
    grader_ids: tuple[str, ...]
    required_categories: tuple[str, ...]
    allowed_splits: tuple[DatasetSplit, ...]
    trial_count: int
    max_concurrency: int
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if not self.suite_id.startswith("EVAL-SUITE-"):
            raise ValueError("invalid suite_id")
        if self.trial_count < 1 or self.trial_count > 10:
            raise ValueError("trial_count must be between 1 and 10")
        if self.max_concurrency < 1 or self.max_concurrency > 4:
            raise ValueError("max_concurrency must be between 1 and 4")
        if self.authority_effect != "none":
            raise ValueError("evaluation suites cannot grant authority")
        if "WP-008" in self.target_system:
            raise ValueError("WP-008 remains inactive_future")


@dataclass(frozen=True, slots=True)
class GraderFinding:
    grader_id: str
    passed: bool
    score: float
    summary: str
    evidence: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be in [0,1]")
        if len(self.summary) > 500:
            raise ValueError("finding summary too long")


@dataclass(frozen=True, slots=True)
class TrialRecord:
    run_id: str
    trial_id: str
    case_id: str
    candidate_id: str
    candidate_digest: str
    findings: tuple[GraderFinding, ...]
    passed: bool
    environment_id: str
    raw_payload_retained: bool = False

    def __post_init__(self) -> None:
        if self.raw_payload_retained:
            raise ValueError("Stage 8A evidence must not retain raw payloads")


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    run_id: str
    suite_id: str
    suite_version: str
    split: DatasetSplit
    case_count: int
    trial_count: int
    passed_trials: int
    failed_trials: int
    pass_rate: float
    required_gate_passed: bool
    category_counts: Mapping[str, int]
    trial_records: tuple[TrialRecord, ...]
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if self.case_count < 0 or self.trial_count < 0:
            raise ValueError("counts must be non-negative")
        if self.passed_trials + self.failed_trials != self.trial_count:
            raise ValueError("trial counts do not reconcile")
        if not 0.0 <= self.pass_rate <= 1.0:
            raise ValueError("pass_rate must be in [0,1]")
        if self.authority_effect != "none":
            raise ValueError("evaluation results are advisory only")

    def to_evidence(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "suite_id": self.suite_id,
            "suite_version": self.suite_version,
            "split": self.split.value,
            "case_count": self.case_count,
            "trial_count": self.trial_count,
            "passed_trials": self.passed_trials,
            "failed_trials": self.failed_trials,
            "pass_rate": self.pass_rate,
            "required_gate_passed": self.required_gate_passed,
            "category_counts": dict(self.category_counts),
            "authority_effect": self.authority_effect,
            "trial_digests": [
                canonical_digest({
                    "trial_id": t.trial_id,
                    "case_id": t.case_id,
                    "candidate_digest": t.candidate_digest,
                    "passed": t.passed,
                    "findings": [
                        {
                            "grader_id": f.grader_id,
                            "passed": f.passed,
                            "score": f.score,
                            "summary": f.summary,
                        }
                        for f in t.findings
                    ],
                })
                for t in self.trial_records
            ],
        }
