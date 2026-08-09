# 05 — Data and Schema Register — Version 1.15.0 Overlay

Preserve `DATA-001–216` and `INT-001–176`. Add:

## Data objects

| ID | Name | Owner |
|---|---|---|
| DATA-217 | CorrelationContext | CMP-003/CMP-009 |
| DATA-218 | TelemetryEvent | CMP-009 |
| DATA-219 | TraceSpan | CMP-009 |
| DATA-220 | StructuredLogRecord | CMP-009 |
| DATA-221 | MetricPoint | CMP-009 |
| DATA-222 | ModelInvocationTelemetry | Harness/CMP-009 |
| DATA-223 | RetrievalTelemetry | CMP-004 |
| DATA-224 | ToolInvocationTelemetry | CMP-005 |
| DATA-225 | PolicyDecisionTelemetry | CMP-007/PEPs |
| DATA-226 | HumanApprovalTelemetry | CMP-006 |
| DATA-227 | StateTransitionTelemetry | CMP-003 |
| DATA-228 | RedactionResult | CMP-009 |
| DATA-229 | AuditEvent | CMP-009 |
| DATA-230 | AuditChainCheckpoint | CMP-009 |
| DATA-231 | AuditVerificationReport | CMP-009 |
| DATA-232 | EvidencePackageManifest | CMP-009/CMP-011 |
| DATA-233 | EvidencePackage | CMP-009 |
| DATA-234 | TelemetrySamplingPolicy | CMP-011 |
| DATA-235 | TelemetryRetentionPolicy | CMP-011 |
| DATA-236 | ObservabilityStatusReport | CMP-009/CMP-010 |

All require `authority_effect: none`.

## Interfaces

`INT-177` PropagateTraceContext; `178` StartRunTrace; `179` StartComponentSpan; `180` RecordStructuredEvent; `181` RecordMetric; `182` RecordModelInvocation; `183` RecordRetrieval; `184` RecordToolInvocation; `185` RecordPolicyDecision; `186` RecordHumanApproval; `187` RecordStateTransition; `188` RedactTelemetry; `189` AppendAuditEvent; `190` VerifyAuditChain; `191` CreateAuditCheckpoint; `192` BuildEvidencePackage; `193` VerifyEvidencePackage; `194` QueryTrace; `195` ExportTelemetryBatch; `196` GetObservabilityStatus.

None can issue authority, approve/finalize, invoke a tool outside CMP-005, mutate DATA-106 or activate a route.
