# ADR-047 — Protocol-Neutral Handoff Contracts Before Transport Selection

- **Status:** Accepted
- **Context:** NorthStar needs task identity, status, artefact, timeout and receipt semantics before choosing in-process calls, REST, gRPC, queues, MCP or agent-to-agent protocols.
- **Decision:** Define canonical signed `DATA-092`, `DATA-094`, `DATA-095`, `DATA-097` and `DATA-098` contracts independent of transport. Do not select MCP/A2A or a network transport in S06B.
- **Alternatives:** Framework-native handoffs; REST-first; queue-first; MCP/A2A-first; shared database/workspace.
- **Rationale:** Application semantics and trust boundaries must survive a later transport choice. Premature protocol selection would obscure missing ownership, failure and authority rules.
- **Consequences:** More application-owned schema code now; easier future protocol adapters and conformance tests.
- **Risks:** Custom semantics may diverge from future standards; mitigated through adapter mapping and versioned schemas.
- **Review trigger:** A production deployment boundary, cross-team service, interoperability requirement or representative protocol benchmark.
