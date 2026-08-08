# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S05A`
- **Stage title:** Specification and Context Engineering — Agent Specification Boundary
- **Architecture version:** `1.1.0`
- **Repository version:** `1.1.0`
- **Handoff version:** `1.1.0`
- **Completion date:** 2026-08-01
- **Status:** Completed within the local/offline standard-library, file-config and synthetic-context verification boundary.
- **Consistency audit:** Passed with recorded reconstruction and production exceptions.

## B. Capabilities now available

1. All accepted S04C one-agent graph/harness/gateway/budget/recovery/durable wait/external approval controls remain.
2. `DATA-071 AGT-001 AgentSpecification` formally defines purpose, ownership, users, goals, non-goals, contracts, authority, context, approval, termination, errors, provisional SLOs, evaluation and retirement.
3. JSON is canonical locally; Draft 2020-12 schema artefacts and strict application semantic validation reject unknown fields and accepted-architecture drift.
4. Canonical SHA-256 binds `AGT-001-spec` `1.0.0` into the harness manifest through `DATA-072`.
5. `INT-049` derives deterministic pre-start and post-result assertions without granting permission or choosing routes.
6. `DATA-077` formalizes access-before-load, allowed/prohibited context kinds, provenance/hash, ordering and 8-item/12,000-character budgets.
7. Memory, cross-case reuse, compaction/regeneration, concurrent graph branches and multiple agents remain disabled.
8. `DATA-075` maps required tests/evaluations; `DATA-076` is a deny-by-default local gate.
9. Missing evaluation/security/human-approval evidence blocks the gate.
10. Active/deprecated/retired lifecycle and retirement criteria exist; retired specifications deny new starts.
11. Thirty S05A tests and six evaluations passed locally.

Not implemented: production signed registry/attestation, enterprise IAM/PDP/KMS, live connectors/models, schema-validator conformance matrix, production SLO/cost/quality benchmark, context compaction, memory, concurrent branches, second agent, MCP/A2A, control plane, audit/WORM, deployment or DR.

## C. Accepted architecture decisions

`ADR-001`–`035` remain accepted.

- `ADR-036`: use one formal machine-readable `AGT-001` specification that grants no runtime authority.
- `ADR-037`: use canonical JSON, Draft 2020-12 schema artefacts, semantic validation and SHA-256 content binding.
- `ADR-038`: derive manifest binding, runtime assertions, evaluation obligations and deny-by-default gates while preserving existing control owners.
- `ADR-039`: formalize current bounded context policy without adding memory or compaction.

## D. Current component inventory

| ID | Name | Current S05A responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Calls specification-guarded harness lifecycle; no browser UI/new authority. |
| `CMP-002` | Regulatory Intake Boundary | Retained bounded publication intake/provenance. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Resolves/binds specification, runs assertions and delegates to unchanged `GRAPH-001`. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supplies `DATA-077`-permitted, authorized typed context. |
| `CMP-005` | Enterprise Integration Boundary | Remains authoritative exact tool registry/gateway for `TOOL-001`–`006`. |
| `CMP-006` | Human Review and Approval Boundary | Remains authoritative typed decision service. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Remains external authorization owner; synthetic local claims only. |
| `CMP-008` | Evaluation and Assurance Boundary | Specification validation, runtime assertion evidence and local deployment gate. |
| `CMP-009` | Observability and Audit Boundary | May record redacted spec/assertion/gate evidence; not audit/WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Local Python runtime and gate execution; no production attestation. |
| `CMP-011` | Source-of-Truth Governance Pack | Version/change/ADR/traceability governance at `1.1.0`. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose exact `TOOL-001`–`006` through `CMP-005`, complete or escalate. Cannot grant authority, approve/finalize, choose routes, alter runtime controls, use memory, delegate, create agents or run concurrent branches. | Only agent; implemented and formally specified by `AGT-001-spec` `1.0.0`. |

## F. Current data and state objects

- `DATA-001`–`070` retained; `DATA-009` remains `1.1.0`.
- New: `DATA-071 AgentSpecification`, `DATA-072 SpecificationBinding`, `DATA-073 RuntimeAssertionResult`, `DATA-074 SpecificationValidationReport`, `DATA-075 EvaluationObligation`, `DATA-076 DeploymentGateResult`, `DATA-077 ContextPolicyProfile`, `DATA-078 RetirementDecision`.
- No memory record, context summary/compaction artefact, audit ledger, final legal conclusion or enterprise case closure is created.

## G. Current interfaces and tools

- `INT-001`–`046` retained.
- `INT-047` Agent Specification Resolution Contract.
- `INT-048` Specification Validation and Compatibility Contract.
- `INT-049` Runtime Specification Assertion Contract.
- `INT-050` Evaluation and Deployment Gate Contract.
- `INT-051` Context Policy Binding Contract.
- `INT-052` Specification Lifecycle and Retirement Contract.
- `TOOL-001`–`003` read-only; `TOOL-004`–`006` reversible unapproved writes; all remain gateway-only.

## H. Repository state

