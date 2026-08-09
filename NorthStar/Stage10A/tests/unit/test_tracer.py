import pytest

from northstar_compliance.observability import CorrelationContext, InMemoryTracer, SamplingPolicy


def ctx():
    return CorrelationContext.new_root(
        session_id="SES", run_id="RUN", task_id="TASK", case_id="CASE", tenant_id="TEN"
    )


@pytest.mark.parametrize(
    "event",
    [
        "authorization.denied",
        "guardrail.denied",
        "tool.write.requested",
        "tool.write.completed",
        "human.approval.decided",
        "task.disposed",
    ],
)
def test_905_to_910_material_events_are_always_sampled(event):
    policy = SamplingPolicy(ratio=0.0)
    assert policy.should_sample(ctx().trace_id, event)


def test_911_success_event_can_be_unsampled():
    policy = SamplingPolicy(ratio=0.0)
    assert not policy.should_sample(ctx().trace_id, "retrieval.completed", "ok")


def test_912_error_event_is_sampled_even_at_zero_ratio():
    policy = SamplingPolicy(ratio=0.0)
    assert policy.should_sample(ctx().trace_id, "retrieval.completed", "error")


def test_913_span_records_duration_and_status():
    tracer = InMemoryTracer(sampling=SamplingPolicy(ratio=1.0))
    with tracer.start_span("northstar.retrieval", ctx(), component_id="CMP-004") as span:
        span.add_event("retrieval.query", {"query": "safe"})
    assert tracer.spans[0].duration_ms >= 0
    assert tracer.spans[0].status == "OK"


def test_914_span_redacts_sensitive_attributes():
    tracer = InMemoryTracer(sampling=SamplingPolicy(ratio=1.0))
    handle = tracer.start_span("model.invoke", ctx(), component_id="CMP-003", attributes={"raw_prompt": "secret"})
    handle.end()
    assert tracer.spans[0].attributes["raw_prompt"] == "[REDACTED]"


def test_915_event_is_structured_and_non_authorizing():
    tracer = InMemoryTracer(sampling=SamplingPolicy(ratio=1.0))
    event = tracer.record_event("task.started", ctx(), component_id="CMP-003", attributes={"x": 1})
    assert event is not None
    data = event.to_dict()
    assert data["event_name"] == "task.started"
    assert data["authority_effect"] == "none"


@pytest.mark.parametrize("label", ["run_id", "case_id", "trace_id"])
def test_916_to_918_high_cardinality_metric_labels_are_rejected(label):
    tracer = InMemoryTracer()
    with pytest.raises(ValueError):
        tracer.metrics.record("northstar.run.duration", 1, "ms", {label: "value"})
