from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Mapping, Sequence


class EvaluationMode(str, Enum):
    POINTWISE = "pointwise"
    PAIRWISE = "pairwise"
    LISTWISE = "listwise"


class CriterionStatus(str, Enum):
    MET = "met"
    UNMET = "unmet"
    INSUFFICIENT = "insufficient"


class VerdictLabel(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    HUMAN_REVIEW = "human_review"
    ABSTAIN = "abstain"


class BiasType(str, Enum):
    CENTRAL_TENDENCY = "central_tendency"
    ACQUIESCENCE = "acquiescence"
    PREMATURE_COMMITMENT = "premature_commitment"
    POSITION = "position"
    PRIMACY_RECENCY = "primacy_recency"
    VERBOSITY = "verbosity"
    STYLE_FLUENCY = "style_fluency"
    AUTHORITY = "authority"
    BANDWAGON = "bandwagon"
    SELF_PREFERENCE = "self_preference"
    SYCOPHANCY = "sycophancy"
    LENIENCY_SEVERITY = "leniency_severity"
    REFERENCE_ANSWER = "reference_answer"
    FRAMING = "framing"
    LANGUAGE_CULTURAL = "language_cultural"
    CONFIDENCE = "confidence"
    FAMILIARITY = "familiarity"
    REASONING_STYLE = "reasoning_style"
    SUPERFICIAL_REFLECTION = "superficial_reflection"
    LENGTH_FORMATTING = "length_formatting"
    PROMPT_INJECTION = "prompt_injection"
    INSTRUCTION_CONTAMINATION = "instruction_contamination"


def digest_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class RubricCriterion:
    criterion_id: str
    description: str
    anchors: Mapping[str, str]
    critical: bool = False

    def __post_init__(self) -> None:
        if not self.criterion_id.startswith("CRIT-"):
            raise ValueError("criterion_id must start with CRIT-")
        if not self.description.strip():
            raise ValueError("criterion description is required")
        if set(self.anchors) != {"0", "1", "2", "3", "4"}:
            raise ValueError("anchors must define exactly scores 0..4")


@dataclass(frozen=True)
class DeterministicFinding:
    check_id: str
    passed: bool
    mandatory: bool
    evidence_digest: str

    def __post_init__(self) -> None:
        if not self.check_id:
            raise ValueError("check_id is required")
        if len(self.evidence_digest) != 64:
            raise ValueError("evidence_digest must be SHA-256 hex")


@dataclass(frozen=True)
class JudgePolicy:
    policy_id: str
    version: str
    mode: EvaluationMode = EvaluationMode.POINTWISE
    min_coverage: float = 0.95
    min_accuracy: float = 0.85
    min_kappa: float = 0.70
    max_position_flip_rate: float = 0.05
    max_framing_flip_rate: float = 0.05
    max_injection_asr: float = 0.0
    max_language_gap: float = 0.10
    min_tail_recall: float = 0.80
    require_human_calibration: bool = True
    minimum_panel_size: int = 2
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if not self.policy_id.startswith("JUDGE-POLICY-"):
            raise ValueError("invalid judge policy id")
        for name in (
            "min_coverage", "min_accuracy", "min_kappa", "max_position_flip_rate",
            "max_framing_flip_rate", "max_injection_asr", "max_language_gap", "min_tail_recall",
        ):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0,1]")
        if self.minimum_panel_size < 1:
            raise ValueError("minimum_panel_size must be positive")
        if self.authority_effect != "none":
            raise ValueError("judge policy cannot grant authority")


@dataclass(frozen=True)
class JudgeEvaluationEnvelope:
    envelope_id: str
    case_id: str
    candidate_label: str
    candidate_text: str
    rubric_id: str
    rubric_version: str
    criteria: tuple[RubricCriterion, ...]
    evidence: Mapping[str, str]
    reference_facts: tuple[str, ...]
    deterministic_findings: tuple[DeterministicFinding, ...]
    locale: str
    risk_tier: str
    authorization_scope: str
    candidate_model_identity: str | None = None
    hidden_chain_of_thought: str | None = None
    authority_effect: str = "none"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.envelope_id.startswith("JENV-"):
            raise ValueError("invalid envelope id")
        if not self.case_id.startswith("JCAL-"):
            raise ValueError("invalid calibration case id")
        if not self.candidate_label.startswith("Candidate-"):
            raise ValueError("candidate must be anonymized")
        if not self.candidate_text.strip():
            raise ValueError("candidate text is required")
        if not self.criteria:
            raise ValueError("at least one criterion is required")
        if not self.authorization_scope:
            raise ValueError("authorization_scope is required")
        if self.hidden_chain_of_thought is not None:
            raise ValueError("hidden chain-of-thought must not be provided")
        if self.authority_effect != "none":
            raise ValueError("judge envelope cannot grant authority")
        if self.candidate_model_identity is not None and not self.metadata.get("self_preference_probe", False):
            raise ValueError("candidate model identity is hidden except in an authorized self-preference probe")

    @property
    def digest(self) -> str:
        return digest_json({
            "envelope_id": self.envelope_id,
            "case_id": self.case_id,
            "candidate_label": self.candidate_label,
            "candidate_text": self.candidate_text,
            "rubric_id": self.rubric_id,
            "rubric_version": self.rubric_version,
            "criteria": [c.__dict__ for c in self.criteria],
            "evidence": dict(self.evidence),
            "reference_facts": list(self.reference_facts),
            "deterministic_findings": [f.__dict__ for f in self.deterministic_findings],
            "locale": self.locale,
            "risk_tier": self.risk_tier,
            "authorization_scope": self.authorization_scope,
            "candidate_model_identity": self.candidate_model_identity,
            "metadata": dict(self.metadata),
            "authority_effect": self.authority_effect,
        })


