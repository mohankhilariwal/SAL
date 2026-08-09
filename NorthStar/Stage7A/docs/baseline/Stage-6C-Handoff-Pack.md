# Stage Handoff Pack

## A. Stage completed

- **Stage identifier:** `S06C`
- **Stage title:** MCP, A2A and Interoperability
- **Architecture version:** `1.5.0`
- **Repository version:** `1.5.0`
- **Handoff version:** `1.5.0`
- **Completion date:** 2026-08-01
- **Status:** Completed within local/offline deterministic reference-boundary and conformance-mapping limits.
- **Consistency audit:** Passed with recorded reconstruction and production exceptions.

## B. Capabilities now available

1. All accepted S06B one-agent/profile/graph/harness/gateway/budget/recovery/human/memory/handoff/authority/artefact/lifecycle controls remain.
2. `DATA-100` defines explicit protocol profiles, semantic domains, versions, bindings, statuses, supported/prohibited features and security targets.
3. `DATA-102` defines expiring capability advertisement without granting authority or allocating an agent.
4. `DATA-103` records exact protocol-version and approved-binding negotiation; silent downgrade fails.
5. `PRF-HTTP-JSON-1` carries the canonical handoff across a separate, synchronous, loopback process and validates at the receiver before content use.
6. `DATA-105` records delivery digests, correlation, terminal status, semantic loss and warnings.
7. MCP 2026-07-28 maps to `CMP-005` tools and immutable resources only; full agent-handoff mapping intentionally fails.
8. A2A 1.0 maps Agent Card, Message/Task, Artifact, status and cancellation with a required NorthStar extension for authority/deadline/causation/approval/termination semantics.
9. `DATA-104` provides adapter conformance and semantic-loss evidence.
10. `TEST-307`–`360` and `EVAL-070`–`078` pass locally.

**Not implemented:** `AGT-002`; autonomous recipient model loop; production MCP/A2A endpoint; gRPC; queue/event bus; framework-native handoff; concurrency; streaming/push; retry/redelivery/ordering/dedupe/backpressure; shared state/memory; live IAM/PDP/KMS/mTLS/OAuth/DPoP; live models/connectors; production database/audit/control plane/deployment/DR.

## C. Accepted architecture decisions

`ADR-001`–`050` remain accepted.

- `ADR-051`: keep canonical NorthStar handoff contracts authoritative above protocol adapters.
- `ADR-052`: use a sequential HTTP/JSON boundary only as the minimum serialized reference, not a production topology.
- `ADR-053`: map MCP 2026-07-28 to tool/resource interoperability through `CMP-005`; no agent-task or case-termination authority.
- `ADR-054`: map A2A 1.0 to candidate agent task lifecycle only with a required NorthStar extension; do not activate an agent.
- `ADR-055`: require exact version and approved binding; defer gRPC, brokers and framework handoffs.

## D. Current component inventory

| ID | Name | Current S06C responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Starts/resumes cases and surfaces preliminary protocol/handoff evidence. |
| `CMP-002` | Regulatory Intake Boundary | Unchanged provenance boundary. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole task/route/state/cancellation/aggregation/system-termination owner; owns canonical-to-adapter invocation. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Authorized evidence; may later expose approved immutable resources. |
| `CMP-005` | Enterprise Integration Boundary | Sole gateway for `TOOL-001`–`006`; MCP mapping terminates here and cannot bypass controls. |
| `CMP-006` | Human Review and Approval Boundary | Unchanged external typed human authority. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole grant issuer; production protocol identity/security target owner. |
| `CMP-008` | Evaluation and Assurance Boundary | Adapter conformance, semantic loss, version and one-agent evaluations. |
| `CMP-009` | Observability and Audit Boundary | Local delivery receipts only; not production audit/WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Local direct and single-threaded HTTP subprocess reference runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Governance at `1.5.0`; protocol profiles and disabled flags. |

## E. Current agent inventory

| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | Existing exact gateway-only proposal/complete/escalate boundary. Cannot route/mutate protected state, approve/finalize, grant consent, write unrestricted memory, create agents, run concurrent branches or bypass owners. | **Only active agent**; spec `1.1.0`; six profiles. |

### Candidate endpoint

| Endpoint ID | Name | Authority | Status |
|---|---|---|---|
| `CAND-EVIDENCE-VERIFIER-001` | Candidate Evidence Verification Endpoint | Verify one supplied immutable evidence artefact under one-use grant; no tools, memory, route, delegation, approval, finalization or concurrency. | `candidate_sandbox_only`; direct/HTTP reference and A2A mapping only; not `AGT-*`. |

## F. Current data and state objects

- `DATA-001`–`099` retained; `DATA-009` remains `1.1.0`.
- New `DATA-100 InteroperabilityProtocolProfile`.
- New `DATA-101 ProtocolBindingManifest`.
- New `DATA-102 CapabilityAdvertisement`.
- New `DATA-103 VersionNegotiationRecord`.
- New `DATA-104 AdapterConformanceRecord`.
- New `DATA-105 TransportDeliveryReceipt`.
- `DATA-081 case_working` is not transferred.
- No shared mutable state, shared-agent memory or protocol-owned state writer exists.

## G. Current interfaces and tools

- `INT-001`–`070` retained.
- `INT-071` Protocol Profile Registry.
- `INT-072` Capability Advertisement and Discovery.
- `INT-073` Version and Binding Negotiation.
- `INT-074` HTTP/JSON Reference Handoff Delivery.
- `INT-075` MCP Tool/Resource Conformance Mapping.
- `INT-076` A2A Task-Lifecycle Conformance Mapping.
- `INT-077` Adapter Conformance and Semantic-Loss Evaluation.
- `INT-078` Protocol Security and Fail-Closed Enforcement.
- `TOOL-001`–`006` remain unchanged and gateway-only.

