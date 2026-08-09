from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from .canonical import sha256_digest
from .models import GuardrailRequest
from .policy import GuardrailControl, PolicyBundle


@dataclass(frozen=True)
class PolicyChangeSet:
    change_id: str
    bundle_id: str
    from_version: str
    to_version: str
    changed_controls: tuple[str, ...]
    requester_id: str
    rationale: str


@dataclass(frozen=True)
class PolicyRelease:
    release_id: str
    bundle_id: str
    version: str
    bundle_digest: str
    approvers: tuple[str, ...]
    released_at: str
    authority_effect: str = "none"


@dataclass(frozen=True)
class GuardrailException:
    exception_id: str
    control_ids: tuple[str, ...]
    tenant_id: str
    case_id: str
    operation: str
    requested_by: str
    approved_by: tuple[str, ...]
    starts_at: str
    expires_at: str
    rationale: str
    compensating_controls: tuple[str, ...]
    status: str = "approved"
    authority_effect: str = "none"


class PolicyLifecycle:
    """Design/build-time lifecycle; does not deploy a production control plane."""

    def release(
        self,
        bundle: PolicyBundle,
        change: PolicyChangeSet,
        *,
        validation_passed: bool,
        tests_passed: bool,
        approvers: Iterable[str],
    ) -> PolicyRelease:
        approved = tuple(dict.fromkeys(approvers))
        if bundle.status != "approved":
            raise ValueError("bundle must be approved before release")
        if not validation_passed or not tests_passed:
            raise ValueError("validation and tests must pass before release")
        if len(approved) < 2 or change.requester_id in approved:
            raise ValueError("release requires two distinct approvers independent of requester")
        return PolicyRelease(
            release_id=f"REL-{sha256_digest((change.change_id, bundle.digest))[:12]}",
            bundle_id=bundle.bundle_id,
            version=bundle.version,
            bundle_digest=bundle.digest,
            approvers=approved,
            released_at=datetime.now(timezone.utc).isoformat(),
        )


class ExceptionManager:
    MAX_DURATION_SECONDS = 30 * 24 * 60 * 60

    def approve(self, exception: GuardrailException, controls: Iterable[GuardrailControl]) -> GuardrailException:
        control_map = {c.control_id: c for c in controls}
        selected = [control_map[cid] for cid in exception.control_ids]
        if any(c.hard or not c.overrideable for c in selected):
            raise ValueError("hard or non-overrideable controls cannot receive exceptions")
        if len(set(exception.approved_by)) < 2 or exception.requested_by in set(exception.approved_by):
            raise ValueError("exception requires two independent approvers")
        if not exception.compensating_controls:
            raise ValueError("exception requires compensating controls")
        start = datetime.fromisoformat(exception.starts_at)
        end = datetime.fromisoformat(exception.expires_at)
        if end <= start or (end - start).total_seconds() > self.MAX_DURATION_SECONDS:
            raise ValueError("exception expiry must be within 30 days")
        return exception

    def applicable(self, exception: GuardrailException, request: GuardrailRequest, control_id: str, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return (
            exception.status == "approved"
            and control_id in exception.control_ids
            and exception.tenant_id == request.tenant_id
            and exception.case_id == request.case_id
            and exception.operation == request.metadata.get("operation", "")
            and datetime.fromisoformat(exception.starts_at) <= now <= datetime.fromisoformat(exception.expires_at)
        )
