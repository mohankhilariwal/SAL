# 06 — ADR Register

**Version:** `1.4.0`

`ADR-001`–`046` remain accepted and are not superseded.

| ADR | Decision | Status |
|---|---|---|
| ADR-047 | Define canonical protocol-neutral handoff/artefact/receipt/lifecycle contracts before transport selection. | Accepted |
| ADR-048 | Use `CMP-007`-issued attenuated authority and recipient/resource-side enforcement before data load/action. | Accepted |
| ADR-049 | Keep handoffs orchestrator-mediated, one-hop, one-attempt and sequential; no peer delegation/concurrency. | Accepted |
| ADR-050 | Keep state private/owned; exchange immutable artefacts; no shared mutable state or shared-agent memory. | Accepted |

## Interaction with prior decisions

- `ADR-044` still retains one active agent and specialized graph profiles.
- `ADR-045` still treats evidence verification as a profile/evaluation surface, not an accepted second agent.
- `ADR-046` still requires independent-boundary or representative measured-value evidence before promotion review.
- S06B supplies future contracts but no promotion evidence or active-agent allocation.
