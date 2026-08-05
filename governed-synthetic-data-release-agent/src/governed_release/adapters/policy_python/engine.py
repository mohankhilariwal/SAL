from __future__ import annotations

from governed_release.domain.enums import ApprovalRole, Decision
from governed_release.domain.models import PolicyDecision, PolicyFinding, PolicyInput

POLICY_VERSION = "2026.08.1"


class PythonPolicyEngine:
    """Deterministic policy decision point. Identical normalized input yields identical output."""

    def findings(self, value: PolicyInput) -> list[PolicyFinding]:
        checks = [
            PolicyFinding(
                policy_id="POL-ID-001",
                passed=value.identity_valid,
                message="Requester identity and active role validated.",
            ),
            PolicyFinding(
                policy_id="POL-AUTH-001",
                passed=value.authority_valid and not value.authorization_expired,
                message="Delegated authority is request-specific and unexpired.",
            ),
            PolicyFinding(
                policy_id="POL-PUR-001", passed=value.purpose_valid, message="Purpose is approved."
            ),
            PolicyFinding(
                policy_id="POL-DATA-001",
                passed=value.data_scope_valid,
                message="Source column and row scope is authorized.",
            ),
            PolicyFinding(
                policy_id="POL-PII-001",
                passed=not value.direct_identifiers_present,
                message="Direct identifiers are prohibited from release.",
            ),
            PolicyFinding(
                policy_id="POL-TOOL-001",
                passed=not value.tool_violations,
                message="Tool calls are within allow-list and argument constraints.",
            ),
            PolicyFinding(
                policy_id="POL-PRIV-001", passed=value.privacy_pass, message="Privacy gates passed."
            ),
            PolicyFinding(
                policy_id="POL-UTIL-001",
                passed=value.utility_pass,
                message="Minimum analytical utility passed.",
            ),
            PolicyFinding(
                policy_id="POL-RECIP-001",
                passed=value.destination_allowed,
                message="Recipient and destination are approved.",
            ),
            PolicyFinding(
                policy_id="POL-EVID-001",
                passed=value.evidence_complete,
                message="Mandatory pre-decision evidence is complete.",
            ),
            PolicyFinding(
                policy_id="POL-BUD-001",
                passed=not value.budget_exceeded,
                message="Execution budget is within limits.",
            ),
            PolicyFinding(
                policy_id="POL-KILL-001",
                passed=not value.kill_switch_enabled and not value.export_kill_switch_enabled,
                message="Kill switches permit processing and export.",
            ),
            PolicyFinding(
                policy_id="POL-INJ-001",
                passed=not value.tool_violations,
                message="No prompt-injection authority-boundary violation detected.",
            ),
        ]
        approval_ok = (not value.external_recipient) or (
            set(value.approved_roles) == {ApprovalRole.DATA_OWNER, ApprovalRole.PRIVACY_OFFICER}
            and not value.rejected_approval
        )
        checks.append(
            PolicyFinding(
                policy_id="POL-APP-001",
                passed=approval_ok,
                message="Required independent approvals are recorded.",
            )
        )
        return checks

    def evaluate(self, value: PolicyInput) -> PolicyDecision:
        findings = self.findings(value)
        failed = [f.policy_id for f in findings if not f.passed]
        triggered: list[str] = []
        required: list[ApprovalRole] = []
        permitted: list[str] = []
        prohibited = [
            "modify_policy",
            "lower_privacy_thresholds",
            "self_approve",
            "arbitrary_export",
        ]

        if value.kill_switch_enabled or value.export_kill_switch_enabled:
            decision = Decision.SUSPEND
            rationale = "Workflow or export kill switch is enabled."
            triggered = ["POL-KILL-001"]
            permitted = ["operator_review", "disable_kill_switch"]
        elif value.tool_violations:
            decision = Decision.DENY
            rationale = "Purpose, data-scope, tool and export-policy violations were detected."
            triggered = ["POL-INJ-001", "POL-TOOL-001", "POL-DATA-001", "POL-EXP-001"]
            permitted = ["operator_review", "create_clean_request"]
            prohibited.extend(["resume_without_operator", "raw_data_export", "evaluator_bypass"])
        elif not value.identity_valid:
            decision = Decision.DENY
            rationale = "Requester identity or active role is invalid."
            triggered = ["POL-ID-001"]
            permitted = ["correct_identity"]
        elif not value.authority_valid or value.authorization_expired:
            decision = Decision.DENY
            rationale = "Delegated authority is absent, invalid or expired."
            triggered = ["POL-AUTH-001", "POL-RET-001"]
            permitted = ["obtain_new_authority"]
        elif not value.purpose_valid:
            decision = Decision.DENY
            rationale = "The requested purpose is not approved."
            triggered = ["POL-PUR-001"]
            permitted = ["submit_approved_purpose"]
        elif not value.data_scope_valid or value.direct_identifiers_present:
            decision = Decision.DENY
            rationale = (
                "Release candidate contains prohibited identifiers or exceeds delegated data scope."
            )
            triggered = ["POL-DATA-001", "POL-PII-001"]
            permitted = ["regenerate_without_prohibited_fields"]
        elif not value.privacy_pass:
            decision = Decision.DENY
            rationale = "Disclosure risk is above the configured privacy threshold."
            triggered = ["POL-PRIV-001"]
            permitted = ["quarantine", "regenerate_with_stronger_controls"]
            prohibited.extend(["export", "manual_release"])
        elif not value.utility_pass:
            decision = Decision.QUARANTINE
            rationale = "Candidate does not meet minimum analytical utility."
            triggered = ["POL-UTIL-001"]
            permitted = ["quarantine", "adjust_generation_plan", "regenerate"]
            prohibited.append("export")
        elif not value.destination_allowed:
            decision = Decision.DENY
            rationale = "Recipient or destination is outside the allow-list."
            triggered = ["POL-RECIP-001", "POL-EXP-001"]
            permitted = ["select_approved_destination"]
        elif not value.evidence_complete:
            decision = Decision.QUARANTINE
            rationale = "Mandatory evidence is incomplete."
            triggered = ["POL-EVID-001"]
            permitted = ["complete_evidence"]
            prohibited.append("export")
        elif value.budget_exceeded:
            decision = Decision.SUSPEND
            rationale = "Execution budget was exceeded."
            triggered = ["POL-BUD-001"]
            permitted = ["operator_review", "new_request_with_authorized_budget"]
        elif value.rejected_approval:
            decision = Decision.DENY
            rationale = "A required independent approver rejected the release."
            triggered = ["POL-APP-001"]
            permitted = ["quarantine", "create_revised_candidate"]
            prohibited.append("export")
        elif value.external_recipient and set(value.approved_roles) != {
            ApprovalRole.DATA_OWNER,
            ApprovalRole.PRIVACY_OFFICER,
        }:
            decision = Decision.REQUIRE_APPROVAL
            rationale = "External release has residual auxiliary-information risk and requires Data Owner and Privacy Officer approval."
            triggered = ["POL-RECIP-001", "POL-APP-001"]
            required = [ApprovalRole.DATA_OWNER, ApprovalRole.PRIVACY_OFFICER]
            permitted = ["record_data_owner_approval", "record_privacy_officer_approval", "reject"]
            prohibited.extend(["export", "requester_self_approval", "agent_self_approval"])
        else:
            decision = Decision.ALLOW
            rationale = "Identity, authority, purpose, data scope, privacy, utility, recipient, evidence, budget and approval controls passed."
            triggered = [f.policy_id for f in findings]
            permitted = ["build_evidence_bundle", "export_through_gateway"]
            prohibited.extend(["direct_file_copy", "change_candidate_after_approval"])

        return PolicyDecision(
            decision=decision,
            rationale=rationale,
            triggered_policies=triggered,
            failed_controls=failed,
            required_approvals=required,
            permitted_next_actions=permitted,
            prohibited_next_actions=prohibited,
            evidence_requirements=[
                "request",
                "identity",
                "delegated_authority",
                "classification",
                "generation_plan",
                "utility_report",
                "privacy_report",
                "recipient_assessment",
                "policy_input",
                "policy_output",
            ],
            expiry_conditions=[
                "release expires after the authorized duration",
                "candidate modification invalidates approvals",
            ],
            policy_version=POLICY_VERSION,
        )
