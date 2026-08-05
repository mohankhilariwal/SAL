from __future__ import annotations

import shutil
import time
from pathlib import Path
from typing import Any

from governed_release.adapters.export_local.gateway import LocalExportGateway
from governed_release.adapters.local_files.source_data import (
    generate_maplebridge_source,
    load_source,
)
from governed_release.adapters.observability.audit import AuditLedger
from governed_release.adapters.ollama.gateway import OllamaModelGateway, StubModelGateway
from governed_release.adapters.persistence.repository import (
    Database,
    SQLAlchemyAuditStore,
    SQLAlchemyWorkflowStore,
)
from governed_release.adapters.policy_opa.adapter import OPAPolicyAdapter
from governed_release.adapters.policy_python.engine import PythonPolicyEngine
from governed_release.adapters.sdv.generator import build_generator
from governed_release.adapters.sklearn.evaluators import evaluate_privacy, evaluate_utility
from governed_release.application.classification import classify_fields
from governed_release.application.evidence import EvidenceBuilder, sha256_file
from governed_release.application.scenarios import request_for_scenario
from governed_release.config.settings import Settings
from governed_release.domain.enums import (
    ApprovalOutcome,
    ApprovalRole,
    Decision,
    ReleaseDisposition,
    Scenario,
    WorkflowStage,
)
from governed_release.domain.models import (
    ApprovalDecision,
    DatasetAsset,
    DelegatedAuthority,
    GenerationPlan,
    GenerationRun,
    PolicyInput,
    RecipientAssessment,
    WorkflowState,
    utcnow,
)
from governed_release.security.injection import detect_injection


