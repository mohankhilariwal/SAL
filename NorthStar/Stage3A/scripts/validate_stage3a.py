from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
TRUTH = ROOT / "docs" / "source-of-truth"
EXPECTED_TRUTH = [
    "00-Project-Constitution.md", "01-Business-and-User-Story-Baseline.md",
    "02-Requirements-Register.md", "03-Architecture-Baseline.md",
    "04-Component-and-Agent-Catalogue.md", "05-Data-and-Schema-Register.md",
    "06-ADR-Register.md", "07-Repository-Manifest.md",
    "08-Risk-Assumption-and-Issue-Register.md", "09-Stage-Handoff-Pack.md",
]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    for name in EXPECTED_TRUTH:
        path = TRUTH / name
        if not path.exists():
            fail(f"missing source-of-truth file: {name}")
        if "0.5.0" not in path.read_text(encoding="utf-8"):
            fail(f"version missing from {name}")

    meta = json.loads((ROOT / "config/tools/tool-descriptor.schema.json").read_text())
    Draft202012Validator.check_schema(meta)
    validator = Draft202012Validator(meta)
    descriptors = []
    for path in sorted((ROOT / "config/tools").glob("TOOL-*.json")):
        raw = json.loads(path.read_text())
        validator.validate(raw)
        Draft202012Validator.check_schema(raw["input_schema"])
        Draft202012Validator.check_schema(raw["output_schema"])
        descriptors.append(raw)
    if [d["tool_id"] for d in descriptors] != [f"TOOL-{i:03d}" for i in range(1, 7)]:
        fail("tool identifiers are not exactly TOOL-001 through TOOL-006")
    if any(d["impact_class"] not in {"read_only", "reversible_write"} for d in descriptors):
        fail("prohibited impact class registered")
    if any(d["impact_class"] == "reversible_write" and (not d["idempotency_required"] or d["retry_policy"]["max_attempts"] != 1) for d in descriptors):
        fail("write idempotency/retry invariant failed")

    texts = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for base in [ROOT / "src", ROOT / "config", TRUTH, ROOT / "docs/stages"]
        for p in base.rglob("*") if p.is_file()
    )
    if re.search(r"\bAGT-\d{3}\b", texts):
        fail("numbered agent identifier allocated in S03A")

    summary_path = ROOT / "examples/stage3a-output/demo-summary.json"
    eval_path = ROOT / "reports/stage3a-tool-evaluation.json"
    benchmark_path = ROOT / "reports/stage3a-gateway-benchmark.json"
    for path in [summary_path, eval_path, benchmark_path]:
        if not path.exists():
            fail(f"missing executed report: {path.relative_to(ROOT)}")
    summary = json.loads(summary_path.read_text())
    evaluation = json.loads(eval_path.read_text())
    if summary["case_writes"] != 1 or summary["duplicate_case_status"] != "replayed":
        fail("demo idempotency invariant failed")
    if summary["approval_granted"] or summary["external_notification_sent"] or summary["agent_identifier_allocated"]:
        fail("authority invariant failed")
    if evaluation["contract_validity_rate"] != 1.0 or evaluation["maya_restricted_hits"] != 0 or evaluation["sofia_restricted_hits"] != 1:
        fail("evaluation invariant failed")

    handoff = (TRUTH / "09-Stage-Handoff-Pack.md").read_text()
    if "Stage 3B — Bounded Single-Agent Loop" not in handoff:
        fail("handoff does not authorize exact S03B continuation")

    print("STAGE3A_VALIDATION: PASSED WITH RECORDED EXCEPTIONS")
    print("- six strict descriptors and gateway invariants validated")
    print("- demo/evaluation/benchmark reports present")
    print("- no AGT-* identifier allocated")
    print("- exceptions remain: Mermaid CLI, Python 3.12, enterprise IAM/PDP/live adapters, protocol exports")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"STAGE3A_VALIDATION: FAILED: {exc}", file=sys.stderr)
        raise
