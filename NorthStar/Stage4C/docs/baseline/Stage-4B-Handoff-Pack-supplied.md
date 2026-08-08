# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S04B`
- **Stage title:** Checkpointing, Durable Execution and Human Approval
- **Architecture version:** `0.9.0`
- **Repository version:** `0.9.0`
- **Handoff version:** `0.9.0`
- **Completion date:** 2026-07-31
- **Status:** Completed within the local/offline SQLite and synthetic-identity verification boundary.
- **Consistency audit:** Passed with recorded reconstruction and production exceptions.

## B. Capabilities now available

1. All accepted S04A one-agent, typed graph, gateway, budget/recovery/reconciliation and preliminary-disposition controls remain.
2. `GRAPH-001` advances to `1.1.0` with explicit wait, decision, approved, rejected and expiry/escalation nodes.
3. `CMP-006` can create `DATA-059` waits and persist local `DATA-007` review decisions.
4. The graph releases execution resources at `N80_REVIEW_DECISION_GATE` and survives process restart through `DATA-058`.
5. HMAC-signed expiring callback claims bind wait, run, review request and graph version.
6. Reviewer role, separation of duties, decision enum, rejection reason, active token and single use are enforced deterministically.
7. Timeout routes to escalation and never approval.
8. A bounded `DATA-062` lease prevents duplicate simultaneous resume.
9. Approved and rejected routes produce distinct preliminary human-reviewed dispositions; neither claims final legal/compliance closure.
10. Completed `TOOL-006` is not repeated after restart/resume.
11. Twenty-five S04B tests and four evaluations passed locally.

Not implemented: enterprise reviewer authentication/PDP, live callback endpoint, automatic scheduler/event trigger, dual approval, delegation/override, distributed workflow engine, event sourcing/audit/WORM, multi-region durability/DR, graph migration, concurrent branches, memory, harness, multiple agents, live model/connectors or production benchmark.

## C. Accepted architecture decisions

`ADR-001`–`ADR-029` remain accepted.

- `ADR-030`: place human approval after the deterministic complete unapproved package.
- `ADR-031`: use a persisted external-event wait with explicit expiry rather than blocking or polling.
- `ADR-032`: use a transactional SQLite local adapter while preserving migration to a production durable engine.

## D. Current component inventory

| ID | Name | Current responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Start/wait/deadline/resume caller. |
| `CMP-002` | Regulatory Intake Boundary | Retained. |
| `CMP-003` | Case and Workflow Orchestration Boundary | `GRAPH-001` 1.1.0, suspension, decision routes and lease-protected resume. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Retained synthetic authorized evidence. |
| `CMP-005` | Enterprise Integration Boundary | Authoritative gateway and idempotent `TOOL-006`. |
| `CMP-006` | Human Review and Approval Boundary | Local durable wait, signed decision validation, decision persistence and expiry. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Synthetic role/SoD checks; enterprise IAM/PDP pending. |
| `CMP-008` | Evaluation and Assurance Boundary | Wait/restart/security/timeout/route evaluations. |
| `CMP-009` | Observability and Audit Boundary | Local transition/decision evidence only; not audit. |
| `CMP-010` | Runtime and Deployment Boundary | Python 3.13.5, SQLite, sequential runner and short resume lease. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented at `0.9.0`. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose `TOOL-001`–`006`, complete or escalate. Cannot create/validate decisions, choose human routes, set waits/timeouts/leases, approve/finalize, delegate or create agents. | Implemented and locally verified; only agent. |

## F. Current data and state objects

- `DATA-001`–`057` retained; `DATA-009` remains `1.1.0`.
- `DATA-007 ReviewDecision` is now executable locally at `1.0.0`.
- New: `DATA-058 DurableWorkflowRecord`, `DATA-059 HumanApprovalWait`, `DATA-060 ApprovalCallbackTokenClaims`, `DATA-061 ApprovalInboxEvent`, `DATA-062 WorkflowResumeLease`.
- No accepted enterprise case closure, audit record or final legal conclusion is created.

## G. Current interfaces and tools

- `INT-001`–`035` retained.
- `INT-036` Durable Workflow Persistence Contract.
- `INT-037` Human Approval Wait Contract.
- `INT-038` Review Decision Submission and Validation Contract.
- `INT-039` Timeout and Escalation Contract.
- `INT-040` Safe Resume and Lease Contract.
- `TOOL-001`–`003` read-only; `TOOL-004`–`006` reversible unapproved writes; every action remains through `INT-017`/`CMP-005`.

