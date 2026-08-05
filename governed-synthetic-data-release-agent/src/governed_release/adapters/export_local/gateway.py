from __future__ import annotations

import json
import os
import shutil
from datetime import timedelta
from pathlib import Path

import pandas as pd

from governed_release.application.evidence import sha256_file, verify_evidence_directory
from governed_release.domain.enums import ApprovalOutcome, ApprovalRole, Decision, WorkflowStage
from governed_release.domain.models import ExportReceipt, WorkflowState


class LocalExportGateway:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir.resolve()
        self.destinations = {
            "internal_sandbox": (self.data_dir / "released" / "internal_sandbox").resolve(),
            "named_external_partner": (
                self.data_dir / "released" / "named_external_partner"
            ).resolve(),
        }

    def release(
        self, state: WorkflowState, candidate_path: Path, evidence_dir: Path
    ) -> ExportReceipt:
        if state.decision != Decision.ALLOW:
            raise PermissionError("Only an ALLOW policy decision can be exported")
        if state.stage not in {
            WorkflowStage.EVALUATED,
            WorkflowStage.APPROVED,
            WorkflowStage.RELEASED,
        }:
            raise PermissionError(f"Workflow stage {state.stage.value} is not exportable")
        if state.request.destination not in self.destinations:
            raise PermissionError("Destination is not in the allow-list")
        if any(part in state.request.destination for part in ("/", "\\", "..", ":")):
            raise PermissionError("Destination contains a path or URL fragment")
        if state.request.destination == "named_external_partner":
            approved = {a.role for a in state.approvals if a.outcome == ApprovalOutcome.APPROVE}
            if approved != {ApprovalRole.DATA_OWNER, ApprovalRole.PRIVACY_OFFICER}:
                raise PermissionError("External release requires both independent approvals")
        ok, errors = verify_evidence_directory(evidence_dir)
        if not ok:
            raise PermissionError("Evidence verification failed: " + "; ".join(errors))
        candidate = candidate_path.resolve()
        candidate_root = (self.data_dir / "candidate").resolve()
        if candidate.parent != candidate_root or not candidate.name.startswith(state.candidate_id):
            raise PermissionError("Candidate path is outside the controlled candidate area")
        if not candidate.exists():
            raise FileNotFoundError(candidate)
        columns = set(pd.read_csv(candidate, nrows=1).columns)
        if columns & {"customer_id", "account_number", "card_token", "device_id"}:
            raise PermissionError("Candidate contains a prohibited direct identifier")

        destination = self.destinations[state.request.destination]
        destination.mkdir(parents=True, exist_ok=True)
        idempotency_key = f"{state.workflow_id}:{state.candidate_id}:{state.request.destination}:v1"
        receipt_path = destination / f"{state.candidate_id}.receipt.json"
        released_path = destination / f"{state.candidate_id}.csv"
        if receipt_path.exists() and released_path.exists():
            existing = json.loads(receipt_path.read_text(encoding="utf-8"))
            if existing.get("idempotency_key") == idempotency_key:
                return ExportReceipt.model_validate(existing)
            raise PermissionError("Export replay conflict")
        temp_path = destination / f".{state.candidate_id}.tmp"
        shutil.copyfile(candidate, temp_path)
        os.replace(temp_path, released_path)
        content_hash = sha256_file(released_path)
        receipt = ExportReceipt(
            workflow_id=state.workflow_id,
            candidate_id=state.candidate_id,
            destination=state.request.destination,
            released_path=str(released_path),
            content_hash=content_hash,
            idempotency_key=idempotency_key,
            expiry_at=state.request.created_at
            + timedelta(days=state.request.release_duration_days),
        )
        temp_receipt = receipt_path.with_suffix(".json.tmp")
        temp_receipt.write_text(receipt.model_dump_json(indent=2), encoding="utf-8")
        os.replace(temp_receipt, receipt_path)
        return receipt
