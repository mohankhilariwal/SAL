from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Iterable

from .models import DatasetSplit, EvaluationCase, canonical_digest


def _normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def _shingles(text: str, width: int = 4) -> set[tuple[str, ...]]:
    tokens = _normalize(text).split()
    return {tuple(tokens[i:i+width]) for i in range(max(0, len(tokens)-width+1))}


def jaccard_similarity(a: str, b: str) -> float:
    left, right = _shingles(a), _shingles(b)
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def parse_case(obj: dict) -> EvaluationCase:
    return EvaluationCase(
        case_id=obj["case_id"],
        suite_id=obj["suite_id"],
        dataset_id=obj["dataset_id"],
        dataset_version=obj["dataset_version"],
        split=DatasetSplit(obj["split"]),
        category=obj["category"],
        task_type=obj["task_type"],
        risk_tier=obj["risk_tier"],
        locale=obj["locale"],
        synthetic=bool(obj["synthetic"]),
        sealed=bool(obj["sealed"]),
        authorization_scope=obj["authorization_scope"],
        source_provenance=tuple(obj["source_provenance"]),
        input_payload=obj["input_payload"],
        expected=obj["expected"],
        assertions=tuple(obj["assertions"]),
        tags=tuple(obj.get("tags", [])),
    )


def load_jsonl(path: Path) -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            cases.append(parse_case(json.loads(line)))
        except Exception as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
    validate_cases(cases)
    return cases


def validate_cases(cases: Iterable[EvaluationCase]) -> None:
    items = list(cases)
    ids = [c.case_id for c in items]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case_id")
    versions = {(c.dataset_id, c.dataset_version) for c in items}
    if not versions:
        raise ValueError("dataset is empty")
    for case in items:
        if case.input_payload.get("raw_customer_data"):
            raise ValueError("raw customer data is prohibited")
        if case.input_payload.get("hidden_chain_of_thought"):
            raise ValueError("hidden chain-of-thought is prohibited")


def build_manifest(cases: Iterable[EvaluationCase], source_paths: Iterable[Path]) -> dict:
    items = list(cases)
    split_counts = Counter(c.split.value for c in items)
    category_counts = Counter(c.category for c in items)
    return {
        "manifest_id": "DATASET-MANIFEST-001",
        "dataset_version": "1.0.0",
        "case_count": len(items),
        "split_counts": dict(split_counts),
        "category_counts": dict(category_counts),
        "case_digests": {c.case_id: c.digest for c in sorted(items, key=lambda x: x.case_id)},
        "source_files": {
            p.name: sha256(p.read_bytes()).hexdigest()
            for p in sorted(source_paths, key=lambda p: p.name)
        },
        "synthetic_only": all(c.synthetic for c in items),
        "test_split_logically_sealed": all(
            c.sealed for c in items if c.split is DatasetSplit.TEST
        ),
        "authority_effect": "none",
    }


def contamination_report(cases: Iterable[EvaluationCase], threshold: float = 0.95) -> dict:
    items = list(cases)
    exact: list[dict] = []
    near: list[dict] = []
    for i, left in enumerate(items):
        left_text = str(left.input_payload.get("document_text", ""))
        for right in items[i+1:]:
            if left.split is right.split:
                continue
            right_text = str(right.input_payload.get("document_text", ""))
            if canonical_digest(_normalize(left_text)) == canonical_digest(_normalize(right_text)):
                exact.append({"left": left.case_id, "right": right.case_id})
            similarity = jaccard_similarity(left_text, right_text)
            if similarity >= threshold:
                near.append({
                    "left": left.case_id,
                    "right": right.case_id,
                    "similarity": round(similarity, 6),
                })
    return {
        "threshold": threshold,
        "exact_cross_split_duplicates": exact,
        "near_cross_split_duplicates": near,
        "passed": not exact and not near,
    }
