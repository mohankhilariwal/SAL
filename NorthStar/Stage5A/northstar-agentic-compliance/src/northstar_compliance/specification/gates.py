from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .models import AgentSpecification, DeploymentGateResult, SpecificationValidationReport


class DeploymentGateEvaluator:
    """Fail-closed local deployment gate derived from the accepted specification."""

    def evaluate(
        self,
        specification: AgentSpecification,
        validation_report: SpecificationValidationReport,
        evidence: Mapping[str, Any],
        *,
        gate_profile: str = "stage5a-local",
    ) -> DeploymentGateResult:
        required_evals = set(specification.raw["evaluation"]["required_evaluations"])
        eval_results = evidence.get("evaluations", {})
        passed_evals = {eval_id for eval_id, result in eval_results.items() if result is True}
        required_tests = set(specification.raw["traceability"]["tests"])
        test_results = evidence.get("tests", {})
        passed_tests = {test_id for test_id, result in test_results.items() if result is True}

        checks = {
            "specification_valid": validation_report.valid,
            "specification_active": specification.status == "active",
            "digest_attested": evidence.get("specification_digest") == specification.digest,
            "required_evaluations_passed": required_evals <= passed_evals,
            "required_tests_passed": required_tests <= passed_tests,
            "security_findings_zero": int(evidence.get("blocking_security_findings", 1)) == 0,
            "future_stage_flags_disabled": evidence.get("future_stage_flags") == {
                "memory_enabled": False,
                "concurrent_graph_branches": False,
                "multiple_agents_enabled": False,
            },
            "human_approval_semantics_passed": evidence.get("human_approval_semantics") is True,
            "no_final_legal_closure": evidence.get("final_legal_or_compliance_closure") is False,
        }
        blocking = tuple(name for name, passed in checks.items() if not passed)
        return DeploymentGateResult(not blocking, gate_profile, checks, blocking)
