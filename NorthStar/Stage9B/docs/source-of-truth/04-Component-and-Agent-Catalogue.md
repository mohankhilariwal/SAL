# 04 - Component and Agent Catalogue (S09B overlay)

All component names and IDs remain unchanged.

| ID | S09B responsibility extension |
|---|---|
| `CMP-003` | Creates `DATA-178`; requests grants; owns run budget and emergency-stop intent; remains sole protected-state/route owner. |
| `CMP-004` | Enforces retrieval/data authorization before loading evidence. |
| `CMP-005` | Verifies grant/proof/state/policy and reserves blast-radius budget before `TOOL-001`-`006`. |
| `CMP-006` | Supplies authoritative transaction-bound human approval evidence. |
| `CMP-007` | Sole identity/token issuer, policy evaluator and revocation authority. |
| `CMP-008` | Evaluates authorization security and updates `TM-001`. |
| `CMP-009` | Receives minimized authorization evidence; no WORM claim. |
| `CMP-011` | Governs `1.13.0` compatibility and decisions. |

Agent inventory: `AGT-001 Regulatory Impact Assessment Agent`, spec `1.1.0`, exactly one active. No authority to issue/enlarge/revoke grants, alter budgets/tiers, approve/finalize, mutate `DATA-106`, create agents or activate routes. `WP-008`, MCP/A2A and additional agents remain inactive.
