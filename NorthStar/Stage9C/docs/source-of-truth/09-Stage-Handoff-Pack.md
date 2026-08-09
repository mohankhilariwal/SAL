# Stage Handoff Pack

## A. Stage completed

- Stage identifier: `S09C`
- Stage title: Guardrails, Governance and Control Plane
- Architecture version: `1.14.0`
- Repository version: `1.14.0`
- Handoff version: `1.14.0`
- Graph version: `GRAPH-001/1.10.0`
- Threat-model version: `TM-001/1.2.0`
- Authorization-model version: `AUTH-001/1.0.0` unchanged
- Blast-radius-model version: `BR-001/1.0.0` unchanged
- Guardrail-model version: `GR-001/1.0.0`
- Governance-model version: `GOV-001/1.0.0`
- Control-plane profile: `CP-001/0.1.0` bounded local reference
- Completion date: 2026-08-01
- Status: completed as a provider-neutral architecture and executable local reference; no full production control plane, production policy service, certification, route or Stage 8D promotion eligibility.
- Consistency audit: passed with recorded exceptions.

## B. Capabilities now available

1. Guardrails cover input, context, retrieval, planning, tool execution/result, output, state, memory, human review and runtime.
2. `GR-BUNDLE-001/1.0.0` contains 59 versioned controls with owner, stage, validator, hard/soft, sync/async, exception and failure-outcome metadata.
3. Hard controls are synchronous and non-overrideable; model-assisted controls are advisory and cannot authorize or approve.
4. Guardrails compose with and do not replace `AUTH-001/1.0.0` and `BR-001/1.0.0`.
5. Guardrail decisions/evidence have `authority_effect: none`.
6. Untrusted source, retrieval and tool-result content cannot become instructions without stage controls.
7. Plans cannot create agents, mutate policy, activate routes or exceed authorized tier.
8. Tool calls remain gateway-only, typed, approval-bound where required and limited to one concurrent protected write.
9. Outputs cannot claim approval/finalization; material claims require evidence and uncertainty handling.
10. State/memory writes are case/tenant/version/idempotency/provenance/retention controlled.
11. Human review is authenticated, role/SoD/digest/expiry bound; timeout never approves.
12. Policy lifecycle supports validate, test, two-human approve, immutable release, distribution receipt, pin, deprecate/retire.
13. Exceptions apply only to soft controls, require two independent approvers, compensating controls and ≤30-day expiry.
14. `CP-001/0.1.0` demonstrates bounded local release/distribution/pinning/status without implementing a full production control plane.
15. Stage 8D production promotion remains blocked.

## C. Accepted architecture decisions

`ADR-001`–`103` remain. New:

- `ADR-104`: execute combined S09C as complete guardrail/governance design plus bounded local control-plane slice; no full production control plane.
- `ADR-105`: stage-specific local PEPs.
- `ADR-106`: deterministic-first; model-assisted advisory only.
- `ADR-107`: hard controls synchronous before protected effect.
- `ADR-108`: immutable pinned bundles and local caches.
- `ADR-109`: soft-only scoped/expiring exceptions.
- `ADR-110`: external digest-bound human accountability.
- `ADR-111`: extend existing components; no new authority owner/agent.
- `ADR-112`: minimized non-authorizing evidence.
- `ADR-113`: local JSON reference; future policy-engine semantic conformance.

## D. Current component inventory

| ID | Name | Current Stage 9C responsibility |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Authenticated case UX and evidence/review presentation. |
| `CMP-002` | Regulatory Intake Boundary | Input guardrails and quarantine. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Sole task/route/protected-state/admission/cancellation/aggregation/termination owner; context/plan/state/memory/runtime PEPs. |
| `CMP-004` | Knowledge and Evidence Access Boundary | AUTH-001 plus retrieval guardrails. |
| `CMP-005` | Enterprise Integration Boundary | Only TOOL-001–006 gateway; AUTH-001, BR-001 and tool/result guardrails. |
| `CMP-006` | Human Review and Approval Boundary | Human identity/role/SoD/digest/expiry controls; humans approve/finalize. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Sole AUTH-001 issuer; owns policy semantics/invariants. |
| `CMP-008` | Evaluation and Assurance Boundary | Policy tests, advisory classifiers and TM-001 delta; no authority. |
| `CMP-009` | Observability and Audit Boundary | Minimized guardrail/release/exception evidence; no WORM claim. |
| `CMP-010` | Runtime and Deployment Boundary | Local verified bundle cache/pin/staleness; no production route. |
| `CMP-011` | Source-of-Truth Governance Pack | Lifecycle, owners, releases, exceptions, incidents and compatibility. |

