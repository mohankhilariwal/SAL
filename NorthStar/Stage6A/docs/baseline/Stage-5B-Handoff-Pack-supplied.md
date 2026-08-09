# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S05B`
- **Stage title:** Context Lifecycle, Compaction and Memory Boundaries
- **Architecture version:** `1.2.0`
- **Repository version:** `1.2.0`
- **Handoff version:** `1.2.0`
- **Completion date:** 2026-08-01
- **Status:** Completed within the local/offline standard-library, synthetic-identity/consent, case-local file-store verification boundary.
- **Consistency audit:** Passed with recorded reconstruction and production exceptions.

## B. Capabilities now available

1. All accepted S05A one-agent/specification/graph/harness/gateway/budget/recovery/durable-wait/external-approval controls remain.
2. `INT-053` deterministically regenerates context from authorized `DATA-009` state and source metadata without a model call.
3. `INT-054` performs complete-item extractive compaction into `DATA-080`, pins case/approval state, preserves source bindings and records omissions.
4. The hard `DATA-077` boundary remains eight items/12,000 characters; the local target is six/8,000.
5. Context can be regenerated and the case resumed with memory disabled.
6. Only `DATA-081 case_working` memory is enabled, solely for case-session continuity.
7. `DATA-082` requires explicit, operation-specific, unexpired opt-in for write/read/delete.
8. Memory is isolated by tenant, case and authorized user; cross-case/profile/semantic/episodic/organizational/shared-agent memory remains disabled.
9. Only authoritative-state or human-decision-reference facts with source ID/version/hash may be persisted; the model has no memory-write tool.
10. Writes are idempotent, one record is active per case, and later writes supersede earlier ones.
11. Source-version conflicts are stale and excluded by default.
12. Provisional 14-day default/30-day maximum expiry, authorized deletion, content removal and content-free tombstones are implemented locally.
13. Poisoning, authority-field, token, path-traversal and digest-tamper tests pass.
14. `TEST-213`–`242` and `EVAL-048`–`054` pass locally.

Not implemented: production IAM/PDP/consent service, encryption/KMS/signatures, enterprise database, distributed idempotency/concurrency, backup deletion, legal holds/records schedules, audit/WORM, live model/connectors, production quality/SLO/cost benchmarks, multi-agent, concurrent branches, MCP/A2A, control plane, deployment or DR.

## C. Accepted architecture decisions

`ADR-001`–`039` remain accepted.

- `ADR-040`: separate authoritative state, disposable context and subordinate memory.
- `ADR-041`: use deterministic regeneration and extractive compaction; no durable model summaries.
- `ADR-042`: enable only opt-in, case-local working memory; no direct model write or broader memory category.
- `ADR-043`: require consent, exact isolation, provenance, expiry, staleness checks, deletion and minimal tombstones.

## D. Current component inventory

| ID | Name | Current S05B responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Requests start/resume and surfaces consent/continuity status; no new runtime authority. |
| `CMP-002` | Regulatory Intake Boundary | Retains source identity/version/provenance. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Owns regeneration, compaction and calls to memory lifecycle; `DATA-009` always wins. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Supplies authorized source bindings and current versions for freshness. |
| `CMP-005` | Enterprise Integration Boundary | Unchanged authoritative gateway for `TOOL-001`–`006`; memory is not an agent tool. |
| `CMP-006` | Human Review and Approval Boundary | Unchanged typed external decision service; tokens/signatures excluded from memory. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Conceptual owner of consent/purpose/scope; synthetic local grants only. |
| `CMP-008` | Evaluation and Assurance Boundary | Context/memory policy validation and `EVAL-048`–`054`. |
| `CMP-009` | Observability and Audit Boundary | Redacted lifecycle evidence; still not audit/WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Local atomic store, expiry and deletion; no production database/KMS. |
| `CMP-011` | Source-of-Truth Governance Pack | Version/change/ADR/traceability governance at `1.2.0`. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose exact `TOOL-001`–`006` through `CMP-005`, complete or escalate. Cannot write memory directly, grant consent, approve/finalize, choose routes, alter controls, delegate, create agents, run concurrent branches or recall across cases. | Only agent; `AGT-001-spec 1.1.0`. |

## F. Current data and state objects

- `DATA-001`–`078` retained; `DATA-009` remains `1.1.0`.
- New: `DATA-079 ContextRegenerationPlan`, `DATA-080 ContextSnapshot`, `DATA-081 CaseWorkingMemoryRecord`, `DATA-082 MemoryConsentGrant`, `DATA-083 MemoryQuery`, `DATA-084 MemoryReadResult`, `DATA-085 MemoryDeletionRequest`, `DATA-086 MemoryLifecycleResult`.
- `DATA-071`/`DATA-077` are updated for the S05B boundary; no final legal conclusion, enterprise case closure, audit ledger, user profile, semantic memory, episodic memory, organizational memory or shared-agent memory is created.

## G. Current interfaces and tools

- `INT-001`–`052` retained.
- `INT-053` Context Regeneration Contract.
- `INT-054` Context Compaction Contract.
- `INT-055` Case Working Memory Write Contract.
- `INT-056` Case Working Memory Read Contract.
- `INT-057` Memory Delete and Expire Contract.
- `INT-058` Memory Policy and Consent Validation Contract.
- `TOOL-001`–`003` remain read-only; `TOOL-004`–`006` remain reversible unapproved writes; all are gateway-only and unchanged.

## H. Repository state

