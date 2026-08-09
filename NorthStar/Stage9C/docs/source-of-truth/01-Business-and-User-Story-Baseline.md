# 01 — Business and User Story Baseline

**Version:** 1.14.0

The accepted NorthStar regulatory-change user stories remain unchanged. Stage 9C adds no persona or business authority.

## Narrative delta

- **Maya Chen** needs evidence that hostile publication text cannot become instructions and that AI output is only a draft until human disposition.
- **Priya Raman** designs stage-specific guardrails and the bounded control-plane profile without adding another agent or moving existing ownership.
- **Marcus Green** requires deterministic enforcement for tenant isolation, authorization composition, tool gateways, state ownership, memory scope and emergency stops.
- **Sofia Alvarez** requires policy ownership, independent release approval, soft-only exceptions, evidence and lifecycle governance.
- **Elena Petrov** implements local immutable bundles and typed validators while preserving future policy-engine portability.
- **Liam O’Connor** requires local cached enforcement to avoid a remote per-request control-plane bottleneck and explicit stale-bundle behavior.
- **Daniel Brooks** retains accountable compliance approval/finalization.
- **Aisha Rahman** retains business-control ownership and may serve as an eligible independent reviewer where policy requires.

## User-story acceptance delta

The system must prevent or route unsafe content/action/state/memory behavior without treating a model, guardrail or policy engine as the accountable decision maker. Every review and exception must be attributable, scoped, versioned and evidenced.
