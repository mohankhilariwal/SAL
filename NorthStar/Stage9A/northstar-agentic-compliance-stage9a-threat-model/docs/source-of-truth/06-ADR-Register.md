# 06 ADR Register - S09A Overlay

`ADR-001`-`088` remain accepted.

- `ADR-089`: Execute Stage 9A before unresolved Stage 8D - Proceed with the explicitly requested threat-modelling stage against the 1.11.0 baseline, record the sequence divergence, and keep metrics/regression/deployment gates unresolved.
- `ADR-090`: Use a hybrid threat-modelling method - Use data-flow and trust-boundary analysis plus STRIDE for systematic coverage, then add OWASP agentic crosswalks, attack trees and misuse cases for agent-specific and adversarial paths.
- `ADR-091`: Version and digest the architecture threat-model snapshot - Threat analysis consumes an immutable architecture snapshot containing components, assets, flows, boundaries, invariants and active/future status.
- `ADR-092`: Use ordinal risk prioritization without false precision - Use a NorthStar 1-5 likelihood and impact scale only for prioritization; preserve raw factors and hard invariant failures rather than claiming actuarial probabilities or a universal score.
- `ADR-093`: Model current single-agent and inactive future multi-agent scopes separately - Assess the running one-agent architecture and a clearly labelled future MCP/A2A/multi-agent scope without allocating or activating another agent.
- `ADR-094`: Keep threat treatment advisory and externally governed - Threat reports and treatment recommendations have authority_effect none and cannot mutate DATA-106, approve/finalize, change routes, create agents or deploy controls automatically.
