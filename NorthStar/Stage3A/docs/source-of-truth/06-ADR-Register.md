# 06 — ADR Register

**Version:** `0.5.0`

`ADR-001`–`ADR-017` remain accepted. S03A adds:

| ADR | Decision | Status |
|---|---|---|
| `ADR-018` | Use application-owned, versioned, hashed tool descriptors with JSON Schema Draft 2020-12 as canonical contracts. | Accepted. |
| `ADR-019` | Route every invocation through one application-owned tool gateway; no caller/model bypass. | Accepted. |
| `ADR-020` | Classify impact; allow only read/reversible tools, require write idempotency and prohibit automatic write retry. | Accepted. |
| `ADR-021` | Defer MCP, remote protocols and model-selected agent execution; use in-process adapters in S03A. | Accepted. |

Full records are in `docs/adr/ADR-018-*.md` through `ADR-021-*.md`.