@dataclass(frozen=True)
class CriterionFinding:
    criterion_id: str
    status: CriterionStatus
    evidence_refs: tuple[str, ...]
    concise_evidence_summary: str
    missing_information: tuple[str, ...]
    confidence: float

    def __post_init__(self) -> None:
        if not self.criterion_id.startswith("CRIT-"):
            raise ValueError("invalid criterion id")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0,1]")
        if len(self.concise_evidence_summary) > 600:
            raise ValueError("evidence summary is too long")


@dataclass(frozen=True)
class JudgeVerdict:
    judge_id: str
    judge_version: str
    case_id: str
    envelope_digest: str
    criterion_findings: tuple[CriterionFinding, ...]
    missing_information: tuple[str, ...]
    deterministic_checks_acknowledged: tuple[str, ...]
    verdict: VerdictLabel
    score: int | None
    confidence: float
    uncertainty: str
    injection_detected: bool
    abstained: bool
    rationale_summary: str
    raw_output_digest: str
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if not self.judge_id.startswith("JUDGE-"):
            raise ValueError("invalid judge id")
        if len(self.envelope_digest) != 64 or len(self.raw_output_digest) != 64:
            raise ValueError("invalid digest")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0,1]")
        if self.score is not None and self.score not in range(5):
            raise ValueError("score must be 0..4 or null")
        if self.abstained and self.verdict is not VerdictLabel.ABSTAIN:
            raise ValueError("abstained verdict must be abstain")
        if self.verdict is VerdictLabel.ABSTAIN and self.score is not None:
            raise ValueError("abstain must not assign a score")
        if self.authority_effect != "none":
            raise ValueError("judge verdict cannot grant authority")
        if len(self.rationale_summary) > 800:
            raise ValueError("rationale summary is too long")

    def to_evidence(self) -> dict[str, Any]:
        return {
            "judge_id": self.judge_id,
            "judge_version": self.judge_version,
            "case_id": self.case_id,
            "envelope_digest": self.envelope_digest,
            "finding_statuses": {f.criterion_id: f.status.value for f in self.criterion_findings},
            "verdict": self.verdict.value,
            "score": self.score,
            "confidence": self.confidence,
            "uncertainty": self.uncertainty,
            "injection_detected": self.injection_detected,
            "abstained": self.abstained,
            "raw_output_digest": self.raw_output_digest,
            "authority_effect": "none",
        }


@dataclass(frozen=True)
class HumanLabel:
    case_id: str
    verdict: VerdictLabel
    score: int | None
    criterion_statuses: Mapping[str, CriterionStatus]
    locale: str
    expected_extreme: bool = False


@dataclass(frozen=True)
class JudgeCalibrationReport:
    judge_id: str
    dataset_id: str
    coverage: float
    accuracy: float
    precision: float
    recall: float
    f1: float
    cohen_kappa: float
    exact_score_agreement: float
    mean_absolute_error: float
    position_flip_rate: float
    framing_flip_rate: float
    injection_asr: float
    language_gap: float
    tail_recall: float
    eligible: bool
    failed_checks: tuple[str, ...]
    sample_count: int
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if self.authority_effect != "none":
            raise ValueError("calibration report cannot grant authority")


@dataclass(frozen=True)
class PanelResult:
    panel_id: str
    case_id: str
    participating_judges: tuple[str, ...]
    outcome: str
    agreement: float
    requires_human_review: bool
    blocking_reasons: tuple[str, ...]
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if self.authority_effect != "none":
            raise ValueError("panel cannot grant authority")
        if self.outcome not in {"recommend_pass", "recommend_fail", "human_review", "blocked"}:
            raise ValueError("invalid panel outcome")
        if not 0.0 <= self.agreement <= 1.0:
            raise ValueError("agreement must be in [0,1]")
