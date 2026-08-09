# Stage Handoff Pack

## A. Stage completed

- Stage identifier: `S09A`
- Stage title: Threat Modelling
- Architecture version: `1.12.0`
- Repository version: `1.12.0`
- Handoff version: `1.12.0`
- Graph version: `GRAPH-001/1.8.0`
- Threat-model version: `TM-001/1.0.0`
- Completion date: 2026-08-01
- Status: completed as a compatible, provider-neutral, design-time threat-modelling overlay; no production security certification, identity deployment, model route, deployment gate or runtime control activation.
- Consistency audit: passed with recorded exceptions.

## B. Capabilities now available

1. All S08A-S08C dataset, evaluator, judge, bias, authority, state, memory, cache, concurrency and human-control constraints remain.
2. `DATA-165`-`176` define the architecture snapshot, trust boundaries, data flows, actors, threats, STRIDE assessments, attack trees, misuse cases, control mappings, ordinal risk assessments, reports and advisory treatments.
3. `INT-130`-`139` define snapshot loading, boundary/asset/actor registration, flow validation, STRIDE/OWASP crosswalks, attack-tree and misuse-case validation, ordinal prioritization, control/test mapping, reporting and advisory export.
4. `TM-001/1.0.0` models 8 trust boundaries, 12 assets, 20 data flows, 8 actor classes and 36 threat scenarios: 28 current and 8 explicitly inactive-future.
5. Every threat maps to system-specific assets/flows, one or more STRIDE classes, an OWASP Agentic Top 10 category, preventive/detective/response controls, risk factors and tests.
6. Three attack trees cover restricted-data exfiltration, unauthorized action and corruption of the assessment/forensic record.
7. Six misuse cases exercise indirect prompt injection, confused-deputy abuse, memory poisoning, duplicate side effects, judge manipulation and future inter-agent spoofing.
8. Hard authority, approval, tenant-isolation, code-execution and mandatory-gate failures remain non-overridable; no aggregate risk score can compensate for them.
9. The threat model and all recommendations have `authority_effect: none` and cannot mutate `DATA-106`, activate a route, approve/finalize, create agents or deploy controls.
10. 62 pytest cases, `EVAL-169`-`184` (16/16), validation, compilation, threat-model execution and consistency audit pass.
11. Stage 8D metrics/regression/deployment gates remain unresolved and are not retroactively claimed.

## C. Accepted architecture decisions

`ADR-001`-`088` remain accepted. New:

- `ADR-089`: execute explicitly requested S09A before unresolved S08D, record the divergence and preserve S08D as open.
- `ADR-090`: combine DFD/trust-boundary analysis and STRIDE with OWASP agentic crosswalks, attack trees and misuse cases.
- `ADR-091`: version and digest an immutable architecture snapshot before generating threat evidence.
- `ADR-092`: use transparent ordinal likelihood/impact factors for prioritization, not false probability or a universal security score.
- `ADR-093`: model the implemented single-agent architecture separately from inactive future MCP/A2A/multi-agent surfaces.
- `ADR-094`: keep treatment recommendations advisory and subject to external security/governance change control.

## D. Current component inventory

| ID | Name | Current responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | User/session entry point; input and output trust boundary. |
| `CMP-002` | Regulatory Intake Boundary | Validates publication envelopes; source text remains untrusted data. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole task, route, protected-state, admission, cancellation, aggregation and system-termination owner. |
| `CMP-004` | Knowledge and Evidence Access Boundary | Access-aware evidence retrieval and provenance. |
| `CMP-005` | Enterprise Integration Boundary | Only gateway to `TOOL-001`-`006`; typed validation and side-effect controls. |
| `CMP-006` | Human Review and Approval Boundary | Human review, approval and finalization remain external. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole authority issuer; production identity/token implementation remains open. |
| `CMP-008` | Evaluation and Assurance Boundary | Owns `TM-001`, STRIDE/crosswalk analysis, attack trees, misuse cases and advisory treatment evidence. |
| `CMP-009` | Observability and Audit Boundary | Receives minimized threat/evaluation evidence; no WORM claim. |
| `CMP-010` | Runtime and Deployment Boundary | Preserves bounded runtime, queue and checkpoint constraints; no new deployment route. |
| `CMP-011` | Source-of-Truth Governance Pack | Governs `1.12.0`, architecture snapshot, risk register, ADRs and compatibility. |

## E. Current agent inventory

- `AGT-001 Regulatory Impact Assessment Agent`, specification `1.1.0`, remains the **only active agent**.
- It retains bounded proposal/complete/escalate behaviour and cannot route, mutate protected state, grant authority, approve/finalize, deploy controls or change threat-treatment status.
- No threat modeller, STRIDE engine, attack tree, evaluator, MCP peer or A2A peer is an agent.
- `WP-008` remains `inactive_future`.

## F. Current data and state objects

- Preserve `DATA-001`-`164`; `DATA-009` remains `1.1.0`.
- Add `DATA-165`-`176` as listed in capability B.
- All S09A objects are design-time assurance objects with `authority_effect: none`.
- No protected-state, approval, route, shared-memory, grant, credential or deployment writer is added.

## G. Current interfaces and tools

- Preserve `INT-001`-`129` and `TOOL-001`-`006`.
- Add `INT-130`-`139`.
- The threat-model engine is not a tool gateway and receives no enterprise credentials, customer data, network access or runtime mutation capability.

## H. Repository state

