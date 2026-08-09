# Stage Handoff Pack

## A. Stage completed
- **Stage identifier:** `S06A`
- **Stage title:** Single-Agent versus Multi-Agent Architecture Decision and Agent Boundary Analysis
- **Architecture version:** `1.3.0`
- **Repository version:** `1.3.0`
- **Handoff version:** `1.3.0`
- **Completion date:** 2026-08-01
- **Status:** Completed within local/offline deterministic architecture-decision and profile-validation boundaries.
- **Consistency audit:** Passed with recorded reconstruction and production exceptions.

## B. Capabilities now available

1. All accepted S05B one-agent/specification/graph/harness/gateway/budget/recovery/durable-wait/external-approval/context/memory controls remain.
2. `INT-059` deterministically compares six architecture options.
3. `DATA-088` records selection, eligibility, reasons, coordination/authority surfaces, limitations and digest.
4. NorthStar selects one `AGT-001` with specialized `GRAPH-001` work units and six bounded profiles.
5. `INT-060` rejects unknown agents/graphs/tools and prohibited future capabilities.
6. `INT-061` binds profile/node/run/spec/graph with hashes and unchanged control owners.
7. `INT-062` is a deny-by-default future architecture-review gate; it cannot allocate or authorize an agent.
8. Verification is a separate profile/evaluation surface, not a second agent or approver.
9. Multi-agent review requires an independent boundary or representative measured gain after single-agent remedies.
10. `TEST-243`–`270` and `EVAL-055`–`061` pass locally.

Not implemented: second agent, delegation, handoff, task/message envelope, attenuated agent identity/token, private/shared agent state, shared-agent memory, concurrent branches/workers, MCP/A2A, live model/connectors, production IAM/PDP/KMS/database/audit/WORM/control plane/deployment/DR.

## C. Accepted architecture decisions
`ADR-001`–`043` remain accepted.
- `ADR-044`: retain one agent and specialize the graph through bounded profiles.
- `ADR-045`: evidence verification is a separately evaluated profile/node, not a second agent.
- `ADR-046`: independent-boundary or representative measured-value evidence is required before controlled promotion review.

## D. Current component inventory
| ID | Name | Current S06A responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Starts/resumes cases and surfaces decision/profile evidence. |
| `CMP-002` | Regulatory Intake Boundary | Unchanged provenance boundary. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Owns graph/state/routes/termination and profile validation/binding. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Unchanged authorized evidence. |
| `CMP-005` | Enterprise Integration Boundary | Unchanged gateway-only `TOOL-001`–`006`. |
| `CMP-006` | Human Review and Approval Boundary | Unchanged external typed decision authority. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Unchanged runtime authority owner. |
| `CMP-008` | Evaluation and Assurance Boundary | Boundary/profile/counterfactual evaluations. |
| `CMP-009` | Observability and Audit Boundary | Local assessment/binding evidence; not audit/WORM. |
| `CMP-010` | Runtime and Deployment Boundary | Local sequential Python. |
| `CMP-011` | Source-of-Truth Governance Pack | Governance at `1.3.0`. |

## E. Current agent inventory
| ID | Name | Authority | Status |
|---|---|---|---|
| `AGT-001` | Regulatory Impact Assessment Agent | May propose exact `TOOL-001`–`006` through `CMP-005`, complete or escalate. Cannot route, mutate protected state, approve/finalize, grant consent, write memory, delegate, hand off, create agents, run concurrent branches or recall across cases. | **Only agent**; `AGT-001-spec 1.1.0`; six profiles. |

## F. Current data and state objects
- `DATA-001`–`086` retained; `DATA-009` remains `1.1.0`.
- New: `DATA-087 AgentBoundaryQuestionnaire`, `DATA-088 AgentBoundaryAssessment`, `DATA-089 TaskProfileSet`, `DATA-090 TaskProfileBinding`.
- `DATA-081 case_working` remains the only optional memory; profiles see it only through harness context.
- No delegated task, message, handoff, agent card, private/shared agent state or shared-agent memory object exists.

## G. Current interfaces and tools
- `INT-001`–`058` retained.
- `INT-059` Agent Boundary Assessment.
- `INT-060` Task Profile Load/Validation.
- `INT-061` Task Profile Runtime Binding.
- `INT-062` Future Multi-Agent Capability Gate.
- `TOOL-001`–`003` remain read-only; `TOOL-004`–`006` remain reversible unapproved writes; all gateway-only.