## E. Current agent inventory

- `AGT-001 Regulatory Impact Assessment Agent`, spec `1.1.0`, remains the **only active agent**.
- It may propose bounded plans/tools/drafts and present existing grants/proofs.
- It cannot alter controls/policy bundles/exceptions, issue/enlarge grants, change BR budgets/tiers, approve/finalize, mutate `DATA-106`, activate routes or create agents.
- No guardrail engine, classifier, policy engine, evaluator or control-plane process is an agent.
- `WP-008`, MCP/A2A peers and additional agents remain `inactive_future`.

## F. Current data and state objects

- Preserve `DATA-001`–`192`; `DATA-009` remains `1.1.0`.
- Add `DATA-193`–`216` for guardrail policies/bundles/requests/decisions/evidence, stage assessments, human review, exceptions, owners, changes, tests, releases, distribution, incidents, snapshots and report.
- Every S09C schema requires `authority_effect: none`.
- `DATA-196` can allow/deny/quarantine/require review for the current stage only; it cannot issue authority, approve/finalize or mutate protected state.

## G. Current interfaces and tools

- Preserve `INT-001`–`154` and `TOOL-001`–`006`.
- Add `INT-155`–`176` for stage guardrails, policy lifecycle, distribution, exceptions, evidence, incidents and consistency.
- `CMP-005` remains the only tool gateway; no `TOOL-007` is introduced.
- Tool tiers remain: `TOOL-001`–`003` tier 1; `TOOL-004`–`005` tier 2; `TOOL-006` tier 3.

## H. Repository state

```text
northstar-agentic-compliance-stage9c-guardrails-control-plane/
├── config/guardrails/
├── docs/{adr,architecture/diagrams,references,source-of-truth,stages,threat-model}/
├── reports/
├── schemas/DATA-193..216.schema.json
├── scripts/
├── src/northstar_compliance/guardrails/
├── tests/{unit,integration,security,performance}/
├── README.md
└── pyproject.toml
```

Entry points: `run_stage9c_demo.py`, `validate_stage9c.py`, `run_stage9c_evaluation_gates.py`, `consistency_audit_stage9c.py`.

## I. Tests completed

- `TEST-793`–`804`: bundle/policy integrity and hard/soft invariants.
- `TEST-805`–`816`: input/context negative matrix.
- `TEST-817`–`826`: retrieval/planning matrix.
- `TEST-827`–`855`: tool/output/state/memory matrix.
- `TEST-856`–`862`: human accountability matrix.
- `TEST-863`–`870`: release, distribution, exceptions and evidence.
- `TEST-871`: local 1,000-evaluation performance guard.
- `TEST-872`–`880`: runtime and architecture invariants.
- `EVAL-205`–`228`: passed through evaluation wrapper.
- Executed locally: **88 pytest cases passed**; 24 schemas and 59 controls validated; demo, evaluation wrapper, compilation and consistency audit passed.

## J. Known limitations

No byte-exact historical merge; no signed/KMS-backed bundles; no distributed registry/release/exception database; no live OPA/Cedar/SaaS adapter; no live calibrated classifier; no live human-review workflow; no WORM audit; no multi-region cache/emergency propagation proof; no full enterprise registries/deployment controls; no active MCP/A2A/multi-agent policy; no Stage 8D gates; no production route or certification.

## K. Open risks, assumptions and issues

