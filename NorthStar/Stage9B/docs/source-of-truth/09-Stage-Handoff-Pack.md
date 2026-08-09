# Stage Handoff Pack

## A. Stage completed

- Stage identifier: `S09B`
- Stage title: Identity, Authorization and Blast-Radius Controls
- Architecture version: `1.13.0`
- Repository version: `1.13.0`
- Handoff version: `1.13.0`
- Graph version: `GRAPH-001/1.9.0`
- Threat-model version: `TM-001/1.1.0`
- Authorization-model version: `AUTH-001/1.0.0`
- Blast-radius-model version: `BR-001/1.0.0`
- Completion date: 2026-08-01
- Status: completed as a provider-neutral architecture and executable local reference; no production IAM, route, certification, broader guardrail architecture, control plane or Stage 8D promotion eligibility.
- Consistency audit: passed with recorded exceptions.

## B. Capabilities now available

1. Human, workload, logical agent, agent-execution, service and tool identity are distinguished.
2. `AGT-001` execution is bound to human, workload, tenant, case, run and task.
3. `CMP-007` can issue local short-lived audience/tool-specific attenuated grants without user-token passthrough.
4. Grants include tool, operation, resource/data, region, authority tier, limits, approval, audience, nonce, expiry, use and delegation fields.
5. Local request proofs bind the grant to a workload key and exact request.
6. Receiver-side PEP logic checks signature, bindings, proof, replay, use, revocation, approval and budget.
7. `BR-001` defines tiers 0-5 and budgets for tools, calls, records, bytes, CAD cost, external messages and concurrent writes.
8. Tier 4 has no current tools and requires dual human control; tier 5 is prohibited autonomously.
9. Authorization and blast-radius results cannot approve/finalize, change routes, mutate `DATA-106`, create agents or deploy controls.
10. Exactly one active `AGT-001` remains; future protocol/multi-agent surfaces remain inactive.
11. Stage 8D remains unresolved.

## C. Accepted architecture decisions

`ADR-001`-`094` remain. Add `ADR-095`-`103` as summarized in section 21.

## D. Current component inventory

`CMP-001`-`011` remain unchanged in name. S09B extends `CMP-003` with run-budget ownership, `CMP-004` with retrieval PEP responsibilities, `CMP-005` with tool PEP/budget reservation, `CMP-006` with transaction-bound approval evidence, `CMP-007` with identity/token/revocation policy, `CMP-008` with S09B evaluation/threat delta, `CMP-009` with minimized authorization evidence and `CMP-011` with version governance.

## E. Current agent inventory

- `AGT-001 Regulatory Impact Assessment Agent`, spec `1.1.0`, is the **only active agent**.
- It can propose a tool call and present a grant/proof.
- It cannot issue/enlarge/revoke grants, change budgets/tiers, approve/finalize, mutate protected state, activate routes or create agents.
- `WP-008`, MCP/A2A peers and additional agents remain `inactive_future`.

## F. Current data and state objects

- Preserve `DATA-001`-`176`; `DATA-009` remains `1.1.0`.
- Add `DATA-177`-`192`.
- Authorization-use, replay, revocation and budget state are security-control state, not protected regulatory-case state.
- `DATA-185`, `188`, `189`, `191`, `192` have `authority_effect: none` beyond current-request allow/deny or bounded reservation.

## G. Current interfaces and tools

- Preserve `INT-001`-`139` and `TOOL-001`-`006`.
- Add `INT-140`-`154`.
- `CMP-005` remains the only tool gateway; all tools retain prior contracts.
- Tool tiers: `TOOL-001`-`003` tier 1, `TOOL-004`-`005` tier 2, `TOOL-006` tier 3.

## H. Repository state

```text
northstar-agentic-compliance-stage9b-identity-blast-radius/
├── config/identity/
├── docs/adr/
├── docs/architecture/diagrams/
├── docs/references/
├── docs/source-of-truth/
├── docs/stages/
├── reports/
├── schemas/DATA-177..192.schema.json
├── scripts/
├── src/northstar_compliance/security/identity/
├── tests/{unit,integration,security}/
├── README.md
└── pyproject.toml
```

Entry points: `run_stage9b_demo.py`, `run_stage9b_evaluation_gates.py`, `validate_stage9b.py`, `consistency_audit_stage9b.py`.

## I. Tests completed

