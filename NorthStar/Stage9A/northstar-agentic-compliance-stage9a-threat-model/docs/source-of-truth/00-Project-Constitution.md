# 00 Project Constitution - S09A Overlay

- Architecture/repository version: `1.12.0`
- Graph version: `GRAPH-001/1.8.0`
- Source baseline: compatible `1.11.0` S08C overlays; byte-exact historical merge remains open.

## Preserved constitutional invariants

NorthStar, the eight personas, `US-001`-`012`, `CMP-001`-`011`, `AGT-001-spec 1.1.0`, `DATA-009 1.1.0`, `TOOL-001`-`006`, human approval/finalization, gateway-only tools, sole authority issuance by `CMP-007`, protected-state ownership by `CMP-003`, sealed evaluation controls, non-overridable deterministic/critical bias failures, inactive `WP-008`, prohibited semantic regulatory-answer caching and no active model/provider/route are preserved.

## S09A additions

1. Threat modelling is a design-time assurance capability inside `CMP-008` governed by `CMP-011`.
2. Threat evidence and recommendations have `authority_effect: none`.
3. The current single-agent scope and inactive future multi-agent scope are labelled separately.
4. A hard security invariant cannot be compensated by an aggregate risk score.
5. Architecture, data flows, boundaries, threats, controls and tests are versioned and digestible.
6. S08D metrics/regression/deployment gates remain unresolved.