```text
northstar-agentic-compliance-stage9a-threat-model/
├── config/threat_model/
│   ├── architecture_snapshot.json
│   ├── actors.json
│   ├── risk_policy.json
│   ├── threat_catalogue.json
│   ├── attack_trees.json
│   └── misuse_cases.json
├── docs/
│   ├── adr/ADR-089..094-*.md
│   ├── architecture/diagrams/*.mmd
│   ├── references/stage9a-primary-sources.md
│   ├── source-of-truth/00..09-*.md
│   └── stages/NorthStar-Stage-9A-Threat-Modelling.md
├── reports/
├── schemas/DATA-165..176.schema.json
├── scripts/
├── src/northstar_compliance/security/threat_model/
├── tests/{unit,integration,security,performance}/
├── README.md
└── pyproject.toml
```

Entry points: `validate_stage9a.py`, `run_stage9a_threat_model.py`, `run_stage9a_evaluation_gates.py`, `consistency_audit_stage9a.py`.

## I. Tests completed

- `TEST-685`-`699`: schemas, versions, canonical digests, boundaries, flows, actors and catalogue integrity - passed.
- `TEST-700`-`712`: STRIDE, OWASP ASI coverage, attack trees, misuse cases and report generation - passed.
- `TEST-713`-`731`: authority, injection, tenant, tool, MCP/A2A, memory, replay, judge, supply-chain and future-scope security assertions - passed.
- `TEST-732`-`736`: bounded local execution and deterministic report properties - passed.
- `EVAL-169`-`184`: 16/16 passed.
- Executed: 62 pytest cases passed.

## J. Known limitations

No byte-exact historical merge, Stage 8D deployment gates, production identity/token service, workload identity, mTLS/proof-of-possession, signed messages, enterprise secrets management, WORM ledger, adaptive red team, live MCP/A2A endpoint, browser/computer-use runtime, sandbox certification, production telemetry, quantitative loss model, independent security assessment or legal/regulatory conclusion.

## K. Open risks, assumptions and issues

- Preserve inherited risks/issues, including `ISS-096`, `ISS-114`-`139` where still applicable.
- New threat risks: `RSK-310`-`345`.
- New assumptions: `ASM-105`-`110`.
- New issues: `ISS-140`-`146`.
- Highest current residual priorities include indirect prompt injection, retrieval/tool poisoning, confused-deputy abuse, cross-tenant leakage, supply-chain compromise, evidence cascades, reviewer trust exploitation and approval forgery.

## L. Compatibility constraints

1. Preserve NorthStar, all eight personas, `US-001`-`012`, `CMP-001`-`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`, `DATA-009 1.1.0`, `GRAPH-001/1.8.0` and all canonical contracts.
3. Preserve `DATA-091`-`176`, `INT-063`-`139` and `TOOL-001`-`006` after merge.
4. `CMP-003` remains the sole task/route/protected-state/admission/cancellation/aggregation/system-termination owner.
5. `CMP-005` remains the only tool gateway; `CMP-007` remains the only authority issuer.
6. Humans remain approval/finalization owners; timeout never approves.
7. Deterministic mandatory failures and critical injection/contamination/authority failures cannot be averaged, voted or thresholded away.
8. Threat/evaluation results cannot mutate `DATA-106`, grant authority, approve/finalize, create agents, activate routes or deploy controls.
9. `WP-008`, MCP/A2A runtime and additional agents remain inactive unless a later accepted ADR explicitly activates them.
10. Stage 8A sealed controls, S08B judge contracts and S08C bias-lab controls remain.
11. Semantic regulatory-answer caching remains prohibited.
12. No unrestricted user credential or token passthrough to a tool, proxy or future MCP server.
13. Current and future threat scopes must remain labelled separately.
14. Any material component, flow, protocol, tool, model, memory, authority or deployment change requires a new architecture snapshot and threat-model review.
15. Resolve/merge `ISS-096`, `ISS-131` and `ISS-141` before claiming a complete byte-exact historical register.
16. Stage 8D remains unresolved; S09A does not establish promotion eligibility.

## M. Required input for the next stage

Use the merged `1.12.0` overlays; `ADR-001`-`094`; `AGT-001-spec 1.1.0`; `GRAPH-001/1.8.0`; `DATA-131`-`176`; `INT-103`-`139`; `TM-001/1.0.0`; the S08A dataset controls, S08B judge contracts, S08C bias laboratory, S09A threat catalogue/attack trees/misuse cases, and all active risks/issues. Preserve unresolved S08D requirements explicitly.

## N. Next architectural problem

The threat model identifies authority confusion, token replay, audience mismatch, confused-deputy behaviour, workload impersonation, approval forgery and cross-tenant disclosure as high-consequence paths. NorthStar has accepted ownership boundaries, but it still lacks a production-grade identity and delegated-authorization design that binds a human, `AGT-001`, workload, intended tool, operation, resource/data scope, risk tier, approval, audience, nonce, expiry, use count and delegation depth. It also lacks proof-of-possession, revocation and receiver-side enforcement semantics.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 9B - Agent Identity and Tokenized Authorization**. Reconstruct the `1.12.0` S09A baseline; preserve exactly one active `AGT-001`, `GRAPH-001/1.8.0`, all current authority owners, gateway-only tools, human approval/finalization, sealed evaluation controls, non-overridable mandatory failures, inactive `WP-008`/MCP/A2A/multi-agent routes and unresolved Stage 8D gates. Design human, agent, workload, service and tool identity; delegated on-behalf-of authority; short-lived audience-bound attenuated grants; token exchange; nonce/expiry/use/delegation limits; proof-of-possession and revocation; receiver-side policy enforcement; negative authorization tests and threat-model updates. Update all artefacts, run the consistency audit and stop before blast-radius controls, guardrail architecture or control-plane implementation.

Audit assertions: exactly one active `AGT-001`; no unrestricted credential/token passthrough; no concurrent protected-state writes; no automatic `DATA-106` mutation; humans own approval/finalization; all S09B recommendations remain non-authoritative until implemented and accepted; no model or production route activated.