- Preserve inherited active items.
- Add `RSK-372`–`401`, `ASM-119`–`126`, `ISS-158`–`169`.
- Highest residual concerns: control coverage/placement, wrong attributes, policy tampering/staleness, model/classifier evasion or drift, exception abuse, reviewer fatigue, PEP bypass, evidence minimization error, administrator compromise and distributed emergency-control delay.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`–`012`, `CMP-001`–`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`, `DATA-009 1.1.0`, `GRAPH-001/1.10.0`, `TM-001/1.2.0`, `AUTH-001/1.0.0`, `BR-001/1.0.0`, `GR-001/1.0.0`, `GOV-001/1.0.0` and bounded `CP-001/0.1.0`.
3. Preserve `DATA-091`–`216`, `INT-063`–`176`, `TOOL-001`–`006`.
4. `CMP-003` remains sole route/protected-state/admission/cancellation/aggregation/termination owner.
5. `CMP-005` remains only tool gateway; `CMP-007` remains sole authority issuer; `CMP-006`/humans own approval/finalization.
6. Guardrail allow is not authorization; `AUTH-001` and `BR-001` remain mandatory.
7. Hard controls remain synchronous/non-overrideable; model-assisted controls cannot authorize/approve or override denial.
8. Human credentials/tokens remain restricted; timeout never approves.
9. Tier 4 has no tools; tier 5 cannot be autonomously granted; one concurrent protected write remains maximum.
10. Policy/evaluation/evidence cannot mutate `DATA-106`, activate routes, create agents or deploy controls.
11. `WP-008`, MCP/A2A and additional agents remain inactive.
12. Stage 8D remains unresolved; production promotion stays denied.
13. `CP-001/0.1.0` is not the full production control plane.
14. Any material policy/control/owner/engine/exception/protocol/deployment change requires snapshot, ADR, threat-model and tests.
15. Future OPA/Cedar/other adapters must pass semantic conformance, not just syntax conversion.
16. Resolve historical merge issues before claiming byte-exact completeness.

## M. Required input for the next stage

Use merged `1.14.0` overlays; `ADR-001`–`113`; `GRAPH-001/1.10.0`; `TM-001/1.2.0`; `AUTH-001/1.0.0`; `BR-001/1.0.0`; `GR-001/1.0.0`; `GOV-001/1.0.0`; `CP-001/0.1.0`; `DATA-165`–`216`; `INT-130`–`176`; S08A–S08C assurance controls; S09A threats; S09B authorization/blast-radius tests; S09C guardrail/lifecycle tests; all active risks/issues; and explicit unresolved S08D.

## N. Next architectural problem

NorthStar now has complete guardrail placement, policy lifecycle, human accountability and a bounded local policy-release/distribution profile. It still lacks the full enterprise Agentic AI control plane: agent/model/prompt/tool/MCP/capability/evaluation/dataset/configuration registries; signed multi-environment configuration; production policy distribution; secrets and compatibility management; deployment and routing controls; cost/runtime controls; trace/audit integration; incident/kill-switch orchestration; highly available multi-region operation; and governed future interoperability. These must be added without centralizing all runtime decisions or moving accepted authority owners.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 9D — Enterprise Agentic AI Control Plane**. Reconstruct the `1.14.0` S09C baseline; preserve exactly one active `AGT-001`, `GRAPH-001/1.10.0`, `TM-001/1.2.0`, `AUTH-001/1.0.0`, `BR-001/1.0.0`, `GR-001/1.0.0`, `GOV-001/1.0.0`, all current component and human authority owners, receiver-side enforcement, gateway-only tools, one concurrent protected write, inactive `WP-008`/MCP/A2A/multi-agent routes and unresolved Stage 8D. Design the full provider-neutral enterprise control plane across design, build, deployment, runtime and post-runtime assurance; include registries, signed configuration and policy distribution, compatibility, secrets, deployment/routing/cost controls, incident/kill-switch operation, high availability and conformance tests; do not activate new agents, protocols, tools or production routes unless separately authorized by an ADR and the unresolved gates.