```text
northstar-agentic-compliance/
├── config/{agents,evaluation,harness}/
├── docs/
│   ├── adr/ADR-036...ADR-039*.md
│   ├── architecture/diagrams/stage-5a-*.mmd
│   ├── baseline/Stage-4C-Handoff-Pack-supplied.md
│   ├── references/Stage-5A-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-5A-Agent-Specification-and-Context-Engineering.md
├── schemas/DATA-071...DATA-078*.schema.json
├── scripts/{run_stage5a_demo,run_stage5a_evaluation,benchmark_stage5a,validate_stage5a,consistency_audit_stage5a}.py
├── src/northstar_compliance/
│   ├── harness/specification_guard.py
│   └── specification/{assertions,canonical,context_policy,gates,integration,loader,models,validator}.py
├── tests/{unit,integration,security,evaluation}/
├── README.md
└── pyproject.toml
```

Python target `>=3.11,<3.15`; executed on Python `3.13.5`. Runtime standard library only; pytest `9.0.2` for tests.

## I. Tests completed

- `TEST-183`–`191`: valid/canonical/strict specification, stable agent/graph/owners/invariants/retirement — passed.
- `TEST-192`–`200`: manifest binding, pre/post assertions, timeout/duplicate effect, deployment gate, retired start — passed.
- `TEST-201`–`208`: authority expansion, dynamic tool/direct adapter, memory/unauthorized/budget context, token persistence and final closure — passed.
- `TEST-209`–`212`: completeness, authority/context, security-finding and human-semantics evaluation gates — passed.

Executed result: **30 tests passed**. Package compilation, demo, six evaluations, local microbenchmark, structural validation and consistency audit passed.

Evaluations:

- `EVAL-042`: specification completeness and semantic consistency.
- `EVAL-043`: pre-start/post-result runtime assertion lifecycle.
- `EVAL-044`: authority expansion and manifest drift resistance.
- `EVAL-045`: context-policy and no-memory boundary.
- `EVAL-046`: complete evidence passes; missing evaluation blocks local gate.
- `EVAL-047`: retired new start denied and final closure remains external.

## J. Known limitations

Compatible reconstruction overlay; unsigned local JSON/config; no external schema conformance matrix; synthetic context/identity; no live harness repository integration beyond the adapter boundary; no production IAM/PDP/KMS/attestation; no production performance/reliability/cost/quality benchmark; no context compaction or memory; no concurrency/multiple agents; no audit/WORM/deployment/DR; Mermaid not CLI-rendered.

## K. Open risks, assumptions and issues

- New risks: `RSK-099`–`111`.
- New assumptions: `ASM-035`–`038`.
- New issues: `ISS-050`–`056`.
- All inherited active production gaps remain.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and `AGT-001` as the only agent.
2. Preserve `GRAPH-001` `1.1.0`, `DATA-009` `1.1.0`, application-owned routes and node/state ownership.
3. Preserve exact gateway-only `TOOL-001`–`006`, access-before-context and S03C budgets/recovery/reconciliation.
4. Preserve S04B external typed role/SoD/expiry/single-use decisions; timeout never approves; late decisions fail closed.
5. Approved/rejected remain preliminary human-reviewed dispositions, not final legal/compliance closure.
6. Preserve original `TOOL-006` idempotency/effect and atomic revision/lease controls.
7. Preserve manifest/instruction/context/session/specification digests and fail closed on incompatibility.
8. Specifications, prompts, hooks, evaluators and registries cannot grant authority or bypass graph/gateway/approval/PDP controls.
9. Trace/workspace/checkpoint/specification evidence is not memory, event sourcing, audit/WORM or exactly-once proof.
10. Do not enable memory, compaction, cross-case reuse, concurrent graph branches or multiple agents without separate requirements/ADRs.

## M. Required input for the next stage

Use all ten `1.1.0` artefacts; `ADR-001`–`039`; `AGT-001-spec` `1.0.0`; `GRAPH-001` `1.1.0`; `DATA-007`, `DATA-009`, `DATA-041`–`078`; `INT-009`–`052`; `TOOL-001`–`006`; the S04C harness manifest/instruction/context/session/workspace/trace contracts; `DATA-077` context policy; S05A code/tests/evaluations/benchmark; cumulative/focused diagrams; and all active risks/issues.

## N. Next architectural problem

The agent is now formally specified and its current context boundary is executable. However, an investigation that spans many documents, human waits or repeated sessions can exceed the bounded `DATA-065` envelope. NorthStar has not defined how to compact or regenerate context, which facts stay in structured state, what may become working/episodic/semantic/user/organizational memory, who may write/read/delete it, how freshness/conflicts/provenance/consent/retention work, or how cross-case/user leakage is prevented.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 5B — Context Lifecycle, Compaction and Memory Boundaries**. Reconstruct the `1.1.0` S05A baseline; preserve `AGT-001-spec` 1.0.0, `GRAPH-001` 1.1.0, one-agent/gateway/external-approval semantics and the current no-memory default. Design explicit context regeneration and state-versus-memory boundaries, enable only the minimum justified memory capability with consent, provenance, expiry, deletion and isolation controls, update all artefacts, execute tests/audit and stop before multi-agent engineering.
