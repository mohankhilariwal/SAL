from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .engine import GuardrailEngine
from .lifecycle import PolicyRelease
from .models import GuardrailDecision, GuardrailRequest
from .policy import PolicyBundle


@dataclass(frozen=True)
class DistributionReceipt:
    receipt_id: str
    consumer_id: str
    bundle_id: str
    version: str
    digest: str
    received_at: str
    authority_effect: str = "none"


class BoundedControlPlane:
    """Stage 9C local control-plane slice.

    It validates, releases, distributes, pins and reports guardrail policy bundles.
    It is deliberately not a distributed production control plane and cannot change
    routes, approvals, agent inventory, AUTH-001 grants or DATA-106.
    """

    profile_id = "CP-001/0.1.0"

    def __init__(self) -> None:
        self._bundles: dict[tuple[str, str], PolicyBundle] = {}
        self._releases: dict[tuple[str, str], PolicyRelease] = {}
        self._active: dict[str, tuple[str, str]] = {}

    def register_release(self, bundle: PolicyBundle, release: PolicyRelease) -> None:
        if release.bundle_id != bundle.bundle_id or release.version != bundle.version or release.bundle_digest != bundle.digest:
            raise ValueError("release does not match bundle")
        key = (bundle.bundle_id, bundle.version)
        self._bundles[key] = bundle
        self._releases[key] = release

    def distribute(self, consumer_id: str, bundle_id: str, version: str) -> DistributionReceipt:
        key = (bundle_id, version)
        bundle = self._bundles[key]
        self._active[consumer_id] = key
        return DistributionReceipt(
            receipt_id=f"DIST-{consumer_id}-{bundle.digest[:10]}",
            consumer_id=consumer_id,
            bundle_id=bundle_id,
            version=version,
            digest=bundle.digest,
            received_at=datetime.now(timezone.utc).isoformat(),
        )

    def evaluate(self, consumer_id: str, request: GuardrailRequest) -> GuardrailDecision:
        key = self._active.get(consumer_id)
        if key is None:
            raise ValueError("consumer has no pinned bundle")
        bundle = self._bundles[key]
        if request.policy_bundle_id != bundle.bundle_id or request.policy_bundle_version != bundle.version:
            raise ValueError("request bundle pin does not match local active bundle")
        return GuardrailEngine(bundle).evaluate(request)

    def status(self) -> dict[str, object]:
        return {
            "profile_id": self.profile_id,
            "registered_releases": len(self._releases),
            "active_consumers": len(self._active),
            "production_ready": False,
            "full_control_plane_implemented": False,
            "stage8d_resolved": False,
            "can_issue_authority": False,
            "can_approve_or_finalize": False,
            "can_mutate_data106": False,
            "can_activate_routes": False,
        }
