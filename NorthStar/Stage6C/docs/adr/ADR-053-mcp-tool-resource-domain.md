# ADR-053 — Map MCP 2026-07-28 to Tool and Resource Interoperability at CMP-005

- **Status:** Accepted
- **Context:** MCP standardizes AI host/client/server interaction around tools, resources, prompts, capabilities and authorization, while NorthStar needs a separate delegated-agent task contract.
- **Decision:** Use the current MCP 2026-07-28 specification as a conformance target for tool/resource exposure through CMP-005. Do not map MCP tools into agent identity, approval, case termination or unrestricted authority. No MCP server is activated in S06C.
- **Alternatives:** Treat MCP as the agent-to-agent bus; retain only 2025-11-25; ignore MCP.
- **Rationale:** Aligns protocol semantics to the correct boundary and avoids a confused-deputy shortcut.
- **Consequences:** MCP can improve tool/resource portability later; delegated tasks still use DATA-091–099.
- **Risks:** Tool metadata mistaken for authorization; remote-server/tool poisoning.
- **Mitigations:** CMP-005/CMP-007 enforcement, allowlists, schema validation, server registry and evaluation gates in later production stages.
- **Review trigger:** MCP adds stable task semantics that demonstrably cover every NorthStar invariant.
