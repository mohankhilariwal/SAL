from pathlib import Path
from northstar_compliance.evaluation.models import DatasetSplit
from northstar_compliance.evaluation.registry import EvaluationRegistry
from northstar_compliance.evaluation.harness import EvaluationHarness
from northstar_compliance.evaluation.gates import evaluate_stage8a_gates
from northstar_compliance.evaluation.io import write_json

ROOT = Path(__file__).resolve().parents[1]
registry = EvaluationRegistry(ROOT)
suite = registry.load_suite()
result = EvaluationHarness(suite).run(
    registry.load_cases(DatasetSplit.VALIDATION),
    registry.load_candidates(),
    split=DatasetSplit.VALIDATION,
    run_id="RUN-S08A-GATES-001",
)
gates = evaluate_stage8a_gates(ROOT, result)
report = {"all_passed": all(g["passed"] for g in gates), "gates": gates, "result": result.to_evidence()}
write_json(ROOT / "reports" / "stage8a-evaluation.json", report)
print(f"Stage 8A gates: {sum(g['passed'] for g in gates)}/{len(gates)} passed")
raise SystemExit(0 if report["all_passed"] else 1)
