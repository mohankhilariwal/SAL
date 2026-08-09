from __future__ import annotations

from collections import Counter
from pathlib import Path

from .datasets import build_manifest, contamination_report, load_jsonl
from .models import DatasetSplit


def evaluate_stage8a_gates(root: Path, result) -> list[dict]:
    paths = [root / "datasets" / "evaluation" / "v1.0.0" / f"{s}.jsonl" for s in ("dev", "validation", "test")]
    cases = [case for path in paths for case in load_jsonl(path)]
    manifest = build_manifest(cases, paths)
    contamination = contamination_report(cases)
    categories = Counter(c.category for c in cases if c.split is DatasetSplit.VALIDATION)
    gates = [
        ("EVAL-116", manifest["case_count"] == 24, "dataset contains the declared 24 synthetic cases"),
        ("EVAL-117", manifest["synthetic_only"], "dataset contains no production data"),
        ("EVAL-118", manifest["test_split_logically_sealed"], "test split is logically sealed"),
        ("EVAL-119", contamination["passed"], "no exact or near cross-split duplicates"),
        ("EVAL-120", len(manifest["case_digests"]) == manifest["case_count"], "case identifiers and digests are unique"),
        ("EVAL-121", all(c.source_provenance for c in cases), "every case has source provenance"),
        ("EVAL-122", all(c.authorization_scope for c in cases), "every case has an authorization scope"),
        ("EVAL-123", all(c.suite_id == "EVAL-SUITE-001" for c in cases), "all cases bind to the declared suite"),
        ("EVAL-124", set(categories) >= {"normal", "negative", "permission", "tool_failure", "adversarial", "temporal", "multilingual", "conflicting_evidence"}, "validation coverage includes all required categories"),
        ("EVAL-125", result.required_gate_passed, "all required deterministic validation gates pass"),
        ("EVAL-126", result.authority_effect == "none", "evaluation result has no authority effect"),
        ("EVAL-127", all(not r.raw_payload_retained for r in result.trial_records), "evidence exports contain digests, not raw payloads"),
        ("EVAL-128", all("WP-008" not in c.task_type for c in cases), "inactive future workload is absent"),
        ("EVAL-129", result.pass_rate == 1.0, "local candidate passes every validation trial"),
        ("EVAL-130", result.split is DatasetSplit.VALIDATION, "default execution uses validation, not sealed test"),
    ]
    return [{"evaluation_id": eid, "passed": passed, "summary": summary} for eid, passed, summary in gates]
