from __future__ import annotations

from dataclasses import replace
from uuid import uuid4

from .lifecycle import ExceptionManager, GuardrailException
from .models import ControlFinding, GuardrailDecision, GuardrailRequest, Outcome, OUTCOME_SEVERITY
from .policy import PolicyBundle
from .validators import VALIDATORS


class GuardrailEngine:
    def __init__(self, bundle: PolicyBundle, exceptions: tuple[GuardrailException, ...] = ()) -> None:
        self.bundle = bundle
        self.exceptions = exceptions
        self.exception_manager = ExceptionManager()

    def evaluate(self, request: GuardrailRequest) -> GuardrailDecision:
        findings: list[ControlFinding] = []
        obligations: list[str] = []
        applied_exception: str | None = None
        blocking: list[Outcome] = []

        controls = self.bundle.controls_for(request.stage)
        if not controls:
            blocking.append(Outcome.DENY)
            obligations.append("no_active_controls_for_stage")

        for control in controls:
            validator = VALIDATORS.get(control.validator)
            if validator is None:
                passed, code, summary, outcome = False, "VALIDATOR_NOT_FOUND", f"Unknown validator {control.validator}", Outcome.DENY
            else:
                passed, code, summary, outcome = validator(request, control.parameters)

            exception = next(
                (
                    e for e in self.exceptions
                    if self.exception_manager.applicable(e, request, control.control_id)
                ),
                None,
            )
            if not passed and exception is not None and control.overrideable and not control.hard:
                passed = True
                code = "EXCEPTION_APPLIED"
                summary = f"Scoped exception {exception.exception_id} applied; compensating controls required"
                outcome = Outcome.ALLOW
                applied_exception = exception.exception_id
                obligations.extend(exception.compensating_controls)

            finding = ControlFinding(
                control_id=control.control_id,
                passed=passed,
                reason_code=code,
                summary=summary,
                hard=control.hard,
                synchronous=control.synchronous,
                outcome_on_fail=control.outcome_on_fail if not passed else Outcome.ALLOW,
                model_assisted=control.model_assisted,
            )
            findings.append(finding)

            if not passed:
                effective = outcome if outcome is not Outcome.ALLOW else control.outcome_on_fail
                if control.synchronous or control.hard:
                    blocking.append(effective)
                else:
                    obligations.append(f"async_follow_up:{control.control_id}:{code}")

        outcome = max(blocking, key=lambda x: OUTCOME_SEVERITY[x]) if blocking else Outcome.ALLOW
        reasons = tuple(f.reason_code for f in findings if not f.passed)
        return GuardrailDecision(
            decision_id=f"GRD-{uuid4().hex[:16]}",
            request_id=request.request_id,
            stage=request.stage,
            outcome=outcome,
            reason_codes=reasons,
            findings=tuple(findings),
            obligations=tuple(dict.fromkeys(obligations)),
            policy_bundle_id=self.bundle.bundle_id,
            policy_bundle_version=self.bundle.version,
            policy_bundle_digest=self.bundle.digest,
            exception_id=applied_exception,
        )
