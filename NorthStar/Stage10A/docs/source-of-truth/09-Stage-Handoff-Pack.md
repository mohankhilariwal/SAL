# Stage Handoff Pack

## A. Stage completed

- Stage identifier: `S10A`
- Stage title: Observability and Audit
- Architecture version: `1.15.0`
- Repository version: `1.15.0`
- Handoff version: `1.15.0`
- Graph version: `GRAPH-001/1.11.0`
- Threat-model version: `TM-001/1.3.0`
- Authorization-model version: `AUTH-001/1.0.0` unchanged
- Blast-radius-model version: `BR-001/1.0.0` unchanged
- Guardrail-model version: `GR-001/1.0.0` unchanged
- Governance-model version: `GOV-001/1.0.0` unchanged
- Control-plane profile: `CP-001/0.1.0` unchanged; Stage 9D remains unresolved
- Observability model: `OBS-001/1.0.0`
- Audit model: `AUD-001/1.0.0`
- Evidence-package model: `EVID-001/1.0.0`
- Completion date: 2026-08-01
- Status: completed as a provider-neutral architecture and executable local reference. No production collector/backend, WORM storage, KMS/HSM-backed signing, trusted timestamp authority, multi-region durability, enterprise retention determination, Stage 9D control plane, Stage 8D promotion eligibility, production route, certification or legal-admissibility claim.
- Consistency audit: passed with recorded exceptions.

## B. Capabilities now available

1. `CMP-009` distinguishes operational observability from accountability audit while keeping both non-authorizing.
2. Correlation spans user request, orchestration, `AGT-001`, model calls, retrieval, tools, policy decisions, human approvals, state transitions, evaluation and final disposition.
3. W3C-compatible trace context is accepted only as untrusted correlation input; identity, tenancy and authority are supplied by accepted NorthStar sources.
4. Structured logs, events, traces and low-cardinality metrics use a provider-neutral canonical schema suitable for future OpenTelemetry adapters.
5. Raw prompts, responses, documents, tool arguments, credentials and secrets are excluded by default; metadata, counts, references, versions and digests are preferred.
6. Operational telemetry may be sampled or buffered. Mandatory accountability events are never sampled.
7. Protected effects require a durable audit intent before execution and a durable outcome after execution. A mandatory append failure blocks the protected effect.
8. `AUD-001/1.0.0` provides canonical JSON, monotonic sequence, payload hash, previous-record hash and HMAC-SHA256 authenticity in a local append-only file.
9. Chain verification detects payload changes, record changes, reordering, deletion, duplicate event IDs, duplicate idempotency keys and signature mismatch within the bounded local threat model.
10. Evidence packages bind ordered audit records, artefact digests and accepted release references without collecting hidden chain-of-thought.
11. Audit replay is read-only evidence reconstruction and cannot mutate `DATA-106`.
12. Status reports explicitly deny WORM, KMS/HSM, full control-plane, Stage 8D/9D and production-readiness claims.

## C. Accepted architecture decisions

`ADR-001`–`113` remain. New:

- `ADR-114`: execute S10A on the accepted S09C baseline while recording, not hiding, the unresolved S09D sequencing gap.
- `ADR-115`: separate sampled operational observability from complete accountability audit.
- `ADR-116`: use a provider-neutral canonical telemetry schema with OpenTelemetry adapters rather than binding core semantics to one backend.
- `ADR-117`: use W3C trace context for correlation only, never identity, tenancy or authority.
- `ADR-118`: capture metadata and digests by default; raw generative-AI content is opt-in, purpose-limited and separately governed.
- `ADR-119`: sample operational telemetry but never sample mandatory audit events.
- `ADR-120`: use a local SHA-256 hash chain with HMAC authenticity; defer WORM storage, trusted time and asymmetric KMS/HSM signing.
- `ADR-121`: require durable audit intent and outcome records around protected effects.
- `ADR-122`: retain `DATA-106` as the business source of truth; audit replay is read-only.
- `ADR-123`: build digest-bound evidence packages without hidden chain-of-thought.
- `ADR-124`: defer production observability-backend selection until S09D, S08D, residency, scale and retention requirements are resolved.

## D. Current component inventory

| ID | Name | Current Stage 10A responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Propagates bounded correlation and presents trace/evidence references without exposing secrets or treating audit as authority. |
| `CMP-002` | Regulatory Intake Boundary | Emits input/quarantine events with content digest, media type, size and guardrail references; no raw hostile text by default. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole route/protected-state/admission/cancellation/aggregation/termination owner; creates run/task spans and mandatory state/disposition audit events. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Emits permission-aware retrieval metadata, freshness, source references and result counts. |
| `CMP-005` | Enterprise Integration Boundary | Only tool gateway; emits tool intent/outcome, auth/BR references, idempotency and protected-effect audit. |
| `CMP-006` | Human Review and Approval Boundary | Emits digest-bound review requests and authenticated human decisions; timeout never approves. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Emits grant/policy decision evidence; remains sole authority issuer. |
| `CMP-008` | Evaluation and Assurance Boundary | Emits evaluation IDs, dataset/rubric versions and results; remains advisory. |
| `CMP-009` | Observability and Audit Boundary | Owns canonical telemetry, redaction, correlation, local export, audit ledger, verification and evidence packaging. |
| `CMP-010` | Runtime and Deployment Boundary | Emits runtime health, resource and deployment/config version telemetry; no production route. |
| `CMP-011` | Source-of-Truth Governance Pack | Owns telemetry/audit policy, retention owners, access model, ADRs, risk/issues and compatibility. |

