# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S03B`
- **Stage title:** Single-Agent Loop and Termination
- **Architecture version:** `0.6.0`
- **Repository version:** `0.6.0`
- **Handoff version:** `0.6.0`
- **Completion date:** 2026-07-31
- **Status:** Completed within the local/offline synthetic verification boundary.
- **Consistency audit:** Passed with recorded exceptions `ISS-014`, `ISS-015`, `ISS-021`–`ISS-028` and inherited production gaps.

## B. Capabilities now available

1. Exactly one accepted agent: `AGT-001 Regulatory Impact Assessment Agent`.
2. Typed `DATA-041 AgentGoal`, executable `DATA-009 AgentRunState`, structured `DATA-042 AgentDecision`, application-owned `DATA-043 AgentObservation` and `DATA-044 AgentRunOutcome`.
3. One application-owned observation-action loop with exactly one `call_tool`, `complete` or `escalate` proposal per iteration.
4. Provider-neutral `INT-022` decision contract with a deterministic local rule provider used as the accepted test oracle.
5. Agent-level allowlist limited to `TOOL-001`–`TOOL-006`; all calls continue through the S03A `CMP-005` gateway.
6. Trusted principal/write scope injected outside model reasoning; agent arguments cannot create authority.
7. Monotonic progress milestones derived only from validated `DATA-038` gateway results.
8. Deterministic completion invariants requiring regulatory source, authorized evidence, control candidates, `draft_unapproved` case, `candidate_unapproved` mapping and queued human review.
9. Explicit terminal states: `completed`, `escalated`, `terminated_guard`.
10. Explicit termination reasons for goal completion, human escalation, invalid completion/decision, tool failure, iteration limit, repeated action and no progress.
11. Finite iteration, repeated-action and no-progress guards.
12. Atomic local final run state/outcome evidence with fixed `preliminary_grounded_unapproved` disposition.
13. Fourteen S03B tests covering schemas, state, happy path, termination accuracy, authority, permission preservation and scope boundary.
14. Four S03B evaluations and updated cumulative architecture, repository, ADRs and all ten source-of-truth artefacts.

Not implemented: time/token/cost/tool-call/failure budgets; sophisticated retry/fallback; ambiguous-write reconciliation; external cancellation; checkpoint/resume; compensation; graph; memory; multi-agent; enterprise identity/PDP; live connectors; actual human review; accepted case/mapping; MCP/A2A; production telemetry/audit/records; production concurrency or deployment.

## C. Accepted architecture decisions

`ADR-001`–`ADR-021` remain accepted. New decisions:

- `ADR-022`: use one application-owned bounded single-agent loop with a provider-neutral structured decision contract; defer graph/framework and multiple agents.
- `ADR-023`: instantiate explicit run state and use layered deterministic completion, escalation and guard termination.

## D. Current component inventory

| ID | Name | Current status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Partial local goal caller/outcome viewer. |
| `CMP-002` | Regulatory Intake Boundary | Retained S01. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Partial bounded single-agent runtime; no graph/durable state. |
| `CMP-004` | Knowledge and Evidence Access Boundary | S02B capability retained through `TOOL-003`. |
| `CMP-005` | Enterprise Integration Boundary | S03A gateway/registry/policy/adapters retained; all agent calls enforced here. |
| `CMP-006` | Human Review and Approval Boundary | Planned service; local queued request only. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Planned enterprise service; local unauthenticated PDP remains partial. |
| `CMP-008` | Evaluation and Assurance Boundary | Extended with loop, termination and authority evaluation. |
| `CMP-009` | Observability and Audit Boundary | Final local run/tool evidence; not audit. |
| `CMP-010` | Runtime and Deployment Boundary | Local single-process Python runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented at `0.6.0`. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose only `TOOL-001`–`TOOL-006`; may create only gateway-authorized idempotent reversible unapproved local artifacts. Cannot approve, finalize, alter controls, assign remediation, notify externally, delegate, create agents, execute code or handle unrestricted credentials. | Implemented and locally verified. |

