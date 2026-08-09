# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S06B`
- **Stage title:** Bounded Agent Handoff, Communication and Authority Contracts
- **Architecture version:** `1.4.0`
- **Repository version:** `1.4.0`
- **Handoff version:** `1.4.0`
- **Completion date:** 2026-08-01
- **Status:** Completed within local/offline deterministic contract-sandbox boundaries.
- **Consistency audit:** Passed with recorded reconstruction and production exceptions.

## B. Capabilities now available

1. All accepted S06A one-agent/profile/graph/harness/gateway/budget/recovery/human/memory controls remain.
2. `DATA-091` describes exact active and candidate endpoint powers/status.
3. `DATA-092` provides canonical signed task/message envelopes with trace/correlation/causation identity, case/run/task binding, deadlines, goal/non-goals, artefacts, expected output and grant binding.
4. `DATA-093` provides short-lived, audience/case/run/task/resource/data-scope-bound authority that can only be attenuated.
5. Local replay/use/revocation checks and authorization-before-load are implemented.
6. `DATA-095` provides immutable hashed, provenance-bearing, case/subject-scoped artefact manifests.
7. `DATA-094` binds receipt to exact envelope, grant and artefacts.
8. `DATA-097` implements deterministic offered/accepted/running/terminal lifecycle events.
9. `DATA-098` defines typed safe failure propagation.
10. `DATA-099` defines system-termination evidence while preserving human/final-closure ownership.
11. `INT-063`–`070` define validation, authority, offer/receipt, artefact, status, cancellation/failure, sandbox and termination contracts.
12. A sequential two-party deterministic sandbox executes evidence verification across `AGT-001` and a candidate endpoint.
13. The candidate endpoint has no tools, memory write, routing, delegation, approval, finalization or concurrency authority.
14. `TEST-271`–`306` and `EVAL-062`–`069` pass locally.

**Not implemented:** a second active agent/`AGT-002`, autonomous recipient model loop, peer delegation, shared mutable state, shared-agent memory, concurrent execution, REST/gRPC/queue/event bus, MCP/A2A, live IAM/PDP/KMS/DPoP/mTLS, live model/connectors, production database/replay ledger, audit/WORM, control plane, deployment or DR.

## C. Accepted architecture decisions

`ADR-001`–`046` remain accepted.

- `ADR-047`: define protocol-neutral handoff contracts before transport/protocol selection.
- `ADR-048`: issue strictly attenuated authority from `CMP-007` and verify it at the recipient/resource boundary before data load/action.
- `ADR-049`: keep handoffs orchestrator-mediated, one-hop, one-attempt and sequential; no peer delegation or concurrency.
- `ADR-050`: keep state private/owned and exchange immutable artefacts; no shared mutable state or shared-agent memory.

`ADR-044`–`046` are not superseded; one active agent and evidence-gated promotion remain.

## D. Current component inventory

| ID | Name | Current S06B responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Starts/resumes cases and surfaces preliminary handoff evidence. |
| `CMP-002` | Regulatory Intake Boundary | Unchanged provenance boundary. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Owns task creation, envelope, route/state, lifecycle, cancellation, aggregation and termination. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Unchanged authorized evidence. |
| `CMP-005` | Enterprise Integration Boundary | Unchanged gateway-only `TOOL-001`–`006`; no candidate bypass. |
| `CMP-006` | Human Review and Approval Boundary | Unchanged external typed human authority. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Owns grant issue/attenuation/verification/revocation semantics. |
| `CMP-008` | Evaluation and Assurance Boundary | Handoff/authority/integrity/one-agent evaluations. |
| `CMP-009` | Observability and Audit Boundary | Local receipts/status evidence only; not audit/WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Local sequential Python contract sandbox. |
| `CMP-011` | Source-of-Truth Governance Pack | Governance at `1.4.0`; active/candidate status and disabled flags. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing exact `TOOL-001`–`006` gateway-only proposal/complete/escalate boundary. Cannot route/mutate protected state, approve/finalize, grant consent, write memory, create agents, run concurrent branches or bypass control owners. | **Only active agent**; spec `1.1.0`; six profiles. |

### Candidate endpoint inventory

