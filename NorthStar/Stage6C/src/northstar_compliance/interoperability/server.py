from __future__ import annotations

import argparse
import datetime as dt
import json
from dataclasses import fields
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, TypeVar, Type

from .canonical import canonical_json, sha256_hex
from .fixtures import SIGNING_SECRET
from .models import ArtifactManifest, AuthorityGrant, EndpointDescriptor, TaskEnvelope
from .validation import ContractError, verify_artifact, verify_envelope, verify_grant

T = TypeVar("T")


def _parse_time(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def _restore(cls: Type[T], data: dict[str, Any]) -> T:
    data = dict(data)
    time_fields = {"issued_at", "expires_at", "sent_at", "deadline_at"}
    tuple_fields = {
        "allowed_purposes",
        "accepted_input_schemas",
        "accepted_output_schemas",
        "allowed_tools",
        "allowed_data_scopes",
        "allowed_operations",
        "allowed_resources",
        "authorized_subjects",
        "provenance_refs",
        "non_goals",
    }
    for key in time_fields & data.keys():
        data[key] = _parse_time(data[key])
    for key in tuple_fields & data.keys():
        data[key] = tuple(data[key])
    if cls is TaskEnvelope:
        data["input_artifacts"] = tuple(ArtifactManifest(**item) for item in data["input_artifacts"])
    return cls(**data)


class ReferenceHandler(BaseHTTPRequestHandler):
    server_version = "NorthStarReference/1.5.0"

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/handoff":
            self._send(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            expected_header = f"sha-256=:{sha256_hex(raw)}:"
            if self.headers.get("Content-Digest") != expected_header:
                raise ContractError("http_content_digest_invalid")
            if self.headers.get("X-NorthStar-Contract-Version") != "1.0.0":
                raise ContractError("http_contract_version_unsupported")
            data = json.loads(raw)
            if data.get("contractVersion") != "1.0.0":
                raise ContractError("payload_contract_version_unsupported")
            sender = _restore(EndpointDescriptor, data["sender"])
            recipient = _restore(EndpointDescriptor, data["recipient"])
            grant = _restore(AuthorityGrant, data["grant"])
            envelope = _restore(TaskEnvelope, data["envelope"])
            manifest = _restore(ArtifactManifest, data["manifest"])
            content = data["artifactContentUtf8"].encode("utf-8")
            now = _parse_time(data["evaluationNow"])
            if self.headers.get("X-NorthStar-Correlation-Id") != envelope.correlation_id:
                raise ContractError("http_correlation_mismatch")
            if self.headers.get("X-NorthStar-Authority-Digest") != grant.digest:
                raise ContractError("http_authority_digest_mismatch")
            verify_grant(grant, secret=SIGNING_SECRET, recipient=recipient, now=now)
            verify_envelope(envelope, secret=SIGNING_SECRET, sender=sender, recipient=recipient, grant=grant, now=now)
            verify_artifact(manifest, content, recipient=recipient, envelope=envelope, grant=grant)
            result = {
                "schema": "DATA-096",
                "taskId": envelope.task_id,
                "result": "verified",
                "notAnApproval": True,
                "sourceArtifactDigest": manifest.digest,
            }
            self._send(
                200,
                {
                    "receiptId": "RCP-HTTP-001",
                    "terminalStatus": "completed",
                    "responseContentDigest": sha256_hex(result),
                    "remoteEndpointId": recipient.endpoint_id,
                    "semanticLoss": [],
                    "warnings": ["local_reference_transport_not_production_https"],
                },
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError, ContractError) as exc:
            self._send(400, {"error": str(exc)})

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send(self, status: int, body: dict[str, Any]) -> None:
        raw = canonical_json(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), ReferenceHandler)
    print(f"READY {args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