## F. Current data and state objects

- `DATA-001`–`DATA-040` remain accepted.
- `DATA-009 AgentRunState` is now executable at schema `1.0.0`.
- `DATA-041 AgentGoal` — immutable goal envelope; owner `CMP-003`.
- `DATA-042 AgentDecision` — one structured decision; owner/proposer `AGT-001`, validated by `CMP-003`.
- `DATA-043 AgentObservation` — application projection of a validated tool result; owner `CMP-003`.
- `DATA-044 AgentRunOutcome` — typed terminal evidence and fixed unapproved disposition; owner `CMP-003`/`CMP-009`.

No `DATA-007 ReviewDecision` or enterprise `DATA-002 RegulatoryCase` is instantiated. Local draft objects remain tool-specific reversible artifacts.

## G. Current interfaces and tools

- `INT-001`–`INT-020` retained.
- `INT-021` Agent Run Contract.
- `INT-022` Structured Decision Provider Contract.
- `INT-023` State Projection and Observation Contract.
- `INT-024` Termination Evaluation Contract.
- `INT-025` Agent Run Evidence Contract.
- `TOOL-001`–`TOOL-003` remain read-only; `TOOL-004`–`TOOL-006` remain reversible writes.

Every agent action must use `INT-017`. Provider/framework schemas remain adapters, not authority.

## H. Repository state

Repository `northstar-agentic-compliance` version `0.6.0`. Important entry points:

```text
src/northstar_compliance/agent/models.py
src/northstar_compliance/agent/decision.py
src/northstar_compliance/agent/termination.py
src/northstar_compliance/agent/runtime.py
src/northstar_compliance/agent/factory.py
src/northstar_compliance/tools/gateway.py
config/tools/TOOL-001.json ... TOOL-006.json
scripts/run_stage3b_demo.py
scripts/run_stage3b_evaluation.py
scripts/validate_stage3b.py
scripts/consistency_audit_stage3b.py
tests/unit/
tests/integration/
tests/security/
tests/evaluation/
docs/stages/Stage-3B-Single-Agent-Loop-and-Termination.md
```

The complete tree and compatibility notes are in `07-Repository-Manifest.md` and the packaged ZIP.

## I. Tests completed

Inherited S03A evidence `TEST-047`–`TEST-073` and `EVAL-014`–`EVAL-017` remains the supplied baseline. Executed S03B tests:

- `TEST-074`–`TEST-075`: decision schema fail-closed behavior — passed.
- `TEST-076`–`TEST-077`: iteration guard and completion invariant — passed.
- `TEST-078`: complete six-tool path and local final-state persistence — passed.
- `TEST-079`: premature completion escalates — passed.
- `TEST-080`: iteration exhaustion terminates with partial unapproved outcome — passed.
- `TEST-081`: repeated action terminates — passed.
- `TEST-082`: explicit escalation returns control — passed.
- `TEST-083`: non-allowlisted tool is not invoked — passed.
- `TEST-084`: model argument cannot grant write scope — passed.
- `TEST-085`: restricted Borealis evidence absent for Maya — passed.
- `TEST-086`: happy-path termination accuracy and loop efficiency — passed.
- `TEST-087`: exactly one agent; no graph/memory/multi-agent modules — passed.

Executed result: **14 tests passed**. Demo, evaluation script, compilation, structural validator and consistency audit passed.

Synthetic evaluation results:

| ID | Result |
|---|---|
| `EVAL-018` | Happy path completed after 7 decisions, 6 tool observations and 6 required milestones. |
| `EVAL-019` | Early completion → `invalid_completion`; explicit escalation → `human_escalation`; iteration guard → `iteration_limit`. |
| `EVAL-020` | Privileged/non-allowlisted tool invocations `0`; unauthorized write artifacts `0`. |
| `EVAL-021` | Maya restricted hits `0`; agent count `1`; graph/memory modules `0`. |

