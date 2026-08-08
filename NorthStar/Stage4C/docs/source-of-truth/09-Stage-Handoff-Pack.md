
# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S04C`
- **Stage title:** Agent Harness Engineering
- **Architecture version:** `1.0.0`
- **Repository version:** `1.0.0`
- **Handoff version:** `1.0.0`
- **Completion date:** 2026-07-31
- **Status:** Completed within the local/offline SQLite, local-workspace and synthetic-identity verification boundary.
- **Consistency audit:** Passed with recorded reconstruction and production exceptions.

## B. Capabilities now available

1. All accepted S04B one-agent, typed graph, gateway, budget/recovery/reconciliation, durable wait, external decision, expiry and lease controls remain.
2. A framework-neutral compositional harness now surrounds `AGT-001` and unchanged `GRAPH-001` 1.1.0.
3. `DATA-063` binds agent, graph, tools, instruction, validators, hooks and explicit future-stage disable flags.
4. `DATA-064` instructions are versioned and SHA-256 verified; they explicitly grant no authority.
5. `DATA-065` context is authorized before source loading, typed, ordered, bounded, hashed and provenance-preserving; memory context is rejected.
6. Registries reject duplicates and freeze before runtime; model text/arguments cannot register tools.
7. `DATA-066`/`067` create a session-scoped bounded workspace with path/suffix/quota/sensitive-field controls.
8. Start, accepted decision and resume share session/run/trace correlation and delegate to existing graph/approval/store contracts.
9. `DATA-069` observer hooks expose evaluation findings without mutation/authorization/route access.
10. `DATA-068` redacted JSONL traces cover start, suspension, decision, resume and completion; they are explicitly not audit.
11. `DATA-070` provides a typed harness result while excluding the transient callback token from persisted results.
12. Approved/rejected/expired routes remain distinct and preliminary; timeout never approves and `TOOL-006` remains one effect.
13. Twenty-four S04C tests and five evaluations passed locally.

Not implemented: formal machine-readable agent specification, memory, context compaction/regeneration across long histories, concurrent graph branches, second agent, dynamic plugins, distributed registries/workers, enterprise sandbox/DLP/IAM/PDP/KMS, live model/connectors, OpenTelemetry exporter, audit/WORM, production SLO/cost benchmark, deployment or DR.

## C. Accepted architecture decisions

`ADR-001`–`032` remain accepted.

- `ADR-033`: use a framework-neutral compositional harness inside existing orchestration/runtime boundaries without changing `GRAPH-001` or adding an agent.
- `ADR-034`: bind runs to versioned instructions, authorized bounded context, frozen registries and deterministic lifecycle validation.
- `ADR-035`: use observer-only evaluation hooks and privacy-preserving correlated local tracing without an audit claim.

## D. Current component inventory

| ID | Name | Stage 4C responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Calls harness start/status/decision/resume surfaces; no browser UI implemented. |
| `CMP-002` | Regulatory Intake Boundary | Retained bounded publication intake and provenance. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Owns the framework-neutral harness lifecycle and delegates execution to unchanged `GRAPH-001` 1.1.0. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supplies authorized typed context sources; access remains before text assembly. |
| `CMP-005` | Enterprise Integration Boundary | Authoritative frozen tool registry/gateway; `TOOL-001`–`006` only; idempotent effects retained. |
| `CMP-006` | Human Review and Approval Boundary | Existing external typed decision service; harness exposes lifecycle but does not approve or interpret decisions. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Synthetic principal/role checks retained; context authorization input and enterprise IAM/PDP remain pending. |
| `CMP-008` | Evaluation and Assurance Boundary | Deterministic validators and observer-only lifecycle evaluation hooks. |
| `CMP-009` | Observability and Audit Boundary | Redacted local JSONL trace evidence; explicitly not production audit. |
| `CMP-010` | Runtime and Deployment Boundary | Python 3.13.5, SQLite, session/workspace manager, local filesystem, sequential runner and resume lease. |
| `CMP-011` | Source-of-Truth Governance Pack | Updated to architecture/repository/handoff 1.0.0. |## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose `TOOL-001`–`006`, complete or escalate. Cannot register capabilities, grant authority, choose graph routes, set waits/timeouts/leases, approve/finalize, use memory, delegate or create agents. | Implemented through the S04C harness; only agent. |

## F. Current data and state objects

- `DATA-001`–`062` retained; `DATA-009` remains `1.1.0`.
- New executable objects: `DATA-063 HarnessManifest`, `DATA-064 InstructionBundle`, `DATA-065 ContextEnvelope`, `DATA-066 HarnessSession`, `DATA-067 WorkspaceManifest`, `DATA-068 TraceEvent`, `DATA-069 HookResult`, `DATA-070 HarnessRunResult`.
- Raw approval token remains transient and is not persisted in workspace, session, trace or workflow records.
- No memory record, audit ledger, final legal conclusion or enterprise case closure is created.

## G. Current interfaces and tools

- `INT-001`–`040` retained.
- `INT-041` Harness Bootstrap and Lifecycle Contract.
- `INT-042` Instruction Resolution Contract.
- `INT-043` Context Assembly Contract.
- `INT-044` Session and Workspace Contract.
- `INT-045` Lifecycle Validation and Evaluation Hook Contract.
- `INT-046` Trace Emission Contract.
- `TOOL-001`–`003` remain read-only; `TOOL-004`–`006` remain reversible unapproved writes; every action remains through `INT-017`/`CMP-005`.

