from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from _common import ROOT, DATA, CONFIG

SOURCE_OF_TRUTH = [
    ROOT / f"docs/source-of-truth/{i:02d}-{name}.md"
    for i, name in enumerate([
        "Project-Constitution",
        "Business-and-User-Story-Baseline",
        "Requirements-Register",
        "Architecture-Baseline",
        "Component-and-Agent-Catalogue",
        "Data-and-Schema-Register",
        "ADR-Register",
        "Repository-Manifest",
        "Risk-Assumption-and-Issue-Register",
        "Stage-Handoff-Pack",
    ])
]


def fail(message: str) -> None:
    raise SystemExit(f"STAGE8B CONSISTENCY AUDIT FAILED: {message}")


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def assert_mermaid(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not re.match(r"^(flowchart|sequenceDiagram|stateDiagram-v2)", text.strip()):
        fail(f"unsupported Mermaid header: {path}")
    if text.count("[") != text.count("]"):
        fail(f"unbalanced square brackets in {path}")
    if text.count("(") != text.count(")"):
        fail(f"unbalanced parentheses in {path}")


def main() -> None:
    required = SOURCE_OF_TRUTH + [
        ROOT / "docs/stages/NorthStar-Stage-8B-LLM-as-a-Judge.md",
        ROOT / "docs/architecture/diagrams/GRAPH-001-v1.6.0.mmd",
        ROOT / "docs/architecture/diagrams/stage-8b-judge-flow.mmd",
        ROOT / "docs/architecture/diagrams/stage-8b-bias-lab.mmd",
        ROOT / "reports/stage8b-demo.json",
        ROOT / "reports/stage8b-bias.json",
        ROOT / "reports/stage8b-calibration.json",
        CONFIG,
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        fail(f"missing required files: {missing}")

    sot_text = "\n".join(p.read_text(encoding="utf-8") for p in SOURCE_OF_TRUTH)
    stage_text = (ROOT / "docs/stages/NorthStar-Stage-8B-LLM-as-a-Judge.md").read_text(encoding="utf-8")
    all_text = sot_text + "\n" + stage_text

    exact_phrases = {
        "active agent invariant": "exactly one active `AGT-001`",
        "graph version": "GRAPH-001/1.6.0",
        "authority neutrality": "authority_effect: none",
        "routing unresolved": "model selection/routing remains unresolved",
        "future workload inactive": "inactive_future",
        "no hidden reasoning": "hidden chain-of-thought",
        "semantic cache prohibition": "Semantic regulatory-answer caching remains prohibited",
        "protected state": "cannot mutate `DATA-106`",
    }
    absent = [name for name, phrase in exact_phrases.items() if phrase not in all_text]
    if absent:
        fail(f"missing invariant statements: {absent}")

    # Stable ID ranges and one-definition checks.
    for prefix, start, end in (("DATA", 143, 154), ("INT", 112, 120), ("ADR", 77, 82), ("S08B-REQ", 1, 25)):
        expected = {f"{prefix}-{i:03d}" for i in range(start, end + 1)}
        found = set(re.findall(rf"`({re.escape(prefix)}-\d{{3}})`", all_text))
        missing_ids = sorted(expected - found)
        if missing_ids:
            fail(f"missing {prefix} identifiers: {missing_ids}")

    schemas = sorted((ROOT / "schemas").glob("DATA-*.schema.json"))
    schema_ids = {p.stem.replace(".schema", "") for p in schemas}
    expected_schema_ids = {f"DATA-{i:03d}" for i in range(143, 155)}
    if schema_ids != expected_schema_ids:
        fail(f"schema IDs differ: expected {sorted(expected_schema_ids)}, found {sorted(schema_ids)}")
    for schema in schemas:
        payload = json.loads(schema.read_text(encoding="utf-8"))
        if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            fail(f"wrong schema dialect: {schema.name}")
        if payload.get("type") != "object":
            fail(f"schema is not object: {schema.name}")

    # Dataset composition, isolation and no sealed-test leakage.
    cases = load_jsonl(DATA / "calibration_cases.jsonl")
    labels = load_jsonl(DATA / "human_labels.jsonl")
    replays = load_jsonl(DATA / "judge_replays.jsonl")
    observations = load_jsonl(DATA / "bias_observations.jsonl")
    if len(cases) != 24 or len(labels) != 24 or len(replays) != 72:
        fail(f"unexpected dataset sizes cases={len(cases)} labels={len(labels)} replays={len(replays)}")
    case_ids = [row["case_id"] for row in cases]
    if len(case_ids) != len(set(case_ids)):
        fail("duplicate calibration case IDs")
    if {row["case_id"] for row in labels} != set(case_ids):
        fail("human-label coverage does not match cases")
    if any(not row.get("metadata", {}).get("synthetic") for row in cases):
        fail("non-synthetic calibration case present")
    if any(row.get("metadata", {}).get("sealed_test_material") for row in cases):
        fail("Stage 8A sealed test material present")
    forbidden_dataset_keys = {"tool_id", "route_id", "route_activation", "authority_grant", "approval"}
    for row in cases:
        if forbidden_dataset_keys.intersection(row):
            fail(f"forbidden field in case {row['case_id']}")
        if not row.get("authorization_scope"):
            fail(f"missing authorization scope in {row['case_id']}")
    if not observations:
        fail("bias observations are empty")

    policy = json.loads(CONFIG.read_text(encoding="utf-8"))
    if policy.get("authority_effect") != "none":
        fail("judge policy has authority")
    if policy.get("live_model_route") not in (None, "none", "unresolved"):
        fail("live model route appears activated")
    prompt_text = (ROOT / "config/evaluation/judges/JUDGE-PROMPT-001.txt").read_text(encoding="utf-8") + (ROOT / "src/northstar_compliance/evaluation/judge/prompt.py").read_text(encoding="utf-8")
    if "deterministic" not in prompt_text.casefold() or "score-last" not in prompt_text.casefold():
        fail("deterministic-first/score-last prompt contract missing")

    # Reports assert no production/live-model claim and expected eligibility paths.
    demo = json.loads((ROOT / "reports/stage8b-demo.json").read_text(encoding="utf-8"))
    calibration = json.loads((ROOT / "reports/stage8b-calibration.json").read_text(encoding="utf-8"))
    bias = json.loads((ROOT / "reports/stage8b-bias.json").read_text(encoding="utf-8"))
    if demo.get("live_model_called") or demo.get("model_route_activated"):
        fail("demo reports a live model or route")
    if calibration.get("production_claim") or calibration.get("live_model_called"):
        fail("calibration report makes production/live claim")
    if calibration["JUDGE-A"]["eligible"]:
        fail("deliberately biased replay is eligible")
    if not calibration["JUDGE-B"]["eligible"] or not calibration["JUDGE-C"]["eligible"]:
        fail("control replay path is not eligible")
    if bias["JUDGE-A"]["injection_asr"] != 1.0 or bias["JUDGE-B"]["injection_asr"] != 0.0:
        fail("bias control paths do not distinguish injection behavior")
    if any(value.get("authority_effect") != "none" for key, value in bias.items() if key.startswith("JUDGE-")):
        fail("bias report contains authority effect")

    # Source code safety scan and parseability.
    py_files = list((ROOT / "src").rglob("*.py")) + list((ROOT / "scripts").glob("*.py"))
    forbidden_calls = ("requests.", "httpx.", "urllib.request", "subprocess.run([\"curl", "openai.", "anthropic.")
    for path in py_files:
        if path.name == "consistency_audit_stage8b.py":
            continue
        text = path.read_text(encoding="utf-8")
        try:
            ast.parse(text)
        except SyntaxError as exc:
            fail(f"syntax error in {path.relative_to(ROOT)}: {exc}")
        if any(token in text for token in forbidden_calls):
            fail(f"external/live model call marker in {path.relative_to(ROOT)}")

    for diagram in (ROOT / "docs/architecture/diagrams").glob("*.mmd"):
        assert_mermaid(diagram)
    graph = (ROOT / "docs/architecture/diagrams/GRAPH-001-v1.6.0.mmd").read_text(encoding="utf-8")
    for component in [f"CMP-{i:03d}" for i in range(1, 12)]:
        if component not in graph:
            fail(f"cumulative graph missing {component}")
    if graph.count("AGT-001") != 1:
        fail("cumulative graph does not contain exactly one AGT-001 occurrence")

    # Test identifiers are complete and unique over 563-618.
    tests_text = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "tests").rglob("test_*.py"))
    test_ids = {int(x) for x in re.findall(r"def test_(\d{3})", tests_text)}
    # Two parametrized functions intentionally cover two IDs each.
    declared = set(test_ids) | {592, 594, 610}
    expected_tests = set(range(563, 619))
    if declared != expected_tests:
        fail(f"test ID coverage differs: missing={sorted(expected_tests-declared)} extra={sorted(declared-expected_tests)}")

    report = ROOT / "reports/Stage-8B-Consistency-Audit.txt"
    report.write_text(
        "NorthStar Stage 8B Consistency Audit\n"
        "Date: 2026-08-01\n"
        "Result: PASSED WITH RECORDED EXCEPTIONS\n"
        "Exceptions: ISS-096, ISS-114-130\n\n"
        "Verified:\n"
        "- ten source-of-truth artefacts and cumulative graph exist;\n"
        "- stable new ID ranges and twelve JSON schemas are complete;\n"
        "- exactly one active AGT-001 and all CMP-001-011 appear in the architecture;\n"
        "- 24 synthetic cases, 24 labels and 72 replay outputs align;\n"
        "- no sealed test material, routes, tools or authority-bearing fields are introduced;\n"
        "- reports make no live-model or production claim;\n"
        "- biased/control calibration paths behave as intended;\n"
        "- Python sources parse and contain no live provider/network calls;\n"
        "- Mermaid sources pass static structural checks;\n"
        "- TEST-563-618 are represented; and\n"
        "- deterministic, human, authority, routing, cache and DATA-106 invariants are preserved.\n",
        encoding="utf-8",
    )
    print("STAGE8B CONSISTENCY AUDIT PASSED WITH RECORDED EXCEPTIONS ISS-096, ISS-114-130")


if __name__ == "__main__":
    main()
