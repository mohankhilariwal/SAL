from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from governed_release.domain.models import EvidenceArtifact, WorkflowState
from governed_release.ports.interfaces import AuditStore


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class EvidenceBuilder:
    def __init__(self, root: Path, audit_store: AuditStore) -> None:
        self.root = root
        self.audit_store = audit_store

    def build(self, state: WorkflowState) -> tuple[Path, list[EvidenceArtifact]]:
        directory = self.root / state.workflow_id
        directory.mkdir(parents=True, exist_ok=True)
        artifacts: dict[str, Any] = {
            "request.json": state.request.model_dump(mode="json"),
            "identity.json": {
                "requester": state.request.requester.model_dump(mode="json"),
                "agent": state.request.agent.model_dump(mode="json"),
            },
            "delegated_authority.json": state.authority.model_dump(mode="json")
            if state.authority
            else None,
            "dataset_profile.json": state.dataset.model_dump(mode="json")
            if state.dataset
            else None,
            "field_classification.json": [
                item.model_dump(mode="json") for item in state.classifications
            ],
            "generation_plan.json": state.generation_plan.model_dump(mode="json")
            if state.generation_plan
            else None,
            "generation_run.json": state.generation_run.model_dump(mode="json")
            if state.generation_run
            else None,
            "utility_report.json": state.utility_report.model_dump(mode="json")
            if state.utility_report
            else None,
            "privacy_report.json": state.privacy_report.model_dump(mode="json")
            if state.privacy_report
            else None,
            "recipient_assessment.json": state.recipient_assessment.model_dump(mode="json")
            if state.recipient_assessment
            else None,
            "policy_decision.json": state.policy_decision.model_dump(mode="json")
            if state.policy_decision
            else None,
            "approvals.json": [item.model_dump(mode="json") for item in state.approvals],
            "export_receipt.json": state.export_receipt.model_dump(mode="json")
            if state.export_receipt
            else None,
            "workflow_state.json": {
                "workflow_id": state.workflow_id,
                "request_id": state.request_id,
                "trace_id": state.trace_id,
                "candidate_id": state.candidate_id,
                "stage": state.stage.value,
                "decision": state.decision.value if state.decision else None,
                "policy_version": state.policy_version,
                "dataset_version": state.dataset_version,
                "evidence_bundle_id": state.evidence_bundle_id,
                "security_events": state.security_events,
                "remediation_proposal": state.remediation_proposal,
            },
            "known_limitations.json": {
                "limitations": [
                    "Entirely fictional source data and a local demonstration environment.",
                    "Privacy metrics are screening controls, not a proof of anonymity.",
                    "The local hash chain is tamper-evident demonstration evidence, not non-repudiation.",
                    "Local operating-system administrators can modify files outside the application boundary.",
                ]
            },
        }
        for name, payload in artifacts.items():
            (directory / name).write_text(
                json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8"
            )

        events = [
            event.model_dump(mode="json")
            for event in self.audit_store.events_for_workflow(state.workflow_id)
        ]
        (directory / "audit_timeline.json").write_text(
            json.dumps(events, indent=2, sort_keys=True, default=str), encoding="utf-8"
        )

        summary = self._summary(state)
        (directory / "summary.md").write_text(summary, encoding="utf-8")
        self._metrics_csv(state, directory / "metrics.csv")

        manifest_entries: dict[str, str] = {}
        for path in sorted(directory.iterdir()):
            if path.is_file() and path.name not in {"manifest.sha256.json", "evidence_bundle.zip"}:
                manifest_entries[path.name] = sha256_file(path)
        manifest = {
            "bundle_id": state.evidence_bundle_id,
            "workflow_id": state.workflow_id,
            "trace_id": state.trace_id,
            "hash_algorithm": "SHA-256",
            "files": manifest_entries,
        }
        manifest_path = directory / "manifest.sha256.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        zip_path = directory / "evidence_bundle.zip"
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(directory.iterdir()):
                if path.is_file() and path.name != zip_path.name:
                    archive.write(path, arcname=path.name)

        evidence = [
            EvidenceArtifact(artifact_type=path.stem, path=str(path), sha256=sha256_file(path))
            for path in sorted(directory.iterdir())
            if path.is_file()
        ]
        return directory, evidence

    @staticmethod
    def _summary(state: WorkflowState) -> str:
        utility = (
            state.utility_report.normalized_utility_score if state.utility_report else "not-run"
        )
        privacy = state.privacy_report.risk_category if state.privacy_report else "not-run"
        policies = (
            ", ".join(state.policy_decision.triggered_policies) if state.policy_decision else "none"
        )
        approvals = (
            ", ".join(f"{a.role.value}:{a.outcome.value}" for a in state.approvals) or "none"
        )
        receipt = state.export_receipt.released_path if state.export_receipt else "not exported"
        return f"""# Governed Synthetic Data Release Evidence

- Workflow ID: `{state.workflow_id}`
- Request ID: `{state.request_id}`
- Trace ID: `{state.trace_id}`
- Candidate ID: `{state.candidate_id}`
- Scenario: `{state.request.scenario.value}`
- Stage: `{state.stage.value}`
- Decision: `{state.decision.value if state.decision else "PENDING"}`
- Purpose: `{state.request.purpose}`
- Recipient: `{state.request.recipient}`
- Destination: `{state.request.destination}`
- Utility score: `{utility}`
- Privacy risk: `{privacy}`
- Triggered policy IDs: `{policies}`
- Approvals: `{approvals}`
- Export: `{receipt}`

This bundle is local, tamper-evident demonstration evidence. It is not production-grade non-repudiation or legal certification.
"""

    @staticmethod
    def _metrics_csv(state: WorkflowState, path: Path) -> None:
        rows: list[tuple[str, Any]] = []
        if state.utility_report:
            rows.extend(
                [
                    (
                        "utility.distribution_similarity",
                        state.utility_report.distribution_similarity,
                    ),
                    (
                        "utility.relationship_similarity",
                        state.utility_report.relationship_similarity,
                    ),
                    ("utility.fraud_roc_auc", state.utility_report.fraud_roc_auc),
                    ("utility.fraud_pr_auc", state.utility_report.fraud_pr_auc),
                    ("utility.normalized_score", state.utility_report.normalized_utility_score),
                ]
            )
        if state.privacy_report:
            rows.extend(
                [
                    ("privacy.exact_match_rate", state.privacy_report.exact_match_rate),
                    ("privacy.mean_source_similarity", state.privacy_report.mean_source_similarity),
                    ("privacy.near_duplicate_rate", state.privacy_report.near_duplicate_rate),
                    (
                        "privacy.rare_combination_exposure",
                        state.privacy_report.rare_combination_exposure,
                    ),
                ]
            )
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["metric", "value"])
            writer.writerows(rows)


def verify_evidence_directory(directory: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    manifest_path = directory / "manifest.sha256.json"
    if not manifest_path.exists():
        return False, [f"Missing manifest: {manifest_path}"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for name, expected in manifest.get("files", {}).items():
        path = directory / name
        if not path.exists():
            errors.append(f"Missing artifact: {name}")
        elif sha256_file(path) != expected:
            errors.append(f"Hash mismatch: {name}")
    return not errors, errors
