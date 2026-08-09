from pathlib import Path
from northstar_compliance.evaluation.models import DatasetSplit
from northstar_compliance.evaluation.registry import EvaluationRegistry
from northstar_compliance.evaluation.harness import EvaluationHarness
from northstar_compliance.evaluation.io import write_json
from northstar_compliance.evaluation.sampling import select_human_review_sample

ROOT = Path(__file__).resolve().parents[1]
registry = EvaluationRegistry(ROOT)
suite = registry.load_suite()
cases = registry.load_cases(DatasetSplit.VALIDATION)
candidates = registry.load_candidates()
result = EvaluationHarness(suite).run(cases, candidates, split=DatasetSplit.VALIDATION)
evidence = result.to_evidence()
evidence["human_review_sample"] = select_human_review_sample(cases, result.trial_records, limit=4)
write_json(ROOT / "reports" / "stage8a-demo.json", evidence)
print(f"{result.suite_id} validation pass rate: {result.pass_rate:.3f}; gate={result.required_gate_passed}")