| Endpoint ID | Name | Authority | Status |
|---|---|---|---|
| `CAND-EVIDENCE-VERIFIER-001` | Candidate Evidence Verification Endpoint | Verify one supplied immutable evidence artefact under one-use grant; no tools, memory, route, delegation, approval, finalization or concurrency. | `candidate_sandbox_only`; not an `AGT-*` allocation. |

## F. Current data and state objects

- `DATA-001`–`090` retained; `DATA-009` remains `1.1.0`.
- New: `DATA-091 AgentEndpointDescriptor`.
- New: `DATA-092 DelegatedTaskEnvelope`.
- New: `DATA-093 AttenuatedAuthorityGrant`.
- New: `DATA-094 HandoffReceipt`.
- New: `DATA-095 HandoffArtifactManifest`.
- New: `DATA-096 VerificationResultArtifact` (`not_an_approval`).
- New: `DATA-097 HandoffStatusEvent`.
- New: `DATA-098 HandoffFailureEnvelope`.
- New: `DATA-099 HandoffTerminationRecord`.
- `DATA-081 case_working` remains optional harness-owned memory and is not automatically transferred.
- No shared mutable state, blackboard, shared-agent memory or candidate state writer exists.

## G. Current interfaces and tools

- `INT-001`–`062` retained.
- `INT-063` Endpoint and Handoff Contract Validation.
- `INT-064` Authority Mint, Attenuate and Verify.
- `INT-065` Task Offer and Receipt.
- `INT-066` Immutable Artefact Exchange.
- `INT-067` Status and Progress.
- `INT-068` Timeout, Cancellation and Failure Propagation.
- `INT-069` Sequential Handoff Contract Sandbox.
- `INT-070` System Termination Decision.
- `TOOL-001`–`003` remain read-only; `TOOL-004`–`006` remain reversible unapproved writes; all remain gateway-only.

## H. Repository state

```text
northstar-agentic-compliance-stage6b/
├── config/{agents,architecture,evaluation}/
├── docs/{adr,architecture/diagrams,baseline,references,source-of-truth,stages}/
├── schemas/DATA-091...DATA-099*.schema.json
├── scripts/{run_stage6b_demo,run_stage6b_evaluation,benchmark_stage6b,validate_stage6b,consistency_audit_stage6b}.py
├── src/northstar_compliance/handoff/{canonical,models,policy,authority,envelopes,artifacts,lifecycle,simulator,fixtures}.py
├── tests/{unit,integration,security,evaluation}/
├── reports/
├── README.md
└── pyproject.toml
```

Python target `>=3.11,<3.15`; executed `3.13.5`; runtime standard library; pytest `9.0.2`.

Primary entry points:

- `scripts/run_stage6b_demo.py`
- `scripts/run_stage6b_evaluation.py`
- `scripts/benchmark_stage6b.py`
- `scripts/validate_stage6b.py`
- `scripts/consistency_audit_stage6b.py`

## I. Tests completed

- `TEST-271`–`280`: grant verification, attenuation, scope/expiry/depth, signature/audience, replay/use and revocation — passed.
- `TEST-281`–`290`: envelope/receipt signatures, tamper, endpoint/expiry, artefact scope/integrity/immutability — passed.
- `TEST-291`–`297`: lifecycle transitions, terminal immutability, timeout, cancellation, duplicates and termination readiness — passed.
- `TEST-298`–`300`: sequential sandbox, candidate non-activation and authority denials — passed.
- `TEST-301`–`305`: one active agent, no protocol/concurrency/shared state/memory, minimized payload and binding — passed.
- `TEST-306`: evaluation IDs and deterministic fixture digest — passed.

Executed result: **36 tests passed in 0.14 seconds**.

Evaluations:

- `EVAL-062`: one active agent / candidate-only endpoint.
- `EVAL-063`: strict attenuation and zero candidate tools.
- `EVAL-064`: envelope/grant digest binding.
- `EVAL-065`: immutable artefact requirement.
- `EVAL-066`: memory/tool boundary denial.
- `EVAL-067`: one-hop/one-attempt bounded lifecycle.
- `EVAL-068`: contract-sandbox-only runtime.
- `EVAL-069`: no route/approval/finalization/concurrency authority.

