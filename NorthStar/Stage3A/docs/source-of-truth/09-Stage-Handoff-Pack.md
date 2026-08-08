# 09 — Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S03A`
- **Stage title:** Tool Contracts and Tool Gateway
- **Architecture version:** `0.5.0`
- **Repository version:** `0.5.0`
- **Handoff version:** `0.5.0`
- **Completion date:** 2026-07-31
- **Status:** Completed within the local/offline synthetic verification boundary
- **Consistency audit:** Passed with recorded exceptions `ISS-014`, `ISS-015`, `ISS-021`–`ISS-024` and inherited production gaps.

## B. Capabilities now available

1. Six versioned, hashed `TOOL-*` descriptors with strict input/output JSON schemas.
2. Exact tool/version resolution and allowlisted registration.
3. Deterministic gateway ordering: validation, idempotency, policy, runtime controls, adapter, output validation, evidence.
4. Read-only and reversible-write impact classification; high-impact tools rejected.
5. Mandatory idempotency, conflict detection and dry-run for reversible writes.
6. Bounded read-only retry, timeout, rate limit, circuit breaker and result-size enforcement.
7. Typed result/error envelopes with authorization decision references.
8. Redacted, hashed local tool execution events.
9. Local adapters for regulatory catalogue, control catalogue and authorized S02B evidence.
10. Local draft case, candidate mapping and human-review queue artefacts that preserve unapproved status.
11. Tool-contract, security, reliability and permission-boundary tests/evaluations.
12. Updated architecture, repository, four ADRs and all ten source-of-truth artefacts.

Not implemented: model-selected action, `AGT-*`, `DATA-009 AgentRunState`, bounded agent loop/termination, graph, durable state, enterprise IAM/PDP, live connectors, actual human review, external notification, accepted case/mapping, MCP/A2A, production observability/audit/records or multi-agent behavior.

## C. Accepted architecture decisions

`ADR-001`–`ADR-017` remain accepted. New decisions: `ADR-018` canonical application-owned JSON Schema tool contracts; `ADR-019` one application-owned gateway; `ADR-020` impact/idempotency/retry policy; `ADR-021` defer MCP and agent selection.

## D. Current component inventory

| ID | Name | Current status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Partial local caller. |
| `CMP-002` | Regulatory Intake Boundary | Retained S01. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Partial deterministic sequence; no loop/state. |
| `CMP-004` | Knowledge and Evidence Access Boundary | S02B capability retained and wrapped by `TOOL-003`. |
| `CMP-005` | Enterprise Integration Boundary | Partial tool gateway and local adapters. |
| `CMP-006` | Human Review and Approval Boundary | Planned; local queued request only. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Planned enterprise service; local PDP partial. |
| `CMP-008` | Evaluation and Assurance Boundary | Partial through tool/gateway evaluation. |
| `CMP-009` | Observability and Audit Boundary | Partial local events/reports; not audit. |
| `CMP-010` | Runtime and Deployment Boundary | Partial local Python runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented at `0.5.0`. |

## E. Current agent inventory

None. No `AGT-*` identifier exists. The gateway is not an agent and the demo call order is deterministic application code.

## F. Current data and state objects

`DATA-001`–`DATA-033` remain accepted. S03A adds `DATA-034 ToolPrincipalContext`, `DATA-035 ToolDescriptor`, `DATA-036 ToolInvocationRequest`, `DATA-037 ToolAuthorizationDecision`, `DATA-038 ToolResultEnvelope`, `DATA-039 ToolIdempotencyRecord` and `DATA-040 ToolExecutionEvent`. No accepted enterprise `DATA-002`, `DATA-007`, `DATA-009` or `DATA-010` is instantiated.

## G. Current interfaces and tools

- `INT-001`–`INT-015` retained.
- `INT-016` Tool Registry and Discovery Contract.
- `INT-017` Tool Invocation Contract.
- `INT-018` Tool Policy Decision Contract.
- `INT-019` Tool Adapter Contract.
- `INT-020` Tool Execution Evidence Contract.
- `TOOL-001`–`TOOL-003` read-only; `TOOL-004`–`TOOL-006` reversible local writes.

Every tool invocation requires gateway enforcement. No adapter is an authorized model endpoint.

## H. Repository state