## E. Current agent inventory

- `AGT-001 Regulatory Impact Assessment Agent`, spec `1.1.0`, remains the **only active agent**.
- It may emit telemetry and propose evidence, but cannot edit or suppress mandatory audit, issue/enlarge grants, change BR budgets/tiers, approve/finalize, mutate `DATA-106`, activate routes or create agents.
- No tracer, collector, exporter, auditor, ledger, verifier or evidence builder is an agent.
- `WP-008`, MCP/A2A peers and additional agents remain `inactive_future`.

## F. Current data and state objects

- Preserve `DATA-001`–`216`; `DATA-009` remains `1.1.0` and `DATA-106` remains the business source of truth.
- Add `DATA-217`–`236`: CorrelationContext, TelemetryEvent, TraceSpan, StructuredLogRecord, MetricPoint, ModelInvocationTelemetry, RetrievalTelemetry, ToolInvocationTelemetry, PolicyDecisionTelemetry, HumanApprovalTelemetry, StateTransitionTelemetry, RedactionResult, AuditEvent, AuditChainCheckpoint, AuditVerificationReport, EvidencePackageManifest, EvidencePackage, TelemetrySamplingPolicy, TelemetryRetentionPolicy and ObservabilityStatusReport.
- Every S10A schema requires `authority_effect: none`.
- Audit records may prove that an accepted owner made a decision; they do not make that decision.

## G. Current interfaces and tools

- Preserve `INT-001`–`176` and `TOOL-001`–`006`.
- Add `INT-177`–`196`: PropagateTraceContext, StartRunTrace, StartComponentSpan, RecordStructuredEvent, RecordMetric, RecordModelInvocation, RecordRetrieval, RecordToolInvocation, RecordPolicyDecision, RecordHumanApproval, RecordStateTransition, RedactTelemetry, AppendAuditEvent, VerifyAuditChain, CreateAuditCheckpoint, BuildEvidencePackage, VerifyEvidencePackage, QueryTrace, ExportTelemetryBatch and GetObservabilityStatus.
- No interface can issue authority, approve/finalize, invoke tools outside `CMP-005`, mutate `DATA-106` or activate a route.
- No `TOOL-007` is introduced.

## H. Repository state

```text
northstar-agentic-compliance-stage10a-observability-audit/
├── config/{audit,observability}/
├── docs/{adr,architecture/diagrams,references,source-of-truth,stages,threat-model}/
├── reports/
├── schemas/DATA-217..236.schema.json
├── scripts/
├── src/northstar_compliance/{audit,common,observability}/
├── tests/{unit,integration,security,performance}/
├── .env.example
├── README.md
└── pyproject.toml
```

Entry points: `run_stage10a_demo.py`, `run_stage10a_performance.py`, `validate_stage10a.py`, `run_stage10a_evaluation_gates.py`, `consistency_audit_stage10a.py`.

## I. Tests completed

- `TEST-881`–`892`: correlation and W3C trace-context parsing/propagation.
- `TEST-893`–`904`: redaction, hashing, secret and sensitive-field minimization.
- `TEST-905`–`918`: spans, events, metrics, sampling and cardinality controls.
- `TEST-919`–`936`: append-only ledger, sequence, hash, HMAC, idempotency and tamper detection.
- `TEST-937`–`946`: evidence-package construction, verification and no-hidden-reasoning rules.
- `TEST-947`–`954`: end-to-end service, protected intent/outcome, exporter and audit failure semantics.
- `TEST-955`–`958`: security invariants including authority separation and read-only replay.
- `TEST-959`–`960`: local throughput/verification guards.
- `EVAL-229`–`252`: passed through the evaluation wrapper.
- Executed locally: **80 pytest cases passed**; 20 schemas and two policies validated; demo, performance wrapper, evaluation gates, compilation and consistency audit passed.

## J. Known limitations

No byte-exact historical merge; no completed S09D enterprise control plane; no completed S08D metrics/regression/deployment gates; no production OpenTelemetry SDK/Collector/backend; no live model/tool/retrieval instrumentation; no WORM/object-lock storage; no asymmetric KMS/HSM signing; no trusted time-stamp authority; no multi-region ledger or disaster-recovery proof; no enterprise legal/records retention schedule; no production evidence-access workflow; no distributed idempotency ledger; no calibrated production sampling/cardinality/SLO baseline; no active MCP/A2A/multi-agent tracing; no legal admissibility, certification or production promotion.