```text
northstar-agentic-compliance/
├── config/{agents,evaluation,harness,memory}/
├── docs/
│   ├── adr/ADR-040...ADR-043*.md
│   ├── architecture/diagrams/stage-5b-*.mmd
│   ├── baseline/Stage-5A-Handoff-Pack-supplied.md
│   ├── references/Stage-5B-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-5B-Context-Lifecycle-Compaction-and-Memory-Boundaries.md
├── schemas/DATA-079...DATA-086*.schema.json
├── scripts/{run_stage5b_demo,run_stage5b_evaluation,benchmark_stage5b,validate_stage5b,consistency_audit_stage5b}.py
├── src/northstar_compliance/memory/{canonical,models,policy,regeneration,compaction,store,service,lifecycle}.py
├── tests/{unit,integration,security,evaluation}/
├── README.md
└── pyproject.toml
```

Python target `>=3.11,<3.15`; executed on Python `3.13.5`. Runtime standard library only; pytest `9.0.2` for tests.

## I. Tests completed

- `TEST-213`–`222`: authoritative deterministic regeneration, bounded/required/omission-aware compaction, authorization, token removal and hard budget — passed.
- `TEST-223`–`232`: consent, round-trip, idempotency/conflict, supersession, deletion, expiry, stale filtering and no-memory resume — passed.
- `TEST-233`–`242`: tenant/case/user isolation, unapproved origin/instruction/authority rejection, tamper/path controls and future-capability denial — passed.

Executed result: **31 pytest checks passed**, comprising 30 numbered tests plus the evaluation-configuration check. Package compilation, demo, seven evaluations, local benchmark, structural validation and consistency audit passed.

Evaluations:

- `EVAL-048`: deterministic authoritative regeneration and no-memory resume.
- `EVAL-049`: compaction budgets, required items, omissions and permission exclusion.
- `EVAL-050`: consented write/read, idempotency and single-active-record lifecycle.
- `EVAL-051`: tenant/case/user isolation and consent enforcement.
- `EVAL-052`: provenance, staleness, poisoning and tamper resistance.
- `EVAL-053`: expiry/deletion and content-free tombstone semantics.
- `EVAL-054`: local performance/size benchmark and preservation of one-agent/no-concurrency boundary.

## J. Known limitations

Compatible reconstruction overlay; synthetic/unsigned consent and identity; unencrypted local JSON; SHA-256 is not authenticated integrity; no enterprise schema conformance matrix; no distributed transactions/concurrency/replicas/backups; no deletion propagation/legal hold/records schedule; no live source-version feed/model/connectors; no semantic analyst-quality or production SLO/cost benchmark; no audit/WORM/deployment/DR; Mermaid not CLI-rendered; broader memory and multi-agent capabilities disabled.

## K. Open risks, assumptions and issues

- New risks: `RSK-112`–`128`.
- New assumptions: `ASM-039`–`043`.
- New issues: `ISS-057`–`064`.
- All inherited active production gaps remain.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one `AGT-001`.
2. Preserve `GRAPH-001 1.1.0`, `DATA-009 1.1.0`, application-owned routes/node/state ownership and sequential branches.
3. Preserve exact gateway-only `TOOL-001`–`006`, access-before-load and all S03C budgets/recovery/reconciliation.
4. Preserve S04B role/SoD/expiry/single-use human decisions; timeout never approves and late decisions fail closed.
5. Approved/rejected remain preliminary human-reviewed dispositions, not final legal/compliance closure.
6. Preserve original `TOOL-006` idempotency/effect and atomic revision/lease controls.
7. Preserve manifest/instruction/context/session/specification digests and fail closed on incompatibility.
8. Memory cannot grant authority, change graph state, override current sources, carry tokens/signatures/final closure or store hidden reasoning.
9. Only `case_working` memory is enabled; exact tenant/case/user scope, opt-in, provenance, expiry and deletion are mandatory.
10. Do not enable cross-case, profile, semantic, episodic, organizational or shared-agent memory without separate requirements, privacy review and ADRs.
11. Do not add a second agent, concurrency, delegation, MCP/A2A or shared memory without a separate value/risk decision.

## M. Required input for the next stage

Use all ten `1.2.0` artefacts; `ADR-001`–`043`; `AGT-001-spec 1.1.0`; `GRAPH-001 1.1.0`; `DATA-007`, `DATA-009`, `DATA-041`–`086`; `INT-009`–`058`; `TOOL-001`–`006`; the S04C harness contracts; `DATA-077` context policy; `MEM-POL-001`; S05B code/tests/evaluations/benchmark; cumulative/focused diagrams; and all active risks/issues.

## N. Next architectural problem

The single agent can now resume long investigations with bounded, provenance-preserving context and optional case-local continuity memory. However, `AGT-001` still spans regulatory research, obligation extraction, policy/control mapping, risk assessment, verification and report generation. NorthStar has not determined whether this complexity is best handled by one agent with specialized graph nodes, multiple prompts, or multiple bounded agents. Adding agents prematurely would introduce delegation, handoff, private/shared state, memory, identity, termination, coordination, latency, cost and error-propagation risks.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 6A — Single-Agent versus Multi-Agent Architecture Decision and Agent Boundary Analysis**. Reconstruct the `1.2.0` S05B baseline; preserve `AGT-001-spec 1.1.0`, `GRAPH-001 1.1.0`, gateway/external-approval semantics and the case-local memory boundary. Compare one agent with tools, specialized graph nodes and multiple bounded agents; add no new agent unless the requirements and measured trade-offs justify it; update all artefacts, execute tests/audit and stop before interoperability or concurrency implementation.
