from __future__ import annotations

from _common import ROOT, write_report
from northstar_compliance.evaluation.judge.gates import evaluate_stage8b_gates


def main() -> None:
    gates = evaluate_stage8b_gates(ROOT)
    payload = {
        "stage": "S08B",
        "architecture_version": "1.10.0",
        "passed": sum(g.passed for g in gates),
        "total": len(gates),
        "all_passed": all(g.passed for g in gates),
        "authority_effect": "none",
        "gates": [g.to_dict() for g in gates],
    }
    path = write_report("stage8b-evaluation-gates.json", payload)
    print(path)
    if not payload["all_passed"]:
        raise SystemExit("one or more Stage 8B evaluation gates failed")


if __name__ == "__main__":
    main()
