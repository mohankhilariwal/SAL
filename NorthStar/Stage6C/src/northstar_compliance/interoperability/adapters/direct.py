from __future__ import annotations

import datetime as dt
from typing import Any

from ..canonical import canonical_json, sha256_hex
from ..models import AdapterConformanceRecord, TransportDeliveryReceipt
from ..validation import verify_artifact, verify_envelope, verify_grant
from ..fixtures import SIGNING_SECRET


class DirectAdapter:
    profile_id = "PRF-DIRECT-1"

    def deliver(self, payload: dict[str, Any]) -> TransportDeliveryReceipt:
        now = payload["now"]
        sender = payload["sender"]
        recipient = payload["recipient"]
        grant = payload["grant"]
        envelope = payload["envelope"]
        manifest = payload["manifest"]
        content = payload["content"]
        verify_grant(grant, secret=SIGNING_SECRET, recipient=recipient, now=now)
        verify_envelope(envelope, secret=SIGNING_SECRET, sender=sender, recipient=recipient, grant=grant, now=now)
        verify_artifact(manifest, content, recipient=recipient, envelope=envelope, grant=grant)
        response = {
            "schema": "DATA-096",
            "task_id": envelope.task_id,
            "result": "verified",
            "not_an_approval": True,
            "artifact_digest": manifest.digest,
        }
        return TransportDeliveryReceipt(
            receipt_id="RCP-DIRECT-001",
            protocol_profile_id=self.profile_id,
            binding="python-call",
            envelope_digest=envelope.digest,
            grant_digest=grant.digest,
            request_content_digest=sha256_hex(content),
            response_content_digest=sha256_hex(response),
            correlation_id=envelope.correlation_id,
            task_id=envelope.task_id,
            terminal_status="completed",
            delivered_at=now,
            remote_endpoint_id=recipient.endpoint_id,
        )

    def conformance(self) -> AdapterConformanceRecord:
        fields = ("authority", "deadline", "cancellation", "artifact_integrity", "correlation", "termination")
        return AdapterConformanceRecord(
            conformance_id="CONF-DIRECT-001",
            protocol_profile_id=self.profile_id,
            canonical_fields=fields,
            native_mappings={field: "in_process_object" for field in fields},
            extension_mappings={},
            lost_fields=(),
            prohibited_semantics_observed=(),
            result="pass",
            notes="Reference only; no interoperability claim.",
        )
