import pytest

from governed_release.adapters.policy_python.engine import PythonPolicyEngine
from governed_release.domain.enums import ApprovalRole, Decision
from governed_release.domain.models import PolicyInput


def base(**overrides):
    values = dict(
        identity_valid=True,
        authority_valid=True,
        purpose_valid=True,
        data_scope_valid=True,
        direct_identifiers_present=False,
        tool_violations=[],
        privacy_pass=True,
        utility_pass=True,
        external_recipient=False,
        destination_allowed=True,
        approved_roles=[],
        rejected_approval=False,
        evidence_complete=True,
        authorization_expired=False,
        kill_switch_enabled=False,
        export_kill_switch_enabled=False,
        budget_exceeded=False,
    )
    values.update(overrides)
    return PolicyInput(**values)


@pytest.mark.parametrize(
    ("policy_input", "expected"),
    [
        (base(), Decision.ALLOW),
        (base(external_recipient=True), Decision.REQUIRE_APPROVAL),
        (
            base(
                external_recipient=True,
                approved_roles=[ApprovalRole.DATA_OWNER, ApprovalRole.PRIVACY_OFFICER],
            ),
            Decision.ALLOW,
        ),
        (base(privacy_pass=False), Decision.DENY),
        (base(utility_pass=False), Decision.QUARANTINE),
        (base(tool_violations=["RAW_DATA_EXPORT"]), Decision.DENY),
        (base(kill_switch_enabled=True), Decision.SUSPEND),
        (base(evidence_complete=False), Decision.QUARANTINE),
    ],
)
def test_policy_decisions(policy_input: PolicyInput, expected: Decision) -> None:
    assert PythonPolicyEngine().evaluate(policy_input).decision == expected


def test_policy_is_deterministic() -> None:
    engine = PythonPolicyEngine()
    value = base(external_recipient=True)
    assert engine.evaluate(value) == engine.evaluate(value)
