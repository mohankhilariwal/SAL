from __future__ import annotations

import datetime as dt
import json
import urllib.error
import urllib.request
from dataclasses import asdict
from typing import Any

from ..canonical import canonical_json, sha256_hex
from ..models import AdapterConformanceRecord, TransportDeliveryReceipt


class HttpAdapterError(RuntimeError):
    pass


class HttpJsonAdapter:
    profile_id = "PRF-HTTP-JSON-1"

    def __init__(self, endpoint_url: str, *, timeout_seconds: float = 3.0) -> None:
        self.endpoint_url = endpoint_url
        self.timeout_seconds = timeout_seconds

    def deliver(self, payload: dict[str, Any]) -> TransportDeliveryReceipt:
        envelope = payload["envelope"]
        grant = payload["grant"]
        sender = payload["sender"]
        recipient = payload["recipient"]
        manifest = payload["manifest"]
        content = payload["content"]
        now = payload["now"]
        body_obj = {
            "contractVersion": "1.0.0",
            "sender": _wire(sender),
            "recipient": _wire(recipient),
            "grant": _wire(grant),
            "envelope": _wire(envelope),
            "manifest": _wire(manifest),
            "artifactContentUtf8": content.decode("utf-8"),
            "evaluationNow": _iso(now),
        }
        body = canonical_json(body_obj).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint_url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Content-Digest": f"sha-256=:{sha256_hex(body)}:",
                "X-NorthStar-Contract-Version": "1.0.0",
                "X-NorthStar-Correlation-Id": envelope.correlation_id,
                "X-NorthStar-Authority-Digest": grant.digest,
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read()
                status = response.status
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise HttpAdapterError(f"http_{exc.code}:{detail}") from exc
        except OSError as exc:
            raise HttpAdapterError(f"transport_unavailable:{exc}") from exc
        if status != 200:
            raise HttpAdapterError(f"unexpected_status:{status}")
        response_obj = json.loads(raw)
        required = {"receiptId", "terminalStatus", "responseContentDigest", "remoteEndpointId"}
        if not required.issubset(response_obj):
            raise HttpAdapterError("response_schema_invalid")
        return TransportDeliveryReceipt(
            receipt_id=response_obj["receiptId"],
            protocol_profile_id=self.profile_id,
            binding="HTTP+JSON",
            envelope_digest=envelope.digest,
            grant_digest=grant.digest,
            request_content_digest=sha256_hex(body),
            response_content_digest=response_obj["responseContentDigest"],
            correlation_id=envelope.correlation_id,
            task_id=envelope.task_id,
            terminal_status=response_obj["terminalStatus"],
            delivered_at=now,
            remote_endpoint_id=response_obj["remoteEndpointId"],
            semantic_loss=tuple(response_obj.get("semanticLoss", [])),
            warnings=tuple(response_obj.get("warnings", [])),
        )

    def conformance(self) -> AdapterConformanceRecord:
        native = {
            "authority": "X-NorthStar-Authority-Digest + signed DATA-093 body",
            "deadline": "DATA-092 deadlineAt plus client timeout",
            "cancellation": "application endpoint; not exercised concurrently in S06C",
            "artifact_integrity": "Content-Digest + DATA-095 contentSha256",
            "correlation": "X-NorthStar-Correlation-Id + DATA-092",
            "termination": "typed response consumed only by CMP-003",
        }
        return AdapterConformanceRecord(
            conformance_id="CONF-HTTP-001",
            protocol_profile_id=self.profile_id,
            canonical_fields=tuple(native),
            native_mappings=native,
            extension_mappings={},
            lost_fields=(),
            prohibited_semantics_observed=(),
            result="pass",
            notes="Serialized local reference boundary. HTTPS/mTLS/OAuth are production targets, not implemented.",
        )


def _iso(value: dt.datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _wire(value: Any) -> dict[str, Any]:
    result = asdict(value)
    for key, item in list(result.items()):
        if isinstance(item, dt.datetime):
            result[key] = _iso(item)
    return result
