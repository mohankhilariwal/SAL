import pytest

from northstar_compliance.observability import CorrelationContext, InvalidTraceContext


def make_root():
    return CorrelationContext.new_root(
        session_id="SES-1", run_id="RUN-1", task_id="TASK-1", case_id="CASE-1", tenant_id="TEN-1"
    )


def test_881_root_identifiers_are_valid():
    ctx = make_root()
    assert len(ctx.trace_id) == 32 and int(ctx.trace_id, 16) != 0
    assert len(ctx.span_id) == 16 and int(ctx.span_id, 16) != 0


def test_882_traceparent_round_trip():
    ctx = make_root()
    parsed = CorrelationContext.from_traceparent(
        ctx.traceparent,
        session_id="SES-2", run_id="RUN-2", task_id="TASK-2", case_id="CASE-2", tenant_id="TEN-2"
    )
    assert parsed.trace_id == ctx.trace_id
    assert parsed.parent_span_id == ctx.span_id


def test_883_child_preserves_trace_and_changes_span():
    ctx = make_root()
    child = ctx.child()
    assert child.trace_id == ctx.trace_id
    assert child.span_id != ctx.span_id
    assert child.parent_span_id == ctx.span_id


@pytest.mark.parametrize(
    "value",
    [
        "bad",
        "00-0-0-00",
        "ff-0123456789abcdef0123456789abcdef-0123456789abcdef-01",
        "00-00000000000000000000000000000000-0123456789abcdef-01",
        "00-0123456789abcdef0123456789abcdef-0000000000000000-01",
    ],
)
def test_884_to_888_invalid_traceparent_is_rejected(value):
    with pytest.raises(InvalidTraceContext):
        CorrelationContext.from_traceparent(
            value,
            session_id="S", run_id="R", task_id="T", case_id="C", tenant_id="N"
        )


def test_889_trace_context_has_no_authority_effect():
    assert make_root().authority_effect == "none"


def test_890_safe_attributes_include_stable_agent_identity():
    attrs = make_root().safe_attributes()
    assert attrs["agent_id"] == "AGT-001"
    assert attrs["agent_spec_version"] == "1.1.0"


def test_891_traceparent_does_not_carry_tenant_or_case():
    ctx = make_root()
    assert "TEN-1" not in ctx.traceparent
    assert "CASE-1" not in ctx.traceparent


def test_892_external_context_cannot_override_authority_fields():
    ctx = make_root()
    parsed = CorrelationContext.from_traceparent(
        ctx.traceparent,
        session_id="ATTACKER", run_id="RUN-X", task_id="TASK-X", case_id="CASE-X", tenant_id="TEN-X"
    )
    assert parsed.tenant_id == "TEN-X"
    assert parsed.authority_effect == "none"
