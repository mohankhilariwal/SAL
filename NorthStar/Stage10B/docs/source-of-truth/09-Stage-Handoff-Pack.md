# Stage Handoff Pack

## A. Stage completed

- Stage identifier: `S10B`
- Stage title: Reliability, Deployment and AgentOps — bounded reliability and non-production reference implementation
- Architecture version: `1.16.0`
- Repository version: `1.16.0`
- Handoff version: `1.16.0`
- Graph version: `GRAPH-001/1.12.0`
- Threat-model version: `TM-001/1.4.0`
- Authorization model: `AUTH-001/1.0.0` unchanged
- Blast-radius model: `BR-001/1.0.0` unchanged
- Guardrail model: `GR-001/1.0.0` unchanged
- Governance model: `GOV-001/1.0.0` unchanged
- Control-plane profile: `CP-001/0.1.0` unchanged; Stage 9D remains unresolved
- Observability model: `OBS-001/1.0.0` unchanged
- Audit model: `AUD-001/1.0.0` unchanged
- Evidence-package model: `EVID-001/1.0.0` unchanged
- Reliability model: `REL-001/1.0.0`
- AgentOps profile: `OPS-001/0.1.0`
- Deployment profile: `DEP-001/0.1.0`
- Disaster-recovery profile: `DR-001/0.1.0`
- Completion date: 2026-08-01
- Status: completed as a provider-neutral reliability design, executable local reference and non-production deployment/AgentOps overlay. No production route, enterprise workflow engine, managed queue, approved fallback catalogue, production SLO, enterprise RTO/RPO, multi-region failover, production provenance verification, Stage 8D/9D resolution, certification or production-readiness claim.
- Consistency audit: passed with recorded historical-merge and environment exceptions.

## B. Capabilities now available

1. Deterministic failure classification by permanence, ambiguity, effect class, retryability and control domain.
2. Operation-specific retry with exponential backoff, full jitter, attempt limits and total-time budget.
3. Automatic retry is prohibited for authorization, policy, security, audit, data-integrity, configuration and permanent failures.
4. Writes require idempotency; ambiguous protected outcomes require reconciliation before repeat.
5. Per-dependency circuit breakers and bounded bulkheads contain cascades and overload.
6. Atomic digest-verified workflow checkpoints support resumption without mutating `DATA-106`.
7. Metadata-minimized dead-letter quarantine and authenticated manual redrive evidence.
8. Deterministic degraded modes: labelled read-only partial service where allowed; fail closed for authority, policy, audit and integrity boundaries.
9. Compensation is defined as a new controlled action through `CMP-005`, not rollback magic.
10. Local incident and chaos evidence preserves authority separation and audit-fail-closed invariants.
11. Release manifests bind architecture, graph, agent specification, source, configuration and test evidence.
12. Non-production promotion gates require tests and human approval; production promotion is denied.
13. Local Docker and illustrative pre-production Kubernetes artefacts include probes, resource bounds, non-root/read-only settings and a disruption budget.
14. No new agent, protocol, external tool or production route is activated.

## C. Accepted architecture decisions

Preserve `ADR-001`–`124`. Add `ADR-125`–`137` as recorded in the ADR register.

## D. Current component inventory

Preserve `CMP-001`–`011`. Stage 10B responsibilities are recorded in `04-Component-and-Agent-Catalogue.md`; no new top-level component is introduced.

## E. Current agent inventory

- `AGT-001 Regulatory Impact Assessment Agent`, specification `1.1.0`, remains the only active agent.
- Recovery, retry, circuit, checkpoint, DLQ, deployment, release and chaos modules are deterministic software, not agents.
- `WP-008`, MCP/A2A peers and additional agents remain `inactive_future`.

## F. Current data and state objects

- Preserve `DATA-001`–`236`.
- Add `DATA-237`–`256`: FailureEnvelope, FailureClassification, RetryPolicy, TimeoutPolicy, CircuitBreakerPolicy, BulkheadPolicy, DeadLetterRecord, WorkflowCheckpoint, RecoveryDecision, CompensationPlan, DegradedModeProfile, IncidentRecord, ChaosExperiment, ChaosResult, RecoveryStatusReport, ReleaseManifest, DeploymentEnvironmentProfile, PromotionDecision, RollbackPlan and RuntimeSLO.
- Every new schema requires `authority_effect: none`.

## G. Current interfaces and tools

- Preserve `INT-001`–`196` and `TOOL-001`–`006`.
- Add `INT-197`–`216`: ClassifyFailure, ExecuteWithRetry, EnforceDeadline, EvaluateCircuit, AcquireBulkheadPermit, PersistWorkflowCheckpoint, LoadWorkflowCheckpoint, QuarantineDeadLetter, AuthorizeDeadLetterRedrive, ReconcileProtectedOutcome, PlanCompensation, EnterDegradedMode, ExitDegradedMode, RecordIncident, RunChaosExperiment, BuildReleaseManifest, EvaluatePromotion, PrepareDeploymentPlan, VerifyRollbackPlan and GetReliabilityStatus.
- No `TOOL-007` is introduced.
- None of the new interfaces may issue authority, approve/finalize, invoke tools outside `CMP-005`, mutate `DATA-106` or activate a production route.

## H. Repository state

```text
northstar-agentic-compliance-stage10b-reliability-agentops/
├── .github/workflows/stage10b.yml
├── config/{agentops,deployment,reliability}/
├── deployment/{docker,kubernetes}/
├── docs/{adr,architecture/diagrams,references,runbooks,source-of-truth,stages}/
├── reports/
├── schemas/DATA-237..256.schema.json
├── scripts/
├── src/northstar_compliance/{agentops,audit,common,deployment,integration,orchestration,reliability}/
├── tests/{chaos,integration,performance,security,unit}/
├── .env.example
├── README.md
└── pyproject.toml
```