## H. Repository state
```text
northstar-agentic-compliance/
├── config/{agents,architecture,evaluation,prompts}/
├── docs/{adr,architecture/diagrams,baseline,references,source-of-truth,stages}/
├── schemas/DATA-087...DATA-090*.schema.json
├── scripts/{run_stage6a_demo,run_stage6a_evaluation,benchmark_stage6a,validate_stage6a,consistency_audit_stage6a}.py
├── src/northstar_compliance/architecture_decision/{canonical,models,policy,assessment,profiles,binding,report}.py
├── tests/{unit,evaluation}/
├── README.md
└── pyproject.toml
```
Python target `>=3.11,<3.15`; executed `3.13.5`; standard-library runtime; pytest `9.0.2`.

## I. Tests completed
- `TEST-243`–`255`: compatibility, deterministic selection and promotion counterfactuals — passed.
- `TEST-256`–`269`: profile identity/tools/capability denial/digests/bindings and malicious-profile rejection — passed.
- `TEST-270`: evaluation IDs and one-agent gate — passed.
- Additional configuration security check — passed.

Executed result: **29 pytest checks passed**. Compilation, demo, seven evaluations, local microbenchmark, structural validation and consistency audit passed.

- `EVAL-055`: deterministic one-agent/profile selection.
- `EVAL-056`: six-profile coverage and one-agent inventory.
- `EVAL-057`: authority/delegation/handoff/memory/concurrency invariants.
- `EVAL-058`: hard-boundary and representative-measured counterfactual triggers.
- `EVAL-059`: coordination/failure-surface evidence.
- `EVAL-060`: deterministic digests.
- `EVAL-061`: current promotion denied and agent count one.

## J. Known limitations
Compatible reconstruction overlay; no live model/profile quality benchmark; no multi-agent implementation/comparison; design scores/thresholds are tutorial parameters; synthetic local identity/tools; same-agent verification may correlate errors; unsigned config/digests; no production SLO/cost/workload/human benchmark; Mermaid not CLI-rendered; no interoperability, production control plane, deployment, audit/WORM or DR.

## K. Open risks, assumptions and issues
- New risks: `RSK-129`–`143`.
- New assumptions: `ASM-044`–`047`.
- New issues: `ISS-065`–`071`.
- All inherited active production gaps remain.

## L. Compatibility constraints
1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`, `GRAPH-001 1.1.0`, `DATA-009 1.1.0`, application-owned routes/state/termination and sequential branches.
3. Preserve gateway-only `TOOL-001`–`006`, access-before-load, budgets/recovery/reconciliation and `TOOL-006` effect/idempotency.
4. Preserve external human role/SoD/expiry/single-use decisions; timeout never approves and late decisions fail closed.
5. Approved/rejected remain preliminary human-reviewed dispositions, not final closure.
6. Preserve manifest/instruction/context/session/specification/profile digests and fail closed on incompatibility.
7. Profiles cannot grant authority, route/mutate state, approve/finalize, write memory, delegate, hand off or create concurrency.
8. Memory remains optional, case-local, consented, provenance-bound, expiring/deletable and harness-owned.
9. `INT-062` is a design-review gate, not allocator/PDP.
10. Do not add `AGT-002`, delegation, handoff, shared-agent memory, MCP/A2A or concurrent branches without new requirements, threat/privacy review, ADRs, schemas, implementation and evaluation.

## M. Required input for the next stage
Use all ten `1.3.0` artefacts; `ADR-001`–`046`; `AGT-001-spec 1.1.0`; `GRAPH-001 1.1.0`; `DATA-007`, `DATA-009`, `DATA-041`–`090`; `INT-009`–`062`; `TOOL-001`–`006`; S04C harness contracts; `DATA-077`; `MEM-POL-001`; S05B context/memory code; S06A code/tests/evaluations/benchmark; diagrams; and active risks/issues.

## N. Next architectural problem
If a future independent boundary or representative evaluation justifies specialists, NorthStar lacks typed delegation/handoff, attenuated authority, agent/task identity, shared-versus-private state/context rules, artefact authenticity, timeout/cancellation/error propagation and system-level termination. These contracts must precede protocol selection or concurrency.

## O. Exact continuation instruction
> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 6B — Bounded Agent Handoff, Communication and Authority Contracts**. Reconstruct the `1.3.0` S06A baseline; preserve the current one-agent runtime and all gateway/human/memory constraints; design typed future handoff and attenuated-authority contracts without enabling concurrent execution or selecting MCP/A2A prematurely; update all artefacts, execute tests/audit and stop after the stage.