## H. Repository state

```text
northstar-agentic-compliance-stage6c/
├── config/{agents,architecture,evaluation,protocols}/
├── docs/{adr,architecture/diagrams,baseline,references,source-of-truth,stages}/
├── reports/
├── schemas/DATA-100...DATA-105.schema.json
├── scripts/{run_reference_server,run_stage6c_demo,run_stage6c_evaluation,benchmark_stage6c,validate_stage6c,consistency_audit_stage6c}.py
├── src/northstar_compliance/interoperability/{canonical,models,validation,fixtures,registry,evaluation,server,adapters/}.py
├── tests/{unit,integration,security,evaluation}/
├── README.md
└── pyproject.toml
```

Primary entry points:

- `scripts/run_stage6c_demo.py`
- `scripts/run_stage6c_evaluation.py`
- `scripts/benchmark_stage6c.py`
- `scripts/validate_stage6c.py`
- `scripts/consistency_audit_stage6c.py`

Python target `>=3.11,<3.15`; executed `3.13.5`; runtime standard library; pytest `9.0.2`.

## I. Tests completed

- `TEST-307`–`312`: canonical models/digests — passed.
- `TEST-313`–`321`: grant/envelope/artefact validation — passed.
- `TEST-322`–`329`: profile and exact negotiation — passed.
- `TEST-330`–`335`: MCP mapping/domain separation — passed.
- `TEST-336`–`341`: A2A card/task/status/extension mapping — passed.
- `TEST-342`–`347`: direct and subprocess HTTP reference delivery — passed.
- `TEST-348`–`355`: protocol/header/digest/version/security denials — passed.
- `TEST-356`–`360`: evaluation IDs and one-agent/no-concurrency invariants — passed.

Executed result: **59 pytest cases passed**.

Evaluations `EVAL-070`–`078`: all passed.

Compilation, demo, nine evaluations, microbenchmark, structural validation and consistency audit passed.

## J. Known limitations

Compatible reconstruction overlay; loopback single-threaded HTTP; no TLS/auth; local HMAC; no SDK-level MCP/A2A execution; no signed discovery/card; no production registry/IAM/replay/audit; no gRPC/broker/framework adapter; no concurrency/stream/push/retry; no live model/connectors; no business/SLO/cost benchmark; no production control plane/deployment/DR/legal sufficiency claim; Mermaid not CLI-rendered.

## K. Open risks, assumptions and issues

- New risks: `RSK-161`–`179`.
- New assumptions: `ASM-053`–`057`.
- New issues: `ISS-080`–`087`.
- All inherited active production gaps remain.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one active `AGT-001` until evidence/ADR-controlled promotion.
2. Preserve `AGT-001-spec 1.1.0`, `GRAPH-001 1.1.0`, `DATA-009 1.1.0`, application-owned routes/state/termination and sequential execution.
3. Preserve gateway-only `TOOL-001`–`006`, access-before-load, budgets/recovery/reconciliation and `TOOL-006` semantics.
4. Preserve external human authority; timeout never approves; final closure remains human/business-owned.
5. Preserve S05B memory boundaries and no automatic transfer/shared-agent memory.
6. Preserve `DATA-091`–`099` and `INT-063`–`070` as canonical handoff semantics above protocols.
7. `CMP-007` remains the only delegated-authority issuer; adapters/cards/metadata cannot grant authority.
8. `CMP-003` remains the sole task lifecycle, route, cancellation and system-termination owner.
9. Capability advertisement is not authorization or agent allocation.
10. Require exact approved version/binding and record `DATA-103`; no silent downgrade.
11. MCP maps to tools/resources through `CMP-005`; it does not own agent task/case termination.
12. A2A mapping requires the NorthStar extension for authority/deadline/causation/approval/termination fields.
13. Protocol conformance does not activate `CAND-EVIDENCE-VERIFIER-001` or create `AGT-002`.
14. No concurrency, automatic retry, redelivery, streaming, push, shared state or peer delegation before a later ADR-backed stage.
15. Do not claim the reference HTTP/HMAC implementation is production HTTPS/OAuth/mTLS/non-repudiation.

## M. Required input for the next stage

Use all ten `1.5.0` artefacts; `ADR-001`–`055`; `AGT-001-spec 1.1.0`; `GRAPH-001 1.1.0`; `DATA-007`, `009`, `041`–`105`; `INT-009`–`078`; `TOOL-001`–`006`; S04C harness contracts; `DATA-077`; `MEM-POL-001`; S05B memory code; S06A profile/evidence gate; S06B handoff contracts; S06C protocol profiles, adapters, mappings, diagrams, reports and tests; active risks/issues.

## N. Next architectural problem

NorthStar can preserve canonical semantics across one serialized sequential boundary, but it cannot yet run independent work concurrently or asynchronously. A later stage must decide where parallelism is justified and design worker admission, backpressure, delivery guarantees, idempotency/deduplication, ordering, cancellation races, fan-out/fan-in, failure containment and resumption without changing the accepted authority, state, memory, human or termination owners.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 6D — Concurrency and Distributed Execution**. Reconstruct the `1.5.0` S06C baseline; preserve exactly one active `AGT-001` unless separately justified by the accepted promotion gate; preserve canonical `DATA-091`–`105` and `INT-063`–`078`; introduce concurrency only for independent work; compare sequential, async, worker-pool and broker options; add bounded concurrency, backpressure, idempotency/deduplication, cancellation and failure tests; update all artefacts, run the consistency audit and stop after the stage.


Audit assertions: exactly one active `AGT-001`. Concurrency remains disabled.