Repository `northstar-agentic-compliance` version `0.5.0`. Primary entry points are `src/northstar_compliance/tools/gateway.py`, `factory.py`, descriptor files under `config/tools/`, Stage 3A scripts/tests, the current chapter and source-of-truth pack. The full tree is in `07-Repository-Manifest.md` and the packaged ZIP.

## I. Tests completed

- Accepted S02B `TEST-033`–`TEST-046` and `EVAL-009`–`EVAL-013` remain inherited evidence.
- `TEST-047`–`TEST-051`: descriptor/schema/version/impact/hash controls — passed.
- `TEST-052`–`TEST-056`: typed reads, reversible write chain, dry-run and idempotency — passed.
- `TEST-057`–`TEST-062`: pre-adapter validation/authorization, retrieval permission boundary, redaction and unauthenticated-claims warning — passed.
- `TEST-063`–`TEST-069`: bounded retry, no write retry, timeout, output validation, size, rate and circuit — passed.
- `TEST-070`–`TEST-073`: contract, draft, permission and no-agent evaluation invariants — passed.
- `EVAL-014`: 6/6 registered descriptors valid and hashed.
- `EVAL-015`: unapproved draft flow and idempotent replay successful.
- `EVAL-016`: Maya restricted hits `0`; Sofia authorized hits `1`.
- `EVAL-017`: one physical case write for duplicate key; no irreversible tool or `AGT-*`.

The validation report records the executed Python/pytest results, demo, benchmark and audit.

## J. Known limitations

1. Local synthetic catalogues and filesystem writes only.
2. Principal claims are not authenticated and policy decisions are unsigned.
3. Idempotency and circuit/rate state are process-local.
4. Thread timeout cannot guarantee cancellation of arbitrary blocking code or remote side effects.
5. No transactional outbox, compensation or reconciliation for ambiguous writes.
6. Tool descriptions are change-controlled files but not signed.
7. No live OpenAPI/function-calling/MCP adapter or conformance test.
8. Events are not tamper-evident, immutable or enterprise retained.
9. No production load, concurrency or tail-latency benchmark.
10. No model action selection, progress measurement, iteration budget or termination.

## K. Open risks, assumptions and issues

Active new items: `RSK-040`–`RSK-048`, `ASM-016`–`ASM-019`, `ISS-021`–`ISS-024`, plus inherited active S02B items.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`US-012`, `CMP-001`–`CMP-011` and all accepted meanings.
2. Preserve S01 preliminary/unapproved/human-review semantics and exact evidence behavior.
3. Preserve S02A/S02B `KSV-*`, `CHK-*`, `CIT-*`, authorization-before-scoring and `DATA-032` access boundary.
4. Preserve `DATA-034`–`DATA-040` and `INT-016`–`INT-020` semantics.
5. Every later agent/tool call must traverse the gateway or a conforming enforcement implementation.
6. Do not add a high-impact tool without a new ADR, approval policy, threat analysis and tests.
7. Writes remain idempotent; automatic write retry remains prohibited unless durable exactly-defined semantics supersede `ADR-020`.
8. Provider/MCP schemas are adapters, not the canonical source of authority.
9. Do not treat local drafts/events as enterprise case, review, record or audit objects.
10. Do not introduce graph, memory or multi-agent behavior in the next substage.

## M. Required input for the next stage

Reconstruct all ten `0.5.0` artefacts, `ADR-001`–`ADR-021`, `DATA-019`–`DATA-040`, `INT-009`–`INT-020`, `TOOL-001`–`TOOL-006`, cumulative diagrams, source descriptors, tests/evaluation reports, S01 disposition invariants, S02B permission boundary and active risks/issues.

## N. Next architectural problem

A deterministic caller can invoke each capability, but NorthStar still cannot receive a goal, inspect run progress, choose the next allowed tool, observe the result, update explicit run state, stop when complete or escalate when progress fails. Adding more gateway logic would mix capability enforcement with probabilistic action selection. The next substage must add exactly one bounded, low-authority agent loop over the existing gateway without weakening any gateway invariant.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 3B — Bounded Single-Agent Loop, Run State and Safe Termination**. Reconstruct the `0.5.0` baseline, preserve `TOOL-001`–`TOOL-006` and gateway enforcement, allocate at most one justified `AGT-*`, implement explicit typed run state, bounded observation-action iteration, progress and repetition checks, completion/escalation/termination, update all artefacts, run the consistency audit and stop after the S03B handoff.