These results prove local control behavior, not managed-model regulatory reasoning quality or production reliability.

## J. Known limitations

1. The decision provider is deterministic; no managed model action-selection quality is measured.
2. Iteration is bounded, but time, tokens, cost, tool calls and failures are not separate run budgets.
3. Any failed/denied tool call immediately escalates; no bounded replan, fallback or dead-end recovery is implemented.
4. No cancellation propagation, ambiguous-write reconciliation, compensation or partial retry strategy.
5. State is in memory until final write; process death loses in-flight progress.
6. Final files/events are not signed, hash-chained, WORM or enterprise retained.
7. Synthetic catalogues, evidence and local writes only.
8. Principal claims and policy decisions are unauthenticated/unsigned.
9. No production load, concurrency, tail-latency or cost benchmark.
10. No graph, human approval processing, memory, MCP/A2A or multi-agent behavior.

## K. Open risks, assumptions and issues

- New active risks: `RSK-049`–`RSK-056`.
- New assumptions: `ASM-020`–`ASM-021`.
- New issues: `ISS-025`–`ISS-028`.
- Inherited active S03A risks/issues remain.

## L. Compatibility constraints

1. Preserve NorthStar, all eight personas, `US-001`–`US-012`, `CMP-001`–`CMP-011` and accepted meanings.
2. Preserve S01 preliminary/unapproved and human-accountability semantics.
3. Preserve S02A/S02B `KSV-*`, `CHK-*`, `CIT-*`, `DATA-032` and authorization-before-scoring/text exposure.
4. Preserve S03A `DATA-034`–`DATA-040`, `INT-016`–`INT-020`, `TOOL-001`–`TOOL-006`, impact/idempotency/retry rules and gateway-only execution.
5. Preserve `AGT-001` as the only agent and its low-authority non-goals.
6. Preserve `DATA-009`, `DATA-041`–`DATA-044` and `INT-021`–`INT-025` schemas/ownership.
7. A `complete` proposal never bypasses `INT-024` completion invariants.
8. Writes remain idempotent and receive no automatic write retry unless a new ADR defines reconciliation.
9. Do not treat local artifacts as enterprise cases, accepted mappings, review decisions, records or audit events.
10. S03C may add loop budgets/recovery but must not introduce graph, memory or multiple agents.

## M. Required input for the next stage

Reconstruct all ten `0.6.0` artefacts, `ADR-001`–`ADR-023`, `DATA-009`, `DATA-019`–`DATA-044`, `INT-009`–`INT-025`, `TOOL-001`–`TOOL-006`, `AGT-001`, cumulative/focused diagrams, S03B code/tests/evaluations, S01 disposition invariants, S02B permission boundary, S03A gateway invariants and active risks/issues.

## N. Next architectural problem

The agent can choose a safe next action and stop correctly under simple conditions. It cannot continue intelligently after transient failures, distinguish retryable from terminal run failures, manage independent token/time/cost/tool-call budgets, cancel in-flight work, use model/tool fallbacks, recover from dead ends, reconcile ambiguous writes or preserve an in-flight run after process failure. Treating every error as immediate escalation is safe but operationally weak; adding ad hoc branches to the minimal loop would make behavior inconsistent.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 3C — Loop Failure Handling, Recovery and Runtime Budgets**. Reconstruct the `0.6.0` baseline, preserve `AGT-001`, `DATA-009`, `TOOL-001`–`TOOL-006`, gateway-only enforcement, deterministic completion and all unapproved/human-review invariants. Add layered iteration, time, token, cost, tool-call and failure budgets; retry classification; dead-end recovery; bounded replanning; model/tool fallback; timeout/cancellation handling; partial completion; safe write reconciliation/compensation boundaries and final recovery evidence. Update all artefacts, tests and handoff, perform the consistency audit and stop before graph, harness, memory or multi-agent engineering.