## K. Open risks, assumptions and issues

- Preserve inherited active items.
- Add `RSK-402`–`431`, `ASM-127`–`134`, `ISS-170`–`181`.
- Highest residual concerns: sensitive telemetry leakage, omitted mandatory events, audit-storage outage, key compromise, tampering by a privileged administrator, exporter backlog, metric-cardinality attack, clock uncertainty, ambiguous protected-effect outcome, overbroad evidence packages and false confidence in a local HMAC chain.
- `ISS-170` records the deliberate S09D/S10A sequence divergence; `ISS-171` records that enterprise-control-plane instrumentation remains incomplete; `ISS-173`/`174` record missing WORM and KMS/HSM/trusted-time guarantees; `ISS-176` records absent multi-region proof; `ISS-180` records the compatible-overlay rather than byte-exact merge.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`, `DATA-009 1.1.0`, `AUTH-001/1.0.0`, `BR-001/1.0.0`, `GR-001/1.0.0`, `GOV-001/1.0.0` and bounded `CP-001/0.1.0`.
3. Preserve `DATA-001`–`236`, `INT-001`–`196`, `TOOL-001`–`006`.
4. `CMP-003` remains sole route/protected-state/admission/cancellation/aggregation/termination owner.
5. `CMP-005` remains only tool gateway; `CMP-007` remains sole authority issuer; `CMP-006`/humans own approval/finalization.
6. Correlation identifiers, telemetry, audit records, evidence packages and replay have `authority_effect: none`.
7. Trace headers/baggage cannot supply trusted identity, tenant, case, approval, grant or resource scope.
8. Operational telemetry may be sampled; mandatory audit events cannot be sampled or silently dropped.
9. A protected effect requires durable audit intent before effect and outcome/reconciliation after effect.
10. Audit append failure blocks protected effects; telemetry-export failure may degrade diagnostics but cannot be represented as audit success.
11. `DATA-106` remains the authoritative business-state record; audit replay is read-only.
12. Raw prompts/responses/documents/tool arguments remain off by default and require purpose, access, retention and redaction approval.
13. Human credentials/tokens remain restricted; timeout never approves.
14. Tier 4 has no tools; tier 5 cannot be autonomously granted; one concurrent protected write remains maximum.
15. `WP-008`, MCP/A2A and additional agents remain inactive.
16. Stage 8D and Stage 9D remain unresolved; production promotion stays denied.
17. Local HMAC hash chaining must not be described as WORM, asymmetric non-repudiation, trusted timestamping or legal admissibility.
18. Any production adapter must pass schema, redaction, sampling, event-completeness, hash/verification, outage and authority-separation conformance tests.
19. Resolve historical merge issues before claiming byte-exact completeness.

## M. Required input for the next stage

Use the merged `1.15.0` overlays; `ADR-001`–`124`; `GRAPH-001/1.11.0`; `TM-001/1.3.0`; `AUTH-001/1.0.0`; `BR-001/1.0.0`; `GR-001/1.0.0`; `GOV-001/1.0.0`; `CP-001/0.1.0`; `OBS-001/1.0.0`; `AUD-001/1.0.0`; `EVID-001/1.0.0`; `DATA-217`–`236`; `INT-177`–`196`; all S09 security/guardrail tests; all S10A event-completeness, tamper, failure and evidence-package tests; all active risks/issues; and explicit unresolved S08D/S09D.

## N. Next architectural problem

NorthStar can now correlate a run and construct a tamper-evident local evidence package, but it has not engineered system-wide recovery. Model, retrieval, queue, state, policy, authorization, tool, audit, human-review and infrastructure failures can still cascade or leave ambiguous outcomes. The architecture needs a failure taxonomy, retry/timeout/backoff rules, circuit breakers, bulkheads, dead-letter handling, checkpoint recovery, compensation, degraded modes, chaos tests, incident evidence and disaster-recovery boundaries—without allowing recovery logic to bypass accepted authority or audit requirements.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 10B — Reliability and Failure Engineering**. Reconstruct the `1.15.0` S10A baseline; preserve exactly one active `AGT-001`, `GRAPH-001/1.11.0`, `TM-001/1.3.0`, `AUTH-001/1.0.0`, `BR-001/1.0.0`, `GR-001/1.0.0`, `GOV-001/1.0.0`, bounded `CP-001/0.1.0`, `OBS-001/1.0.0`, `AUD-001/1.0.0`, all current authority owners, gateway-only tools, one concurrent protected write, read-only audit replay, unsampled mandatory audit events, inactive `WP-008`/MCP/A2A/multi-agent routes and unresolved Stages 8D/9D. Design failure detection, containment, recovery, compensation, checkpointing, dead-letter handling, circuit breakers, bulkheads, chaos tests and disaster-recovery boundaries; do not activate new agents, protocols, tools or production routes.
