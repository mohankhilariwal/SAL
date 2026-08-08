# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S04A`
- **Stage title:** Graph Foundations and Typed State
- **Architecture version:** `0.8.0`
- **Repository version:** `0.8.0`
- **Handoff version:** `0.8.0`
- **Completion date:** 2026-07-31
- **Status:** Completed within the local/offline synthetic verification boundary.
- **Consistency audit:** Passed with recorded exceptions `ISS-014`, `ISS-015`, `ISS-021`–`ISS-035` and inherited production gaps.

## B. Capabilities now available

1. All S03C one-agent, gateway-only, budget, recovery, cancellation, reconciliation, checkpoint and deterministic unapproved-completion capabilities remain.
2. `GRAPH-001` explicitly represents deterministic, model, policy, tool, recovery and termination nodes.
3. `DATA-053` defines a versioned graph; `INT-031` validates node/edge integrity and reachability before execution.
4. `DATA-054` wraps unchanged `DATA-009 AgentRunState` `1.1.0` with graph/current-node/pending/transition fields.
5. Nodes receive snapshots and return `DATA-055 GraphNodeResult` plus `DATA-056 GraphStatePatch`.
6. `INT-033` enforces exact node-owned mutation paths and rejects protected authority, budget, goal and disposition fields.
7. `INT-034` maps named routes to targets; provider output cannot name arbitrary nodes.
8. `N30` makes policy preflight visible while `CMP-005` remains the authoritative gateway for every action.
9. `N50` reuses S03C read fallback and ambiguous-write reconciliation; no blind write retry is added.
10. `DATA-057` records ordered source/type/route/target/evidence transitions.
11. `DATA-050` checkpoints `DATA-054` after every accepted transition and binds resume to graph ID/version.
12. A resumed local run continues from `current_node` without repeating completed `TOOL-001` work in the executed test.
13. The happy path completes with six milestones, three unapproved artifacts, seven model calls, six tool calls and 41 graph transitions.
14. Twenty-four S04A tests and six evaluations passed locally.

Not implemented: actual human approval decision/wait, durable timers/workers, distributed workflow execution, event sourcing, graph migration, concurrent branches, memory, harness, multiple agents, live model/connectors, enterprise identity/PDP, production telemetry/audit/records, compensation execution, deployment or DR.

## C. Accepted architecture decisions

`ADR-001`–`ADR-026` remain accepted.

- `ADR-027`: replace implicit imperative control flow with `GRAPH-001` while preserving one agent and existing authority.
- `ADR-028`: use a framework-neutral application-owned local graph kernel before selecting a framework, managed state machine or durable workflow engine.
- `ADR-029`: use node-owned copy-on-write patches and graph-version-bound current-state checkpoints.

## D. Current component inventory

| ID | Name | Current responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Local graph run/cancel/resume caller and path/outcome viewer. |
| `CMP-002` | Regulatory Intake Boundary | Retained. |
| `CMP-003` | Case and Workflow Orchestration Boundary | `GRAPH-001`, typed state/patches/routes, transition checkpoints, S03C budgets/recovery and deterministic termination. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Retained synthetic authorized evidence. |
| `CMP-005` | Enterprise Integration Boundary | Authoritative gateway, registered read fallback and write reconciliation. |
| `CMP-006` | Human Review and Approval Boundary | Local queued request only; no wait/decision service. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Partial unauthenticated local principal/write-scope enforcement; graph policy node is preflight. |
| `CMP-008` | Evaluation and Assurance Boundary | Graph definition, path, patch ownership, resume, failure and boundary evaluations. |
| `CMP-009` | Observability and Audit Boundary | Local transition/checkpoint evidence only; not audit. |
| `CMP-010` | Runtime and Deployment Boundary | Python 3.13.5 single-process sequential graph. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented at `0.8.0`. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose `TOOL-001`–`006`, complete or escalate. Cannot choose graph nodes/routes, mutate state, set budgets/recovery/reconciliation, approve/finalize, compensate, delegate, create agents, execute code or handle unrestricted credentials. | Implemented and locally verified; only agent. |

## F. Current data and state objects

- `DATA-001`–`DATA-052` retained.
- `DATA-009 AgentRunState` remains schema `1.1.0`.
- `DATA-050` remains the checksummed atomic local current-state checkpoint and now stores `DATA-054` as payload.
- New: `DATA-053 ExecutionGraphDefinition`, `DATA-054 TypedGraphExecutionState`, `DATA-055 GraphNodeResult`, `DATA-056 GraphStatePatch`, `DATA-057 GraphTransitionRecord`.
- No accepted enterprise `RegulatoryCase` or `ReviewDecision` is instantiated. Local case/mapping/review artifacts remain reversible and unapproved.

## G. Current interfaces and tools

- `INT-001`–`INT-030` retained.
- `INT-031` Graph Definition Validation Contract.
- `INT-032` Node Execution Contract.
- `INT-033` State Patch Application Contract.
- `INT-034` Transition Routing Contract.
- `INT-035` Graph Run and Resume Contract.
- `TOOL-001`–`003` remain read-only; `TOOL-004`–`006` remain reversible unapproved writes.
- Every action continues through `INT-017`/`CMP-005`; policy preflight does not replace gateway authorization.

## H. Repository state

Repository `northstar-agentic-compliance` version `0.8.0`. Important entry points:

```text
northstar-agentic-compliance/
├── config/{graph,runtime}/
├── docs/
│   ├── adr/ADR-027...ADR-029*.md
│   ├── architecture/diagrams/*.mmd
│   ├── references/Stage-4A-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-4A-Graph-Foundations-and-Typed-State.md
├── schemas/DATA-053...DATA-057*.schema.json
├── scripts/{run_stage4a_demo,run_stage4a_evaluation,validate_stage4a,consistency_audit_stage4a}.py
├── src/northstar_compliance/
│   ├── agent/{models,budgets,decision,termination}.py
│   ├── graph/{models,definition,state,nodes,runtime,factory}.py
│   ├── state/checkpoint.py
│   └── tools/gateway.py
├── tests/{unit,integration,security,evaluation}/
├── README.md
└── pyproject.toml
```

Python target `>=3.11,<3.15`; executed on `3.13.5`. Runtime dependencies: standard library only. Test dependency: pytest `9.0.2`.

## I. Tests completed

- `TEST-110`–`114`: graph definition validity/fail-closed cases — passed.
- `TEST-115`–`117`: patch ownership, copy-on-write and disposition protection — passed.
- `TEST-118`–`120`: happy path, conditional path and policy-before-write — passed.
- `TEST-121`–`124`: read fallback, ambiguous-write reconciliation, cancellation and graph budget — passed.
- `TEST-125`–`128`: checkpoint round trip, no repeated completed work, graph-version mismatch and checksum tamper — passed.
- `TEST-129`–`131`: one-agent/no-future-modules, gateway-only execution and restricted-evidence boundary — passed.
- `TEST-132`–`133`: recovery-path/efficiency metrics and run-scoped wall-time budget — passed.

Executed result: **24 tests passed**. Compilation, installed-package demo, evaluation, structural validator and consistency audit passed.

Evaluations:

| ID | Result |
|---|---|
| `EVAL-027` | Normal graph completed in 41 transitions. |
| `EVAL-028` | Transient evidence read used registered fallback and completed. |
| `EVAL-029` | Ambiguous draft write reconciled one committed case and completed. |
| `EVAL-030` | Checkpoint resumed same run without repeating completed `TOOL-001`. |
| `EVAL-031` | Write scope denial escalated before any write gateway call. |
| `EVAL-032` | Nine graph nodes, exactly one agent, no harness/memory/multi-agent modules. |

## J. Known limitations

1. Deterministic/scripted provider and synthetic token/cost usage.
2. Synthetic/local tools and unauthenticated principal claims.
3. Sequential single-process graph; no parallel branches/workers.
4. Local current-state checkpoint, not event sourcing/audit/distributed durability/DR.
5. No in-flight graph-version migration.
6. No actual human approval wait or decision processing.
7. No durable timer, queue, lease, distributed lock or concurrent resume protection.
8. No compensation execution.
9. Unsigned graph configuration, identity/policy evidence and checkpoints.
10. Copy-on-write state not benchmarked at enterprise scale.
11. No live graph-framework/managed-workflow conformance.
12. No production latency/concurrency/throughput/failure/cost benchmark.
13. Mermaid not rendered by CLI.
14. Compatible overlay rather than byte-exact `0.7.0` continuation (`ISS-032`).
15. No harness, memory, multi-agent, MCP/A2A or production control plane.

## K. Open risks, assumptions and issues

- New risks: `RSK-067`–`RSK-076`.
- New assumptions: `ASM-025`–`ASM-027`.
- New issues: `ISS-032`–`ISS-035`.
- Inherited active risks/issues remain.

## L. Compatibility constraints

1. Preserve NorthStar, all eight personas, `US-001`–`US-012`, `CMP-001`–`CMP-011` and accepted meanings.
2. Preserve S01/S02 unapproved/human-accountability and authorization-before-context semantics.
3. Preserve `TOOL-001`–`006`, `INT-017`, gateway-only execution, impact classes and idempotency.
4. Preserve `AGT-001` as the only low-authority agent.
5. Preserve `DATA-009` `1.1.0`, `DATA-041`–`057` and `INT-021`–`035` ownership/semantics.
6. Graph routing, budgets, failure classification, fallback, retry safety, reconciliation, completion and disposition remain application-owned.
7. Never blindly retry an ambiguous write; reconcile by the same idempotency key or escalate.
8. Partial/guard/cancel/escalation outcomes remain `preliminary_grounded_unapproved` and require human review.
9. Checkpoints/transitions are not memory, audit, event sourcing, durable replay or exactly-once guarantees.
10. A future framework mapping must preserve node ownership, protected paths, gateway authority and route semantics.
11. Do not add memory, multiple agents, concurrent branches or a harness in the next substage unless separately requested and justified.

## M. Required input for the next stage

Reconstruct all ten `0.8.0` artefacts, `ADR-001`–`029`, `GRAPH-001`, `DATA-009` `1.1.0`, `DATA-041`–`057`, `INT-009`–`035`, `TOOL-001`–`006`, `AGT-001`, cumulative/focused diagrams, S04A code/tests/evaluations, S01 disposition invariants, S02 permission boundary, S03A gateway invariants, S03C budget/recovery invariants and active risks/issues.

## N. Next architectural problem

`TOOL-006` can queue a review request, but `GRAPH-001` cannot yet enter a durable human-wait state, release execution resources, validate a reviewer decision, handle expiry/escalation or safely resume through approved/rejected branches. Local graph checkpoints are insufficient for hours- or days-long approval waits and do not provide distributed durability.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 4B — Human Approval, Waiting States and Durable Graph Resumption**. Reconstruct the `0.8.0` baseline; preserve `GRAPH-001`, `AGT-001`, `TOOL-001`–`TOOL-006`, node-owned typed state patches, gateway-only authority, S03C budgets/recovery/reconciliation, deterministic completion and unapproved/human-accountability semantics. Add explicit human-review wait, timeout, decision-validation and approved/rejected/escalated routes plus an appropriately justified durable-resumption option, while stopping before harness, memory, concurrency or multi-agent engineering. Update all artefacts, tests and handoff, perform the consistency audit and stop after this stage.