## H. Repository state

```text
northstar-agentic-compliance/
├── config/{graph,runtime}/
├── docs/
│   ├── adr/ADR-030...ADR-032*.md
│   ├── architecture/diagrams/stage-4b-*.mmd
│   ├── references/Stage-4B-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-4B-Checkpointing-Durable-Execution-and-Human-Approval.md
├── schemas/DATA-007,DATA-058...DATA-062*.schema.json
├── scripts/{run_stage4b_demo,run_stage4b_evaluation,validate_stage4b,consistency_audit_stage4b}.py
├── src/northstar_compliance/
│   ├── approval/{token,service}.py
│   ├── durable/store.py
│   ├── graph/{models,definition,runtime,factory}.py
│   └── tools/gateway.py
├── tests/{unit,integration,security,evaluation}/
├── README.md
└── pyproject.toml
```

Python target `>=3.11,<3.15`; executed on `3.13.5`. Runtime standard library only; pytest `9.0.2`.

## I. Tests completed

- `TEST-134`–`138`: graph/store/checksum/raw-token persistence — passed.
- `TEST-139`–`145`: signature, expiry, role, SoD, reason, enum and single-use controls — passed.
- `TEST-146`–`154`: suspension, no-event wait, approve/reject/timeout, restart, no duplicate tool, lease and graph-version mismatch — passed.
- `TEST-155`–`158`: no replay, transition evidence, one-agent boundary and non-final disposition — passed.

Executed result: **25 tests passed**. Demo, evaluation, compilation, structural validation and consistency audit passed.

Evaluations: `EVAL-033` approved, `EVAL-034` rejected, `EVAL-035` timeout-escalated, `EVAL-036` one-agent/no-future-modules.

## J. Known limitations

Synthetic identity and local secret; one SQLite host; no automatic event-triggered resume; no production callback gateway/rate limits; no dual approval/delegation/override; no managed workflow conformance; no distributed timers/workers, event history, graph migration, audit/WORM, backup/DR, live model/connectors, production benchmark, harness, memory, concurrent branches or multiple agents.

## K. Open risks, assumptions and issues

- New risks: `RSK-077`–`RSK-086`.
- New assumptions: `ASM-028`–`ASM-030`.
- New issues: `ISS-036`–`ISS-042`.
- Inherited active risks/issues remain.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and `AGT-001` as the only agent.
2. Preserve gateway-only tools, access-before-context, S03C budgets/recovery/reconciliation and S04A node/route ownership.
3. Preserve `DATA-009` `1.1.0`; preserve `GRAPH-001` `1.1.0` for in-flight waits or define an explicit migration ADR.
4. Human decisions must remain external, typed, role/SoD checked, expiring and single-use.
5. Timeout must never approve; late decisions must fail closed.
6. Approved means controlled continuation of a preliminary package, not final legal/compliance closure.
7. Do not repeat completed `TOOL-006` on resume; retain the original idempotency key.
8. Resume ownership must remain atomic; do not remove revision/lease controls without replacement guarantees.
9. Durable records are not memory, event sourcing, audit ledger or exactly-once proof.
10. Do not add memory, concurrent graph branches or multiple agents in the next substage unless separately requested and justified.

## M. Required input for the next stage

Reconstruct all ten `0.9.0` artefacts, `ADR-001`–`032`, `GRAPH-001` `1.1.0`, `DATA-007`, `DATA-009`, `DATA-041`–`062`, `INT-009`–`040`, `TOOL-001`–`006`, `AGT-001`, cumulative/focused diagrams, S04B code/tests/evaluations and active risks/issues.

## N. Next architectural problem

The graph, tools, durable state, approval, budgets, policy hooks and evaluations now work, but cross-cutting runtime responsibilities are scattered across modules and wiring. NorthStar needs an agent harness that standardizes instruction/context assembly, registries, validation, session/workspace controls, checkpoints, approvals, evaluation hooks and tracing without turning prompts into security controls or adding memory/multiple agents prematurely.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 4C — Agent Harness Engineering**. Reconstruct the `0.9.0` baseline; preserve `GRAPH-001` 1.1.0, `AGT-001`, gateway-only tools, typed state, durable human wait/decision routes, budgets/recovery/reconciliation and preliminary human-accountability semantics. Introduce a framework-neutral harness only to consolidate existing cross-cutting runtime responsibilities; stop before memory, concurrent branches or multi-agent engineering. Update all artefacts, tests and handoff, perform the consistency audit and stop after this stage.