## H. Repository state

```text
northstar-agentic-compliance/
├── config/{graph,harness,runtime}/
├── docs/
│   ├── adr/ADR-033...ADR-035*.md
│   ├── architecture/diagrams/stage-4c-*.mmd
│   ├── baseline/Stage-4B-Handoff-Pack-supplied.md
│   ├── references/Stage-4C-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-4C-Agent-Harness-Engineering.md
├── schemas/DATA-063...DATA-070*.schema.json
├── scripts/{run_stage4c_demo,run_stage4c_evaluation,validate_stage4c,consistency_audit_stage4c}.py
├── src/northstar_compliance/
│   ├── approval/{token,service}.py
│   ├── durable/store.py
│   ├── evaluation/stage4c.py
│   ├── graph/{models,runtime,factory}.py
│   ├── harness/{context,factory,hooks,instructions,models,registries,runtime,tracing,validation,workspace}.py
│   └── tools/gateway.py
├── tests/{unit,integration,security,evaluation}/
├── README.md
└── pyproject.toml
```

Python target `>=3.11,<3.15`; executed on `3.13.5`. Runtime standard library only; pytest `9.0.2`.

## I. Tests completed

- `TEST-159`–`164`: manifest/future flags/instruction/context access, memory rejection and deterministic budget — passed.
- `TEST-165`–`169`: frozen registries, workspace containment, trace redaction, observer hook and no dynamic tool registration — passed.
- `TEST-170`–`177`: harness start/wait, no raw token, approve/reject/timeout, restart and compatibility mismatch — passed.
- `TEST-178`–`182`: SoD, token tampering, trace privacy/correlation and no future-stage modules — passed.

Executed result: **24 tests passed**. Demo, five-case evaluation, package compilation, structural validation and consistency audit passed.

Evaluations:

- `EVAL-037`: approved lifecycle through harness; preliminary approved; one `TOOL-006`; correlated/redacted trace.
- `EVAL-038`: rejected lifecycle; preliminary rejected; one `TOOL-006`.
- `EVAL-039`: expired wait escalates and remains unapproved.
- `EVAL-040`: manifest/instruction/access/future-stage boundary checks.
- `EVAL-041`: workspace/trace secret exclusion and explicit non-audit boundary.

## J. Known limitations

Reconstruction overlay; synthetic identity/local secret; local filesystem and SQLite; no production sandbox/DLP/KMS/IAM/PDP; no automatic event trigger; no distributed registry/workflow/trace exporter; no audit/WORM; no formal agent specification; no memory/context compaction; no concurrency or multiple agents; no live model/connectors; no production performance, reliability or cost benchmark; Mermaid not CLI-rendered.

## K. Open risks, assumptions and issues

- New risks: `RSK-087`–`098`.
- New assumptions: `ASM-031`–`034`.
- New issues: `ISS-043`–`049`.
- All inherited active production gaps remain.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and `AGT-001` as the only agent.
2. Preserve `GRAPH-001` `1.1.0`, `DATA-009` `1.1.0`, application-owned routes and node/state ownership.
3. Preserve gateway-only `TOOL-001`–`006`, access-before-context and S03C budgets/recovery/reconciliation.
4. Preserve external typed role/SoD/expiry/single-use decisions; timeout never approves; late decisions fail closed.
5. Approved/rejected remain preliminary human-reviewed dispositions, not final legal/compliance closure.
6. Preserve original `TOOL-006` idempotency key/effect and atomic revision/lease controls.
7. Preserve manifest/instruction/context/session digests and fail closed on incompatibility.
8. Prompts, hooks and registries cannot create authority or bypass deterministic controls.
9. Trace/workspace/checkpoint records are not memory, event sourcing, audit/WORM or exactly-once proof.
10. Do not add memory, concurrent graph branches or multiple agents until separate requirements/ADRs justify them.

## M. Required input for the next stage

Use all ten `1.0.0` artefacts; `ADR-001`–`035`; `GRAPH-001` `1.1.0`; `DATA-007`, `DATA-009`, `DATA-041`–`070`; `INT-009`–`046`; `TOOL-001`–`006`; `AGT-001`; the harness manifest/instruction/context/session/workspace/trace contracts; cumulative/focused diagrams; S04C code/tests/evaluations; and active risks/issues.

## N. Next architectural problem

The harness makes runtime behavior repeatable, but the authoritative definition of `AGT-001` is still distributed across instructions, graph invariants, code, requirements and tests. NorthStar needs a formal machine-readable agent specification for purpose, goals, non-goals, pre/postconditions, authority, tool/data access, approval, termination, SLOs, evaluation and retirement before adding long-lived context or memory.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 5A — Agent Specification Engineering**. Reconstruct the `1.0.0` S04C baseline; preserve `GRAPH-001` 1.1.0, the framework-neutral harness, `AGT-001` as the only agent, gateway-only tools, external human decisions and no-memory/no-concurrency boundaries. Create a formal machine-readable specification and derive runtime assertions, tests and evaluation/deployment gates from it. Update all artefacts, perform the consistency audit and stop before context compaction, long-term memory, concurrent branches or multi-agent engineering.
