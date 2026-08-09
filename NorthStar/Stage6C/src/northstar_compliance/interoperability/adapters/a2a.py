from __future__ import annotations

from typing import Any

from ..models import AdapterConformanceRecord, EndpointDescriptor, TaskEnvelope

NORTHSTAR_EXTENSION = "https://northstar.example/extensions/handoff-contract/v1"


class A2AMappingAdapter:
    profile_id = "PRF-A2A-1.0"

    def build_agent_card(self, endpoint: EndpointDescriptor, *, endpoint_url: str) -> dict[str, Any]:
        return {
            "name": endpoint.name,
            "description": "Sandbox-only evidence verification endpoint; not an allocated production agent.",
            "supportedInterfaces": [
                {
                    "url": endpoint_url,
                    "protocolBinding": "HTTP+JSON",
                    "protocolVersion": "1.0",
                }
            ],
            "version": endpoint.version,
            "capabilities": {
                "streaming": False,
                "pushNotifications": False,
                "extendedAgentCard": False,
                "extensions": [
                    {
                        "uri": NORTHSTAR_EXTENSION,
                        "description": "Preserves authority, deadline, correlation and termination-owner semantics.",
                        "required": True,
                    }
                ],
            },
            "securitySchemes": {
                "northstarOAuth": {
                    "oauth2SecurityScheme": {
                        "description": "Production target. Not implemented by the local reference sandbox.",
                        "flows": {},
                    }
                },
                "northstarMtls": {"mtlsSecurityScheme": {"description": "Production target."}},
            },
            "securityRequirements": [{"schemes": {"northstarOAuth": {"list": []}, "northstarMtls": {"list": []}}}],
            "defaultInputModes": ["application/json"],
            "defaultOutputModes": ["application/json"],
            "skills": [
                {
                    "id": "verify-supplied-evidence",
                    "name": "Verify supplied immutable evidence",
                    "description": "Validates one authorized DATA-095 artefact and emits DATA-096; never approves or finalizes.",
                    "tags": ["evidence", "integrity", "compliance"],
                    "inputModes": ["application/json"],
                    "outputModes": ["application/json"],
                }
            ],
            "metadata": {
                "northstarRuntimeStatus": endpoint.runtime_status,
                "northstarEndpointDigest": endpoint.digest,
                "northstarNoAgentAllocation": True,
            },
        }

    def map_task_message(self, envelope: TaskEnvelope, *, include_extension: bool = True) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "northstarEnvelopeDigest": envelope.digest,
            "northstarGrantDigest": envelope.authority_grant_digest,
            "northstarCaseId": envelope.case_id,
            "northstarRunId": envelope.run_id,
            "northstarDeadlineAt": envelope.deadline_at.isoformat().replace("+00:00", "Z"),
            "northstarCausationId": envelope.causation_id,
            "northstarTerminationOwner": "CMP-003",
            "northstarNotApproval": True,
        }
        if include_extension:
            metadata["extensions"] = [NORTHSTAR_EXTENSION]
        return {
            "message": {
                "role": "ROLE_USER",
                "messageId": envelope.envelope_id,
                "contextId": envelope.correlation_id,
                "taskId": envelope.task_id,
                "parts": [
                    {
                        "data": {
                            "purpose": envelope.purpose,
                            "goal": envelope.goal,
                            "nonGoals": list(envelope.non_goals),
                            "expectedOutputSchema": envelope.expected_output_schema,
                            "artifacts": [
                                {
                                    "artifactId": item.artifact_id,
                                    "contentSha256": item.content_sha256,
                                    "schemaId": item.schema_id,
                                }
                                for item in envelope.input_artifacts
                            ],
                        },
                        "mediaType": "application/json",
                    }
                ],
                "metadata": metadata,
            }
        }

    def map_status(self, northstar_status: str) -> str:
        mapping = {
            "offered": "TASK_STATE_SUBMITTED",
            "accepted": "TASK_STATE_SUBMITTED",
            "running": "TASK_STATE_WORKING",
            "completed": "TASK_STATE_COMPLETED",
            "failed": "TASK_STATE_FAILED",
            "cancelled": "TASK_STATE_CANCELED",
            "rejected": "TASK_STATE_REJECTED",
            "expired": "TASK_STATE_FAILED",
            "cancel_requested": "TASK_STATE_WORKING",
        }
        try:
            return mapping[northstar_status]
        except KeyError as exc:
            raise ValueError("unsupported_northstar_status") from exc

    def conformance_for_message(self, message: dict[str, Any]) -> AdapterConformanceRecord:
        metadata = message["message"].get("metadata", {})
        extension_active = NORTHSTAR_EXTENSION in metadata.get("extensions", [])
        required = {
            "authority": "northstarGrantDigest",
            "deadline": "northstarDeadlineAt",
            "correlation": "contextId",
            "causation": "northstarCausationId",
            "termination": "northstarTerminationOwner",
            "approval_boundary": "northstarNotApproval",
        }
        lost = tuple(key for key, mapped in required.items() if mapped not in metadata and mapped != "contextId")
        if not message["message"].get("contextId"):
            lost += ("correlation",)
        if not extension_active:
            lost += ("required_northstar_extension_declaration",)
        result = "pass" if not lost else "fail"
        return AdapterConformanceRecord(
            conformance_id="CONF-A2A-MESSAGE-001" if result == "pass" else "CONF-A2A-MESSAGE-FAIL-001",
            protocol_profile_id=self.profile_id,
            canonical_fields=tuple(required),
            native_mappings={
                "correlation": "Message.contextId",
                "task_identity": "Message.taskId / Task.id",
                "status": "TaskStatus.state",
                "artifact": "Task.artifacts",
                "version": "AgentInterface.protocolVersion",
            },
            extension_mappings={
                "authority": f"Message.metadata under {NORTHSTAR_EXTENSION}",
                "deadline": f"Message.metadata under {NORTHSTAR_EXTENSION}",
                "causation": f"Message.metadata under {NORTHSTAR_EXTENSION}",
                "termination": f"Message.metadata under {NORTHSTAR_EXTENSION}",
                "approval_boundary": f"Message.metadata under {NORTHSTAR_EXTENSION}",
            },
            lost_fields=lost,
            prohibited_semantics_observed=(),
            result=result,
            notes="A2A is conformance-only; AGT-002 remains unallocated and execution remains sequential.",
        )

    def conformance(self) -> AdapterConformanceRecord:
        return AdapterConformanceRecord(
            conformance_id="CONF-A2A-001",
            protocol_profile_id=self.profile_id,
            canonical_fields=("agent_card", "task", "message", "status", "artifact", "cancellation", "version"),
            native_mappings={
                "agent_card": "AgentCard",
                "task": "Task",
                "message": "Message",
                "status": "TaskStatus/TaskState",
                "artifact": "Artifact",
                "cancellation": "cancel task operation",
                "version": "supportedInterfaces.protocolVersion",
            },
            extension_mappings={"northstar_security_semantics": NORTHSTAR_EXTENSION},
            lost_fields=(),
            prohibited_semantics_observed=(),
            result="pass_with_required_extension",
            notes="Protocol mapping only. No remote A2A endpoint is served and no second agent is activated.",
        )