Entry points: `run_stage10b_demo.py`, `run_stage10b_chaos.py`, `validate_stage10b.py`, `run_stage10b_evaluation_gates.py`, `consistency_audit_stage10b.py`.

## I. Tests completed

- `TEST-961`–`973`: retry success, exhaustion, prohibited failure classes, idempotency and ambiguous-outcome safety.
- `TEST-974`–`980`: circuit-breaker and bulkhead state/limit behavior.
- `TEST-981`–`991`: recovery decision table and fail-closed rules.
- `TEST-992`–`998`: checkpoint integrity and dead-letter minimization/redrive controls.
- `TEST-999`–`1009`: protected-effect intent/outcome, idempotency, reconciliation and release/deployment gates.
- `TEST-1010`–`1013`: authority, tool and route invariants.
- `TEST-1014`–`1015`: local chaos behavior.
- `TEST-1016`: deterministic local recovery performance guard.
- `EVAL-253`–`260`: retry safety, reconciliation, audit fail-closed, authority separation, checkpoint integrity, DLQ control, production denial and chaos invariant.
- Executed locally: **56 pytest cases passed**; **20 schemas and five configuration files validated**; demo, chaos wrapper, evaluation gates and compilation passed.

## J. Known limitations

No byte-exact historical merge; no full Stage 10A repository merge; no distributed workflow engine; no durable enterprise checkpoint database; no managed queue/DLQ; no approved fallback model/tool; no live dependency adapters; no calibrated production retry/circuit/bulkhead values; no production SLO/error budget; no control-plane implementation; no deployment evaluation eligibility; no production route; no canary controller; no production registry/signing/provenance verification; no enterprise backup platform; no approved RTO/RPO; no multi-region failover; no WORM/KMS/HSM/trusted-time upgrade; no production incident-management integration; no FinOps model; no certification or production-readiness claim.

## K. Open risks, assumptions and issues

Preserve inherited items. Add `RSK-432`–`461`, `ASM-135`–`142`, and `ISS-182`–`193` as recorded in the risk register.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001/1.1.0`, `DATA-009/1.1.0`, `AUTH-001/1.0.0`, `BR-001/1.0.0`, `GR-001/1.0.0`, `GOV-001/1.0.0`, bounded `CP-001/0.1.0`, `OBS-001/1.0.0`, `AUD-001/1.0.0` and `EVID-001/1.0.0`.
3. Preserve `DATA-001`–`256`, `INT-001`–`216`, `TOOL-001`–`006`.
4. `CMP-003` remains sole route/protected-state/admission/cancellation/aggregation/termination/recovery owner.
5. `CMP-005` remains only tool, reconciliation and compensation gateway; `CMP-007` remains sole authority issuer; `CMP-006`/humans own approval/finalization.
6. Reliability, checkpoints, dead letters, incidents, release manifests and promotion decisions have `authority_effect: none`.
7. Do not retry authorization, policy, audit, security, integrity, configuration or permanent failures automatically.
8. Do not retry an ambiguous protected outcome until `CMP-005` reconciles the idempotency reference.
9. Protected writes require durable audit intent before effect and outcome/reconciliation after effect.
10. Audit failure blocks protected effects; telemetry failure does not equal audit success.
11. Checkpoint load and audit replay remain read-only with respect to `DATA-106`.
12. Human approval timeout remains pending and escalated; timeout never approves.
13. One concurrent protected write remains the maximum.
14. Tier 4 has no tools; tier 5 cannot be autonomously granted.
15. `WP-008`, MCP/A2A and additional agents remain inactive.
16. S08D and S09D remain unresolved; production promotion and route activation stay denied.
17. Local deployment and HMAC audit controls must not be described as enterprise production, WORM, legal admissibility, trusted time, multi-region DR or certification.
18. Fallbacks must be separately approved for quality, security, residency, cost and evaluation before activation.
19. Rollback of code/config does not reverse completed external effects; compensation is a separate controlled action.
20. Resolve historical merge issues before claiming byte-exact completeness.

## M. Required input for the next stage

Use the merged `1.16.0` overlays; `ADR-001`–`137`; `GRAPH-001/1.12.0`; `TM-001/1.4.0`; `REL-001/1.0.0`; `OPS-001/0.1.0`; `DEP-001/0.1.0`; `DR-001/0.1.0`; `DATA-237`–`256`; `INT-197`–`216`; all S09/S10A controls; all Stage 10B tests/evaluations; all active risks/issues; and explicit unresolved S08D/S09D.

## N. Next architectural problem

NorthStar can now contain and recover from bounded failures in a local/non-production reference, but it cannot make an economically or operationally justified production decision. Capacity targets, production SLOs and error budgets, workload-specific cost models, human-review cost, observability/evaluation cost, regional deployment economics, retention costs and approved RTO/RPO remain undefined. Production promotion also remains blocked by unresolved S08D and S09D.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 10C — FinOps, Capacity and Production Readiness**. Reconstruct the `1.16.0` Stage 10B baseline; preserve exactly one active `AGT-001`, all accepted authority owners, gateway-only tools, one concurrent protected write, audit-fail-closed protected effects, read-only checkpoint/audit replay, inactive `WP-008`/MCP/A2A/multi-agent routes and denied production promotion. Define workload-based capacity, SLO/error-budget proposals, full cost formulas, cost controls, RTO/RPO decision ownership and production-readiness evidence without activating a production route or claiming unresolved S08D/S09D controls are complete.
