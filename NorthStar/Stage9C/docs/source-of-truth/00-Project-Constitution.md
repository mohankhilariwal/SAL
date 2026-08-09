# 00 — Project Constitution

**Version:** 1.14.0  
**Stage:** S09C — Guardrails, Governance and Control Plane

## Preserved constitution

NorthStar Financial Services, the eight accepted personas, `US-001`–`012`, `CMP-001`–`011`, exactly one active `AGT-001`, `TOOL-001`–`006`, accepted data/interfaces/ADRs and the narrative-driven progressive architecture remain authoritative.

## Stage 9C constitutional additions

1. `GR-001/1.0.0` defines stage-specific guardrails across input, context, retrieval, planning, tool/result, output, state, memory, human review and runtime.
2. `GOV-001/1.0.0` defines control ownership, change, validation, testing, approval, release, exception, incident and retirement lifecycle.
3. `CP-001/0.1.0` is a bounded local reference for policy release/distribution only; the full production control plane is not implemented.
4. Guardrail decisions have `authority_effect: none`; allow is not authorization, approval, finalization or protected-state mutation.
5. `AUTH-001/1.0.0` and `BR-001/1.0.0` remain independently mandatory and unchanged.
6. Hard controls are synchronous and non-overrideable. Model-assisted controls are advisory and cannot authorize/approve or override deterministic denial.
7. Exceptions apply only to explicit soft controls, are tenant/case/operation/control scoped, expire within 30 days, require compensating controls and two independent humans.
8. Humans own approval/finalization; timeout never approves; reviews bind exact digests.
9. `CMP-003` remains sole route/protected-state owner; `CMP-005` only tool gateway; `CMP-007` sole authority issuer; `CMP-006` human decision boundary.
10. One concurrent protected write remains the maximum. Tier 4 has no tools; tier 5 cannot be autonomously granted.
11. `WP-008`, MCP/A2A and additional agents remain inactive. Stage 8D remains unresolved and production promotion is denied.
12. Every material policy/control/owner/exception/engine change requires impact analysis, ADR, threat-model delta and tests.

## Definition of done for S09C

- Complete cross-stage guardrail model and ownership.
- Runnable local engine and policy lifecycle.
- Negative tests for bypass, injection, false approval, cross-scope state/memory and policy exceptions.
- Updated diagrams, data/interfaces, ADRs, repository, risks and handoff.
- Passed consistency audit with exceptions explicitly recorded.
