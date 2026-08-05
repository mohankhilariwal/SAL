from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from governed_release.application.workflow import build_service
from governed_release.config.settings import Settings
from governed_release.domain.enums import ApprovalRole, Scenario


def summary(state: object, *, checkpoint: dict[str, object] | None = None) -> dict[str, object]:
    receipt = state.export_receipt.model_dump(mode="json") if state.export_receipt else None
    if receipt and receipt.get("released_path"):
        try:
            receipt["released_path"] = str(Path(receipt["released_path"]).relative_to(ROOT))
        except ValueError:
            receipt["released_path"] = str(receipt["released_path"])
    result = {
        "workflow_id": state.workflow_id,
        "scenario": state.request.scenario.value,
        "stage": state.stage.value,
        "decision": state.decision.value if state.decision else None,
        "utility_score": state.utility_report.normalized_utility_score
        if state.utility_report
        else None,
        "privacy_passed": state.privacy_report.passed if state.privacy_report else None,
        "privacy_risk": state.privacy_report.risk_category if state.privacy_report else None,
        "approvals": [a.role.value for a in state.approvals],
        "export_receipt": receipt,
        "evidence_dir": f"data/evidence/{state.workflow_id}",
        "sample_evidence_dir": f"artifacts/sample-evidence/{state.request.scenario.value}",
    }
    if checkpoint is not None:
        result["approval_checkpoint"] = checkpoint
    return result


def main() -> None:
    settings = Settings(
        data_dir=ROOT / "data", database_url=f"sqlite:///{ROOT / 'data' / 'governed_release.db'}"
    )
    service = build_service(settings)
    results: list[dict[str, object]] = []
    for scenario in Scenario:
        print(f"Running {scenario.value} ...", flush=True)
        state = service.run_scenario(scenario)
        checkpoint = None
        if scenario == Scenario.EXTERNAL_APPROVAL:
            checkpoint = {
                "stage": state.stage.value,
                "decision": state.decision.value if state.decision else None,
                "required_approvals": [
                    role.value for role in state.policy_decision.required_approvals
                ],
                "export_blocked": state.export_receipt is None,
            }
            service.approve(
                state.workflow_id,
                ApprovalRole.DATA_OWNER,
                "data_owner_001",
                "Data owner reviewed purpose, recipient and utility.",
            )
            service.approve(
                state.workflow_id,
                ApprovalRole.PRIVACY_OFFICER,
                "privacy_officer_001",
                "Privacy officer reviewed residual and auxiliary-data risk.",
            )
            state = service.resume(state.workflow_id)
        results.append(summary(state, checkpoint=checkpoint))
        evidence_dir = ROOT / "data" / "evidence" / state.workflow_id
        sample_dir = ROOT / "artifacts" / "sample-evidence" / scenario.value
        if sample_dir.exists():
            shutil.rmtree(sample_dir)
        shutil.copytree(evidence_dir, sample_dir)
        print(json.dumps(results[-1], indent=2, default=str))
    output = ROOT / "artifacts" / "scenario-results.json"
    output.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"Scenario report: {output}")


if __name__ == "__main__":
    main()
