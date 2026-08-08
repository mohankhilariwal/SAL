# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S03C`
- **Stage title:** Loop Failures, Recovery and Budgets
- **Architecture version:** `0.7.0`
- **Repository version:** `0.7.0`
- **Handoff version:** `0.7.0`
- **Completion date:** 2026-07-31
- **Status:** Completed within the local/offline synthetic verification boundary.
- **Consistency audit:** Passed with recorded exceptions `ISS-014`, `ISS-015`, `ISS-021`–`ISS-031` and inherited production gaps.

## B. Capabilities now available

1. All S03B one-agent, gateway-only, deterministic-completion and unapproved/human-review capabilities remain.
2. `DATA-045 RuntimeBudget` and `DATA-046 BudgetLedger` enforce independent iteration, wall-time, input/output/total token, synthetic CAD cost, tool-call, model-call, failure, retry and replan limits.
3. `DATA-047 FailureEnvelope` and `INT-027` classify failures by kind, execution stage, retryability and known commit state.
4. Bounded provider fallback preserves `INT-022` and agent authority.
5. Read-only `TOOL-001`–`TOOL-003` may use one configured fallback adapter; write-tool fallback is prohibited.
6. Reversible writes may retry only after definite pre-dispatch non-commit with the same idempotency key.
7. Ambiguous write failures use `INT-030` reconciliation by tool and idempotency key; unresolved status escalates without blind retry.
8. Repetition/no-progress can trigger finite replanning with blocked canonical action signatures.
9. `INT-028` cooperative cancellation stops new work and returns a non-success partial outcome.
10. `INT-029` persists checksummed atomic local checkpoints and resumes the same run from missing milestones.
11. `DATA-052` records partial/terminal milestones, artifacts, budget ledger and concise recovery evidence.
12. Compensation boundaries are defined; autonomous compensation execution is not implemented.
13. Twenty-two S03C tests and five evaluations passed locally.

Not implemented: graph/workflow engine, durable distributed execution, event sourcing, concurrent branches, memory, multiple agents, live model/connectors, enterprise identity/PDP, actual human review, accepted mapping/case, production telemetry/audit/records, compensation execution, production concurrency/deployment/DR.

## C. Accepted architecture decisions

`ADR-001`–`ADR-023` remain accepted.

- `ADR-024`: application-owned independent budgets and monotonic usage ledger.
- `ADR-025`: typed failure recovery combining failure class and operation impact; bounded model/read fallback; no blind ambiguous-write retry.
- `ADR-026`: atomic checksummed local checkpoint/resume without claiming graph, event sourcing, audit or distributed durable execution.

## D. Current component inventory

| ID | Name | Current responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Local run/cancel/resume caller and partial-outcome viewer. |
| `CMP-002` | Regulatory Intake Boundary | Retained. |
| `CMP-003` | Case and Workflow Orchestration Boundary | One-agent runtime with budgets, recovery, cancellation, checkpoint and deterministic termination. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Retained synthetic authorized evidence. |
| `CMP-005` | Enterprise Integration Boundary | Gateway, registered read fallback and write reconciliation. |
| `CMP-006` | Human Review and Approval Boundary | Local queued request only; no decision service. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Partial unauthenticated local principal/write-scope enforcement. |
| `CMP-008` | Evaluation and Assurance Boundary | Budget/recovery/cancellation/resume tests and evaluations. |
| `CMP-009` | Observability and Audit Boundary | Local checkpoints/outcomes only; not audit. |
| `CMP-010` | Runtime and Deployment Boundary | Python 3.13.5 single-process local runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented at `0.7.0`. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose one of `TOOL-001`–`006`, complete or escalate. Cannot set budgets/retries/fallbacks/reconciliation, approve/finalize, compensate, delegate, create agents, execute code or handle unrestricted credentials. | Implemented and locally verified. |

## F. Current data and state objects

- `DATA-001`–`DATA-044` retained.
- `DATA-009 AgentRunState` schema `1.1.0` adds budget/recovery/checkpoint fields compatibly.
- New: `DATA-045 RuntimeBudget`, `DATA-046 BudgetLedger`, `DATA-047 FailureEnvelope`, `DATA-048 RecoveryRecord`, `DATA-049 CancellationSignal`, `DATA-050 RunCheckpoint`, `DATA-051 ReconciliationRecord`, `DATA-052 RecoveryOutcome`.
- No enterprise `DATA-002 RegulatoryCase` or `DATA-007 ReviewDecision` is instantiated. Local drafts/mappings/review requests remain reversible unapproved artifacts.

## G. Current interfaces and tools

- `INT-001`–`INT-025` retained.
- `INT-026` Budget Enforcement Contract.
- `INT-027` Failure Classification and Recovery Contract.
- `INT-028` Cancellation Contract.
- `INT-029` Checkpoint and Resume Contract.
- `INT-030` Ambiguous Write Reconciliation Contract.
- `TOOL-001`–`003` read-only; `TOOL-004`–`006` reversible unapproved writes.
- Every action continues through `INT-017`/`CMP-005`; provider/fallback schemas are adapters, not authority.

## H. Repository state

Repository `northstar-agentic-compliance` version `0.7.0`. Important entry points:

```text
src/northstar_compliance/agent/{models,budgets,cancellation,decision,recovery,termination,runtime,factory}.py
src/northstar_compliance/tools/{gateway,local_tools}.py
src/northstar_compliance/state/checkpoint.py
config/runtime/stage3c-budget.json
schemas/DATA-045...DATA-052*.schema.json
scripts/run_stage3c_demo.py
scripts/run_stage3c_evaluation.py
scripts/validate_stage3c.py
scripts/consistency_audit_stage3c.py
tests/{unit,integration,security,evaluation}/
docs/stages/Stage-3C-Loop-Failures-Recovery-and-Budgets.md
```

## I. Tests completed

- `TEST-088`–`090`: token, cost and tool-call budgets — passed.
- `TEST-091`–`092`: checkpoint round trip and tamper detection — passed.
- `TEST-093`: happy path/unapproved semantics — passed.
- `TEST-094`: transient read fallback — passed.
- `TEST-095`: ambiguous write reconciliation/no duplicate — passed.
- `TEST-096`: model fallback — passed.
- `TEST-097`–`098`: partial outcome and failure budget — passed.
- `TEST-099`: checkpoint resume without repeated completed work — passed.
- `TEST-100`: external cancellation — passed.
- `TEST-101`: bounded dead-end replan — passed.
- `TEST-102`–`105`: authority, allowlist, evidence and write-scope boundaries — passed.
- `TEST-106`: recovery/efficiency metrics — passed.
- `TEST-107`: exactly one agent/no future-stage modules — passed.
- `TEST-108`–`109`: wall-time and retry budgets — passed.

Executed result: **22 tests passed**. Compilation, demo, evaluation, structural validator and consistency audit passed.

Evaluations:

| ID | Result |
|---|---|
| `EVAL-022` | Normal run completed. |
| `EVAL-023` | Transient primary read used fallback and completed. |
| `EVAL-024` | Draft timeout after commit reconciled one artifact and completed. |
| `EVAL-025` | Primary provider timeout used secondary provider and completed. |
| `EVAL-026` | Tool-call budget stopped with exact reason and partial milestones. |

## J. Known limitations

1. Deterministic/scripted decision providers and synthetic token usage only.
2. Synthetic/local tools and status stores only.
3. Synthetic CAD tariff; no live provider billing.
4. No worst-case in-flight budget reservation.
5. No real backoff/jitter, circuit breaker or shared retry quota in local tests.
6. Cooperative cancellation only.
7. Local current-state checkpoint, not event sourcing/audit/distributed workflow/DR.
8. No multi-process lease or concurrent resume.
9. Reconciliation not live-connector verified.
10. Compensation execution absent.
11. Unsigned local identity/policy/checkpoint evidence.
12. No production latency/concurrency/throughput/failure/cost benchmark.
13. Mermaid not rendered by CLI.
14. Compatible overlay rather than byte-exact `0.6.0` continuation (`ISS-029`).

## K. Open risks, assumptions and issues

- New risks: `RSK-057`–`RSK-066`.
- New assumptions: `ASM-022`–`ASM-024`.
- New issues: `ISS-029`–`ISS-031`.
- Inherited active risks/issues remain.

## L. Compatibility constraints

1. Preserve NorthStar, all eight personas, `US-001`–`US-012`, `CMP-001`–`CMP-011` and accepted meanings.
2. Preserve S01/S02 unapproved/human-accountability and authorization-before-context semantics.
3. Preserve S03A `TOOL-001`–`006`, gateway-only execution, impact classes and idempotency.
4. Preserve `AGT-001` as the only agent and its low authority.
5. Preserve `DATA-009` `1.1.0`, `DATA-041`–`052`, `INT-021`–`030` ownership and semantics.
6. Budgets, failure classification, fallback selection, retry safety, reconciliation, completion and final disposition remain application-owned.
7. Never blindly retry an ambiguous write; reconcile by the same idempotency key or escalate.
8. Partial/guard/cancel outcomes remain `preliminary_grounded_unapproved` and require human review.
9. Checkpoints are not memory, audit, event sourcing or exactly-once guarantees.
10. The next stage may introduce a graph but must preserve S03C budget/recovery contracts and must not add multiple agents or memory unless separately justified.

## M. Required input for the next stage

Reconstruct all ten `0.7.0` artefacts, `ADR-001`–`026`, `DATA-009` `1.1.0`, `DATA-019`–`052`, `INT-009`–`030`, `TOOL-001`–`006`, `AGT-001`, cumulative/focused diagrams, S03C code/tests/evaluations, S01 disposition invariants, S02 permission boundary, S03A gateway invariants and active risks/issues.

## N. Next architectural problem

Budget and recovery logic now works, but the imperative loop contains increasingly complex branches for deterministic prerequisites, model decisions, tool calls, recovery, waiting and termination. NorthStar needs an explicit typed execution graph so node/edge ownership, error routes, checkpoints and future human approval can be reviewed and tested independently. The graph must reuse S03C budgets/recovery rather than replacing them.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 4A — Graph Foundations and Typed Execution State**. Reconstruct the `0.7.0` baseline; preserve `AGT-001`, `TOOL-001`–`TOOL-006`, gateway-only authority, `DATA-045`–`052`, `INT-026`–`030`, deterministic completion, unapproved/human-review semantics and no blind ambiguous-write retry. Convert the increasingly branched single loop into an explicit typed graph with deterministic/model/tool/policy/recovery nodes and conditional/error/termination edges, while stopping before harness, memory or multi-agent engineering. Update all artefacts, tests and handoff, perform the consistency audit and stop after this stage.
