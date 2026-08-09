from pathlib import Path
import json
from northstar_compliance.evaluation.datasets import contamination_report, load_jsonl
from northstar_compliance.evaluation.models import DatasetSplit
from northstar_compliance.evaluation.registry import EvaluationRegistry

ROOT = Path(__file__).resolve().parents[1]
registry = EvaluationRegistry(ROOT)
suite = registry.load_suite()
assert suite.authority_effect == "none"
assert "WP-008" not in suite.target_system
all_cases = []
for split in DatasetSplit:
    cases = registry.load_cases(split)
    all_cases.extend(cases)
    assert all(c.split is split for c in cases)
assert len(all_cases) == 24
assert contamination_report(all_cases)["passed"]
assert len(list((ROOT / "schemas").glob("DATA-*.schema.json"))) == 12
for path in (ROOT / "config" / "evaluation" / "graders").glob("*.json"):
    obj = json.loads(path.read_text(encoding="utf-8"))
    assert obj["type"] == "deterministic" and obj["model_based"] is False
print("Stage 8A structural validation passed")