Compilation, demo, eight evaluations, local microbenchmark, structural validation and consistency audit passed.

## J. Known limitations

Compatible reconstruction overlay; candidate deterministic rather than model-based; no evidence to allocate `AGT-002`; local HMAC/shared secrets; no production identity/token exchange/proof-of-possession/KMS/trusted clock; in-memory use/revocation/artifact stores; no protocol adapter; no distributed delivery/dedup/order; no concurrency; no live model/connectors; no multi-agent quality/cost benchmark; no production SLO/load/human benchmark; Mermaid not CLI-rendered; no audit/WORM/control plane/deployment/DR/legal sufficiency claim.

## K. Open risks, assumptions and issues

- New risks: `RSK-144`–`160`.
- New assumptions: `ASM-048`–`052`.
- New issues: `ISS-072`–`079`.
- All inherited active production gaps remain.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one active `AGT-001` until promotion is evidence/ADR controlled.
2. Preserve `AGT-001-spec 1.1.0`, `GRAPH-001 1.1.0`, `DATA-009 1.1.0`, application-owned routes/state/termination and sequential execution.
3. Preserve gateway-only `TOOL-001`–`006`, access-before-load, budgets/recovery/reconciliation and `TOOL-006` effect/idempotency.
4. Preserve external human role/SoD/expiry/single-use decisions; timeout never approves and late decisions fail closed.
5. Approved/rejected remain preliminary human-reviewed dispositions, not final closure.
6. Preserve manifest/instruction/context/session/specification/profile digests and fail closed on incompatibility.
7. Profiles/candidate endpoints cannot grant authority, route/mutate state, approve/finalize, write memory, create agents or create concurrency.
8. Memory remains optional, case-local, consented, provenance-bound, expiring/deletable and harness-owned; no automatic handoff transfer.
9. `INT-062` remains a design-review gate, not an allocator/PDP.
10. `CMP-007` is the only delegated-authority issuer; child scope can only narrow.
11. Recipient/resource enforcement must occur before data load/action.
12. `CMP-003` remains the sole handoff lifecycle and system-termination owner.
13. Handoffs exchange immutable `DATA-095` artefacts and receipts, not shared mutable state.
14. Do not claim local HMAC objects are production OAuth/DPoP/macaroons/non-repudiation.
15. Do not select MCP/A2A/REST/gRPC/queue/event bus or enable concurrency without S06C/S06D ADRs, adapters and conformance/evaluation evidence.

## M. Required input for the next stage

Use all ten `1.4.0` artefacts; `ADR-001`–`050`; `AGT-001-spec 1.1.0`; `GRAPH-001 1.1.0`; `DATA-007`, `DATA-009`, `DATA-041`–`099`; `INT-009`–`070`; `TOOL-001`–`006`; `HOF-POL-001`; S04C harness contracts; `DATA-077`; `MEM-POL-001`; S05B context/memory code; S06A decision/profile code; S06B handoff/authority/artefact/lifecycle code and tests; diagrams; benchmark/evaluation reports; active risks/issues.

## N. Next architectural problem

The canonical handoff semantics are now explicit, but no communication mechanism carries them across a real boundary. NorthStar must compare direct calls, REST, gRPC, message queues/event buses, framework-native handoffs, MCP and agent-to-agent task protocols; distinguish tool/resource interoperability from agent task lifecycle; define discovery/authentication/version negotiation; and build adapter conformance tests proving that authority, deadlines, cancellation, artefact integrity, correlation and termination semantics are not lost. Concurrency must still remain separate until communication is selected and validated.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 6C — Agent Communication, Interoperability and Protocol Mapping**. Reconstruct the `1.4.0` S06B baseline; preserve exactly one active `AGT-001`, all graph/state/gateway/human/memory owners and the canonical `DATA-091`–`099`/`INT-063`–`070` contracts; compare and map direct calls, REST, gRPC, queues/event buses, framework handoffs, MCP and agent-to-agent task protocols; select only the minimum justified adapter architecture, add conformance/security/evaluation tests, do not enable concurrent execution, update all artefacts, run the consistency audit and stop after the stage.
