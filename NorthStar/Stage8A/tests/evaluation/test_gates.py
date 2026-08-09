from northstar_compliance.evaluation.gates import evaluate_stage8a_gates
from northstar_compliance.evaluation.harness import EvaluationHarness
from northstar_compliance.evaluation.models import DatasetSplit

def test_all_stage_gates_pass(root, suite, validation_cases, candidates):
    result = EvaluationHarness(suite).run(validation_cases, candidates, split=DatasetSplit.VALIDATION)
    gates = evaluate_stage8a_gates(root, result)
    assert len(gates) == 15 and all(g["passed"] for g in gates)

def test_evidence_export_has_no_raw_payload(suite, validation_cases, candidates):
    result = EvaluationHarness(suite).run(validation_cases, candidates, split=DatasetSplit.VALIDATION)
    evidence = result.to_evidence()
    assert "trial_records" not in evidence and "raw_payload" not in str(evidence)