- `TEST-737`-`747`: signing, issuer and attenuation.
- `TEST-748`-`752`: proof-key/request proof.
- `TEST-753`-`771`: full identity/scope negative matrix.
- `TEST-772`-`782`: replay, expiry, revocation, use, tampering and approval.
- `TEST-783`-`792`: blast-radius and architecture invariants.
- `EVAL-185`-`204`: passed through the test/evaluation wrapper.
- Executed locally: **56 pytest cases passed**; `EVAL-185`-`204` passed; demo, validation, compilation and consistency audit passed.

## J. Known limitations

Preserve all limitations in section 24. Most importantly: no production IdP/STS/SPIFFE/KMS/mTLS/DPoP, no distributed ledgers/budgets, no WORM audit, no live approval service, no broader guardrails/control plane and no Stage 8D gates.

## K. Open risks, assumptions and issues

- Preserve inherited risks/issues where applicable.
- Add `RSK-346`-`371`, `ASM-111`-`118`, `ISS-147`-`157`.
- Highest residual concerns: issuer/proof-key compromise, stale revocation, policy/attribute error, distributed budget races, approval integrity, clock skew and enforcement outage.

## L. Compatibility constraints

1. Preserve NorthStar, eight personas, `US-001`-`012`, `CMP-001`-`011` and exactly one active `AGT-001`.
2. Preserve `AGT-001-spec 1.1.0`, `DATA-009 1.1.0`, `GRAPH-001/1.9.0`, `TM-001/1.1.0`, `AUTH-001/1.0.0`, `BR-001/1.0.0`.
3. Preserve `DATA-091`-`192`, `INT-063`-`154`, `TOOL-001`-`006`.
4. `CMP-003` remains sole route/protected-state/admission/cancellation/aggregation/termination owner.
5. `CMP-005` remains only tool gateway; `CMP-007` remains sole issuer.
6. Human tokens/credentials are never passed unrestricted to agents/tools.
7. Every tool request is receiver-authorized; signature alone is insufficient.
8. Humans own approval/finalization; timeout never approves.
9. Tier 4 has no current tools; tier 5 cannot be autonomously granted.
10. One concurrent protected write remains the maximum.
11. Authorization/evaluation cannot mutate `DATA-106` or activate a route.
12. `WP-008`, MCP/A2A and additional agents remain inactive.
13. Stage 8D remains unresolved.
14. Broader guardrail architecture and the agent control plane are not implemented.
15. Any material identity, token, policy, tier, tool, protocol or deployment change requires snapshot/threat-model/ADR/test updates.
16. Resolve historical merge issues before claiming byte-exact completeness.

## M. Required input for the next stage

Use the merged `1.13.0` overlays; `ADR-001`-`103`; `GRAPH-001/1.9.0`; `TM-001/1.1.0`; `AUTH-001/1.0.0`; `BR-001/1.0.0`; `DATA-131`-`192`; `INT-103`-`154`; the S08A-S08C assurance controls; S09A threats; S09B negative authorization tests; and all active risks/issues. Preserve unresolved S08D explicitly.

## N. Next architectural problem

NorthStar can now authenticate and bind principals, delegate constrained rights, verify requests at receivers and cap action volume/scope. It still lacks a complete guardrail architecture across input, context, retrieval, planning, tools, output, state, memory and human approval, plus governed policy lifecycle, exceptions, ownership and evidence. Those controls must be designed without duplicating or weakening `AUTH-001` and `BR-001` and without prematurely implementing the full control plane.

## O. Exact continuation instruction

> Continue the NorthStar Agentic AI Architecture Playbook by executing only **Stage 9C - Guardrail Architecture and Human Accountability**. Reconstruct the `1.13.0` S09B baseline; preserve exactly one active `AGT-001`, `GRAPH-001/1.9.0`, `TM-001/1.1.0`, `AUTH-001/1.0.0`, `BR-001/1.0.0`, all current authority owners, receiver-side authorization, gateway-only tools, human approval/finalization, one concurrent protected write, sealed evaluation controls, inactive `WP-008`/MCP/A2A/multi-agent routes and unresolved Stage 8D gates. Design deterministic and model-assisted guardrails across input, context, retrieval, planning, tool execution, output, state, memory and human review; define synchronous/asynchronous placement, policy ownership, exceptions, evidence and negative tests; update all artefacts, run the consistency audit and stop before the full Agentic AI control-plane implementation.
