from __future__ import annotations

import json
from pathlib import Path

from .datasets import load_jsonl
from .models import DatasetSplit, EvaluationSuite


class EvaluationRegistry:
    def __init__(self, root: Path):
        self.root = root

    def load_suite(self, suite_id: str = "EVAL-SUITE-001") -> EvaluationSuite:
        path = self.root / "config" / "evaluation" / "suites" / f"{suite_id}.json"
        obj = json.loads(path.read_text(encoding="utf-8"))
        return EvaluationSuite(
            suite_id=obj["suite_id"],
            version=obj["version"],
            description=obj["description"],
            target_system=obj["target_system"],
            active=bool(obj["active"]),
            dataset_refs=tuple(obj["dataset_refs"]),
            grader_ids=tuple(obj["grader_ids"]),
            required_categories=tuple(obj["required_categories"]),
            allowed_splits=tuple(DatasetSplit(v) for v in obj["allowed_splits"]),
            trial_count=int(obj["trial_count"]),
            max_concurrency=int(obj["max_concurrency"]),
            authority_effect=obj.get("authority_effect", "none"),
        )

    def load_cases(self, split: DatasetSplit) -> list:
        return load_jsonl(self.root / "datasets" / "evaluation" / "v1.0.0" / f"{split.value}.jsonl")

    def load_candidates(self) -> dict[str, dict]:
        path = self.root / "datasets" / "evaluation" / "v1.0.0" / "candidate_outputs.jsonl"
        output = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                output[obj["case_id"]] = obj
        return output
