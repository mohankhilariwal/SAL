from datetime import timedelta

import pytest

from northstar_compliance.handoff.fixtures import build_signed_fixture
from northstar_compliance.handoff.lifecycle import HandoffCoordinator, LifecycleError
from northstar_compliance.handoff.models import HandoffStatus


def test_291_valid_sequential_lifecycle_completes():
    f = build_signed_fixture()
    c = HandoffCoordinator()
    c.register(f["envelope"])
    c.transition("ENV-001", HandoffStatus.ACCEPTED, actor_id=f["recipient"].endpoint_id, reason_code="accepted", now=f["now"])
    c.transition("ENV-001", HandoffStatus.RUNNING, actor_id=f["recipient"].endpoint_id, reason_code="running", now=f["now"])
    c.transition("ENV-001", HandoffStatus.COMPLETED, actor_id=f["recipient"].endpoint_id, reason_code="done", now=f["now"])
    assert c.current("ENV-001").status is HandoffStatus.COMPLETED
    assert c.system_termination_ready(("ENV-001",))


def test_292_invalid_transition_is_rejected():
    f = build_signed_fixture()
    c = HandoffCoordinator()
    c.register(f["envelope"])
    with pytest.raises(LifecycleError, match="invalid_status_transition"):
        c.transition("ENV-001", HandoffStatus.COMPLETED, actor_id="AGT-001", reason_code="skip", now=f["now"])


def test_293_terminal_state_cannot_transition():
    f = build_signed_fixture()
    c = HandoffCoordinator()
    c.register(f["envelope"])
    c.transition("ENV-001", HandoffStatus.REJECTED, actor_id=f["recipient"].endpoint_id, reason_code="reject", now=f["now"])
    with pytest.raises(LifecycleError, match="terminal_transition_prohibited"):
        c.transition("ENV-001", HandoffStatus.ACCEPTED, actor_id="AGT-001", reason_code="late", now=f["now"])


def test_294_timeout_requires_expired_or_cancelled_terminal():
    f = build_signed_fixture()
    c = HandoffCoordinator()
    c.register(f["envelope"])
    after = f["envelope"].deadline_at + timedelta(seconds=1)
    with pytest.raises(LifecycleError, match="deadline_passed"):
        c.transition("ENV-001", HandoffStatus.ACCEPTED, actor_id=f["recipient"].endpoint_id, reason_code="late", now=after)
    c.transition("ENV-001", HandoffStatus.EXPIRED, actor_id="CMP-003", reason_code="deadline", now=after)
    assert c.system_termination_ready(("ENV-001",))


def test_295_cancel_request_requires_ack_or_terminal_failure():
    f = build_signed_fixture()
    c = HandoffCoordinator()
    c.register(f["envelope"])
    c.transition("ENV-001", HandoffStatus.ACCEPTED, actor_id=f["recipient"].endpoint_id, reason_code="accepted", now=f["now"])
    c.transition("ENV-001", HandoffStatus.CANCEL_REQUESTED, actor_id="CMP-003", reason_code="user_cancel", now=f["now"])
    c.transition("ENV-001", HandoffStatus.CANCELLED, actor_id=f["recipient"].endpoint_id, reason_code="cancel_ack", now=f["now"])
    assert c.current("ENV-001").status is HandoffStatus.CANCELLED


def test_296_duplicate_envelope_is_rejected():
    f = build_signed_fixture()
    c = HandoffCoordinator()
    c.register(f["envelope"])
    with pytest.raises(LifecycleError, match="duplicate_envelope"):
        c.register(f["envelope"])


def test_297_termination_requires_all_tasks_terminal():
    f = build_signed_fixture()
    c = HandoffCoordinator()
    c.register(f["envelope"])
    assert not c.system_termination_ready(("ENV-001",))