class WorkflowService:
    def __init__(
        self,
        settings: Settings,
        store: SQLAlchemyWorkflowStore,
        audit: AuditLedger,
        evidence: EvidenceBuilder,
        export_gateway: LocalExportGateway,
        policy: PythonPolicyEngine | OPAPolicyAdapter,
        model: StubModelGateway | OllamaModelGateway,
    ) -> None:
        self.settings = settings
        self.store = store
        self.audit = audit
        self.evidence = evidence
        self.export_gateway = export_gateway
        self.policy = policy
        self.model = model

    def run_scenario(self, scenario: Scenario | str) -> WorkflowState:
        scenario = Scenario(scenario)
        request = request_for_scenario(scenario)
        state = WorkflowState(request_id=request.id, request=request)
        self._checkpoint(
            state,
            "request.received",
            {"scenario": scenario.value, "request": request.model_dump(mode="json")},
        )
        return self._execute(state)

    def _execute(self, state: WorkflowState) -> WorkflowState:
        request = state.request
        interpretation = self.model.interpret(
            request.malicious_content or request.intended_use, trace_id=state.trace_id
        )
        self.audit.append(
            workflow_id=state.workflow_id,
            trace_id=state.trace_id,
            event_type="model.interpretation",
            payload=interpretation,
        )

        state.stage = WorkflowStage.IDENTITY_VALIDATED
        self._checkpoint(
            state,
            "identity.validated",
            {
                "requester_id": request.requester.id,
                "role": request.requester.role,
                "active": request.requester.active,
            },
        )

        authority_valid = request.requested_rows <= self.settings.max_rows and request.purpose in {
            "fraud_research",
            "fraud_model_development",
        }
        state.authority = DelegatedAuthority(
            requester_id=request.requester.id,
            dataset_id=request.dataset_name,
            purpose=request.purpose,
            recipient=request.recipient,
            max_rows=self.settings.max_rows,
            expiry_days=request.release_duration_days,
            valid=authority_valid,
        )
        state.stage = WorkflowStage.AUTHORITY_VALIDATED
        self._checkpoint(state, "authority.validated", state.authority.model_dump(mode="json"))

        violations = detect_injection(request.malicious_content)
        if violations:
            state.security_events.extend(violations)
            self.audit.append(
                workflow_id=state.workflow_id,
                trace_id=state.trace_id,
                event_type="security.prompt_injection_detected",
                payload={
                    "violations": violations,
                    "blocked_tool_calls": [
                        "read_raw_identifiers",
                        "skip_privacy_evaluator",
                        "upload_external_url",
                    ],
                },
            )
            policy_input = self._policy_input(
                state,
                authority_valid=authority_valid,
                privacy_pass=True,
                utility_pass=True,
                evidence_complete=True,
                direct_identifiers=False,
                data_scope_valid=False,
                destination_allowed=False,
                violations=violations,
            )
            state.policy_decision = self.policy.evaluate(policy_input)
            state.decision = state.policy_decision.decision
            state.stage = WorkflowStage.SUSPENDED
            self._checkpoint(
                state, "policy.denied_injection", state.policy_decision.model_dump(mode="json")
            )
            self._refresh_evidence(state)
            return state

        if not self.settings.source_path.exists():
            generate_maplebridge_source(self.settings.source_path)
        source = load_source(self.settings.source_path)
        state.dataset = DatasetAsset(
            id="ds_maplebridge_transactions_v1",
            name=request.dataset_name,
            version="1",
            path=str(self.settings.source_path),
            row_count=len(source),
            columns=list(source.columns),
        )
        state.stage = WorkflowStage.DATA_PROFILED
        self._checkpoint(
            state,
            "dataset.profiled",
            {
                "row_count": len(source),
                "columns": list(source.columns),
                "fraud_rate": float(source["is_fraud"].mean()),
            },
        )

        state.classifications = classify_fields(source)
        state.stage = WorkflowStage.CLASSIFIED
        self._checkpoint(
            state,
            "dataset.classified",
            {"classifications": [item.model_dump(mode="json") for item in state.classifications]},
        )
        permitted_fields = [
            item.field_name
            for item in state.classifications
            if item.disposition == ReleaseDisposition.PERMITTED
        ]
        removed_fields = [
            item.field_name
            for item in state.classifications
            if item.disposition == ReleaseDisposition.PROHIBITED
        ]
        release_source = source[permitted_fields].copy()

        state.generation_plan = GenerationPlan(
            generator=self.settings.generator,
            requested_rows=request.requested_rows,
            included_fields=permitted_fields,
            removed_fields=removed_fields,
            seed=20260804,
            unsafe_mode=request.scenario == Scenario.PRIVACY_LEAKAGE,
            configuration={
                "max_retries": self.settings.max_generation_retries,
                "max_runtime_seconds": self.settings.max_runtime_seconds,
            },
        )
        budget_exceeded = request.requested_rows > self.settings.max_rows
        if budget_exceeded:
            policy_input = self._policy_input(
                state,
                authority_valid=False,
                privacy_pass=True,
                utility_pass=True,
                evidence_complete=True,
                direct_identifiers=False,
                data_scope_valid=True,
                destination_allowed=True,
                violations=[],
                budget_exceeded=True,
            )
            state.policy_decision = self.policy.evaluate(policy_input)
            state.decision = state.policy_decision.decision
            state.stage = WorkflowStage.SUSPENDED
            self._checkpoint(
                state, "budget.suspended", state.policy_decision.model_dump(mode="json")
            )
            self._refresh_evidence(state)
            return state
        state.stage = WorkflowStage.PLAN_AUTHORIZED
        self._checkpoint(
            state, "generation.plan_authorized", state.generation_plan.model_dump(mode="json")
        )

        generator = build_generator(self.settings.generator)
        started = time.perf_counter()
        candidate = generator.generate(
            release_source,
            request.requested_rows,
            state.generation_plan.seed,
            unsafe_mode=state.generation_plan.unsafe_mode,
        )
        runtime = time.perf_counter() - started
        candidate_path = self.settings.data_dir / "candidate" / f"{state.candidate_id}_v1.csv"
        if candidate_path.exists():
            raise FileExistsError(f"Candidate version already exists: {candidate_path}")
        candidate.to_csv(candidate_path, index=False)
        state.generation_run = GenerationRun(
            candidate_id=state.candidate_id,
            candidate_version=1,
            path=str(candidate_path),
            row_count=len(candidate),
            runtime_seconds=round(runtime, 6),
            retry_count=0,
            generator=generator.name,
            configuration=state.generation_plan.configuration,
            content_hash=sha256_file(candidate_path),
        )
        state.stage = WorkflowStage.GENERATED
        self._checkpoint(state, "candidate.generated", state.generation_run.model_dump(mode="json"))

        state.utility_report = evaluate_utility(
            release_source, candidate, self.settings, state.generation_plan.seed
        )
        state.privacy_report = evaluate_privacy(
            release_source, candidate, self.settings, state.generation_plan.seed
        )
        external = request.destination == "named_external_partner"
        state.recipient_assessment = RecipientAssessment(
            recipient=request.recipient,
            destination=request.destination,
            external=external,
            approved_recipient=request.recipient
            in {"maplebridge_internal_fraud_sandbox", "northlake_analytics_partner"},
            auxiliary_data_risk="RESIDUAL" if external else "LOW",
            contract_boundary="named simulated partner" if external else "internal sandbox",
        )
        state.stage = WorkflowStage.EVALUATED
        self._checkpoint(
            state,
            "candidate.evaluated",
            {
                "utility": state.utility_report.model_dump(mode="json"),
                "privacy": state.privacy_report.model_dump(mode="json"),
                "recipient": state.recipient_assessment.model_dump(mode="json"),
            },
        )

        candidate_columns = set(candidate.columns)
        direct_names = {
            item.field_name
            for item in state.classifications
            if item.field_class.value == "DIRECT_IDENTIFIER"
        }
        policy_input = self._policy_input(
            state,
            authority_valid=authority_valid,
            privacy_pass=state.privacy_report.passed,
            utility_pass=state.utility_report.passed,
            evidence_complete=True,
            direct_identifiers=bool(candidate_columns & direct_names),
            data_scope_valid=candidate_columns.issubset(set(permitted_fields)),
            destination_allowed=request.destination
            in {"internal_sandbox", "named_external_partner"},
            violations=[],
        )
        state.policy_decision = self.policy.evaluate(policy_input)
        state.decision = state.policy_decision.decision
        explanation = self.model.explain(
            state.policy_decision.model_dump(mode="json"), trace_id=state.trace_id
        )
        self.audit.append(
            workflow_id=state.workflow_id,
            trace_id=state.trace_id,
            event_type="model.explanation",
            payload={"explanation": explanation},
        )

        if state.decision == Decision.REQUIRE_APPROVAL:
            state.stage = WorkflowStage.AWAITING_APPROVAL
            self._checkpoint(
                state, "approval.required", state.policy_decision.model_dump(mode="json")
            )
            self._refresh_evidence(state)
            return state
        if state.decision == Decision.ALLOW:
            state.stage = WorkflowStage.EVALUATED
            self._checkpoint(state, "policy.allowed", state.policy_decision.model_dump(mode="json"))
            evidence_dir = self._refresh_evidence(state)
            self._export(state, candidate_path, evidence_dir)
            return state
        if state.decision == Decision.DENY:
            state.stage = WorkflowStage.QUARANTINED
            state.remediation_proposal = "Regenerate with stronger disclosure controls, no copied rows, larger perturbation and reviewed rare-combination handling."
            quarantine = self.settings.data_dir / "quarantine" / candidate_path.name
            shutil.move(str(candidate_path), quarantine)
            state.generation_run.path = str(quarantine)
            self._checkpoint(
                state,
                "candidate.quarantined",
                {"reason": state.policy_decision.rationale, "path": str(quarantine)},
            )
            self._refresh_evidence(state)
            return state
        state.stage = (
            WorkflowStage.QUARANTINED
            if state.decision == Decision.QUARANTINE
            else WorkflowStage.SUSPENDED
        )
        self._checkpoint(state, "workflow.stopped", state.policy_decision.model_dump(mode="json"))
        self._refresh_evidence(state)
        return state

    def approve(
        self,
        workflow_id: str,
        role: ApprovalRole | str,
        approver_id: str,
        comment: str,
        outcome: ApprovalOutcome | str = ApprovalOutcome.APPROVE,
    ) -> WorkflowState:
        state = self.store.get(workflow_id)
        role = ApprovalRole(role)
        outcome = ApprovalOutcome(outcome)
        if state.stage != WorkflowStage.AWAITING_APPROVAL:
            raise ValueError("Workflow is not awaiting approval")
        if approver_id in {state.request.requester.id, state.request.agent.id}:
            raise PermissionError("Requester and workload agent cannot approve the release")
        if role not in {ApprovalRole.DATA_OWNER, ApprovalRole.PRIVACY_OFFICER}:
            raise PermissionError("Approver role is not authorized")
        if any(item.role == role for item in state.approvals):
            raise ValueError(f"Single-use approval for {role.value} already recorded")
        candidate_version = state.generation_run.candidate_version if state.generation_run else 0
        approval = ApprovalDecision(
            workflow_id=state.workflow_id,
            approver_id=approver_id,
            role=role,
            outcome=outcome,
            comment=comment,
            evidence_viewed=[artifact.path for artifact in state.evidence_artifacts],
            request_version=state.request.request_version,
            candidate_version=candidate_version,
        )
        self.store.add_approval(approval)
        state.approvals.append(approval)
        self._checkpoint(state, "approval.recorded", approval.model_dump(mode="json"))
        self._refresh_evidence(state)
        return state

    def resume(self, workflow_id: str) -> WorkflowState:
        state = self.store.get(workflow_id)
        if state.stage != WorkflowStage.AWAITING_APPROVAL:
            return state
        approved_roles = [a.role for a in state.approvals if a.outcome == ApprovalOutcome.APPROVE]
        rejected = any(a.outcome == ApprovalOutcome.REJECT for a in state.approvals)
        policy_input = self._policy_input(
            state,
            authority_valid=bool(state.authority and state.authority.valid),
            privacy_pass=bool(state.privacy_report and state.privacy_report.passed),
            utility_pass=bool(state.utility_report and state.utility_report.passed),
            evidence_complete=True,
            direct_identifiers=False,
            data_scope_valid=True,
            destination_allowed=state.request.destination
            in {"internal_sandbox", "named_external_partner"},
            violations=[],
            approved_roles=approved_roles,
            rejected_approval=rejected,
        )
        state.policy_decision = self.policy.evaluate(policy_input)
        state.decision = state.policy_decision.decision
        if state.decision == Decision.REQUIRE_APPROVAL:
            self._checkpoint(
                state,
                "approval.still_required",
                {"approved_roles": [role.value for role in approved_roles]},
            )
            self._refresh_evidence(state)
            return state

        generation_run = state.generation_run
        if generation_run is None:
            raise RuntimeError("Workflow has no generated candidate")

        if state.decision == Decision.DENY:
            state.stage = WorkflowStage.QUARANTINED
            candidate_path = Path(generation_run.path)

            if (
                candidate_path.exists()
                and candidate_path.parent == self.settings.data_dir / "candidate"
            ):
                quarantine = self.settings.data_dir / "quarantine" / candidate_path.name
                shutil.move(str(candidate_path), quarantine)
                generation_run.path = str(quarantine)

            self._checkpoint(
                state,
                "approval.rejected",
                state.policy_decision.model_dump(mode="json"),
            )
            self._refresh_evidence(state)
            return state

        state.stage = WorkflowStage.APPROVED
        self._checkpoint(
            state,
            "approval.complete",
            {"approved_roles": [role.value for role in approved_roles]},
        )
        evidence_dir = self._refresh_evidence(state)

        self._export(
            state,
            Path(generation_run.path),
            evidence_dir,
        )
        return state

    def set_kill_switch(
        self, name: str, enabled: bool, reason: str, updated_by: str = "local_operator"
    ) -> None:
        allowed = {"global_workflow", "export_only"}
        if name not in allowed and not name.startswith(("recipient:", "request:")):
            raise ValueError("Unsupported kill-switch scope")
        self.store.set_switch(name, enabled, reason, updated_by)
        self.audit.append(
            workflow_id=None,
            trace_id="operator",
            event_type="kill_switch.changed",
            payload={"name": name, "enabled": enabled, "reason": reason, "updated_by": updated_by},
        )

    def _policy_input(
        self,
        state: WorkflowState,
        *,
        authority_valid: bool,
        privacy_pass: bool,
        utility_pass: bool,
        evidence_complete: bool,
        direct_identifiers: bool,
        data_scope_valid: bool,
        destination_allowed: bool,
        violations: list[str],
        budget_exceeded: bool = False,
        approved_roles: list[ApprovalRole] | None = None,
        rejected_approval: bool = False,
    ) -> PolicyInput:
        global_kill = self.store.switch_enabled("global_workflow") or self.store.switch_enabled(
            f"request:{state.request_id}"
        )
        export_kill = self.store.switch_enabled("export_only") or self.store.switch_enabled(
            f"recipient:{state.request.recipient}"
        )
        return PolicyInput(
            identity_valid=state.request.requester.active
            and state.request.requester.role == "fraud_analyst",
            authority_valid=authority_valid,
            purpose_valid=state.request.purpose in {"fraud_research", "fraud_model_development"},
            data_scope_valid=data_scope_valid,
            direct_identifiers_present=direct_identifiers,
            tool_violations=violations,
            privacy_pass=privacy_pass,
            utility_pass=utility_pass,
            external_recipient=state.request.destination == "named_external_partner",
            destination_allowed=destination_allowed,
            approved_roles=approved_roles or [],
            rejected_approval=rejected_approval,
            evidence_complete=evidence_complete,
            kill_switch_enabled=global_kill,
            export_kill_switch_enabled=export_kill,
            budget_exceeded=budget_exceeded,
        )

    def _export(self, state: WorkflowState, candidate_path: Path, evidence_dir: Path) -> None:
        if self.store.switch_enabled("export_only") or self.store.switch_enabled(
            f"recipient:{state.request.recipient}"
        ):
            raise PermissionError("Export kill switch is enabled")
        state.export_receipt = self.export_gateway.release(state, candidate_path, evidence_dir)
        state.stage = WorkflowStage.RELEASED
        self._checkpoint(state, "dataset.released", state.export_receipt.model_dump(mode="json"))
        self._refresh_evidence(state)

    def _refresh_evidence(self, state: WorkflowState) -> Path:
        directory, artifacts = self.evidence.build(state)
        state.evidence_artifacts = artifacts
        state.updated_at = utcnow()
        self.store.save(state)
        return directory

    def _checkpoint(self, state: WorkflowState, event_type: str, payload: dict[str, Any]) -> None:
        state.updated_at = utcnow()
        self.store.save(state)
        self.audit.append(
            workflow_id=state.workflow_id,
            trace_id=state.trace_id,
            event_type=event_type,
            payload=payload,
        )


def build_service(settings: Settings | None = None) -> WorkflowService:
    settings = settings or Settings()
    settings.ensure_directories()
    database = Database(settings.database_url)
    database.create()
    store = SQLAlchemyWorkflowStore(database)
    audit_store = SQLAlchemyAuditStore(database)
    audit = AuditLedger(audit_store, settings.data_dir / "logs" / "audit.jsonl")
    evidence = EvidenceBuilder(settings.data_dir / "evidence", audit_store)
    export = LocalExportGateway(settings.data_dir)
    if settings.policy_engine == "opa":
        policy: PythonPolicyEngine | OPAPolicyAdapter = OPAPolicyAdapter(
            Path("data/policies/rego/release.rego")
        )
    else:
        policy = PythonPolicyEngine()
    if settings.model_gateway == "ollama":
        model: StubModelGateway | OllamaModelGateway = OllamaModelGateway(
            settings.ollama_url, settings.ollama_model, max_characters=settings.max_llm_characters
        )
    else:
        model = StubModelGateway()
    return WorkflowService(settings, store, audit, evidence, export, policy, model)
