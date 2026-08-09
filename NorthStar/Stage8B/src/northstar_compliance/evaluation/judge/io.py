from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

from .models import (
    BiasType,
    CriterionStatus,
    DeterministicFinding,
    HumanLabel,
    JudgeEvaluationEnvelope,
    JudgePolicy,
    RubricCriterion,
    VerdictLabel,
)


def load_json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl(path: str | Path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def dump_json(path: str | Path, value) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_policy(path: str | Path) -> JudgePolicy:
    data = load_json(path)
    return JudgePolicy(**data)


def default_criteria() -> tuple[RubricCriterion, ...]:
    anchors = {
        "0": "Contradicts authoritative evidence or crosses a critical boundary.",
        "1": "Materially incorrect or unsupported.",
        "2": "Partially supported but incomplete or uncertain.",
        "3": "Substantially correct with minor non-critical gaps.",
        "4": "Fully supported, complete, bounded and explicit about uncertainty.",
    }
    return (
        RubricCriterion("CRIT-001", "Factual and evidentiary correctness", anchors, True),
        RubricCriterion("CRIT-002", "Completeness of obligation and impact coverage", anchors, False),
        RubricCriterion("CRIT-003", "Authority, permission and human-accountability compliance", anchors, True),
    )


def envelope_from_case(row: Mapping) -> JudgeEvaluationEnvelope:
    findings = tuple(
        DeterministicFinding(
            check_id=item["check_id"],
            passed=bool(item["passed"]),
            mandatory=bool(item["mandatory"]),
            evidence_digest=item["evidence_digest"],
        )
        for item in row["deterministic_findings"]
    )
    return JudgeEvaluationEnvelope(
        envelope_id=row["envelope_id"],
        case_id=row["case_id"],
        candidate_label=row["candidate_label"],
        candidate_text=row["candidate_text"],
        rubric_id=row["rubric_id"],
        rubric_version=row["rubric_version"],
        criteria=default_criteria(),
        evidence=row["evidence"],
        reference_facts=tuple(row["reference_facts"]),
        deterministic_findings=findings,
        locale=row["locale"],
        risk_tier=row["risk_tier"],
        authorization_scope=row["authorization_scope"],
        candidate_model_identity=row.get("candidate_model_identity"),
        hidden_chain_of_thought=None,
        authority_effect="none",
        metadata=row.get("metadata", {}),
    )


def human_label_from_row(row: Mapping) -> HumanLabel:
    return HumanLabel(
        case_id=row["case_id"],
        verdict=VerdictLabel(row["verdict"]),
        score=row["score"],
        criterion_statuses={k: CriterionStatus(v) for k, v in row["criterion_statuses"].items()},
        locale=row["locale"],
        expected_extreme=bool(row.get("expected_extreme", False)),
    )
