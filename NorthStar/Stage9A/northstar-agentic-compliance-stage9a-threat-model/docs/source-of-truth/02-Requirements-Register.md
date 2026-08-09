# 02 Requirements Register - S09A Overlay

| Requirement | Statement | Components | Implementation | Verification |
|---|---|---|---|---|
| `S09A-REQ-001` | Record and safely manage the S08C-to-S09A sequence divergence. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-002` | Reconstruct and version the 1.11.0 architecture snapshot with assets, data flows and trust boundaries. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-003` | Apply STRIDE to architecture-specific elements and flows. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-004` | Crosswalk threats to the OWASP Agentic Top 10 without treating it as a complete control standard. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-005` | Create attack trees for exfiltration, unauthorized action and assessment/audit corruption. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-006` | Create realistic misuse cases with expected preventive, detective and response controls. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-007` | Cover direct/indirect injection, jailbreaking, tool/retrieval/memory poisoning and judge manipulation. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-008` | Cover data exfiltration, secret leakage, cross-tenant leakage, identity abuse, confused deputy and privilege escalation. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-009` | Cover malicious MCP, A2A spoofing, replay and insecure inter-agent communication as inactive-future threats. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-010` | Cover supply chain, unexpected code execution, sandbox/browser abuse and rogue-agent threats. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-011` | Cover DoS, resource/cost attacks, loops, replay, queue flooding and cascading failures. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-012` | Use explicit ordinal inherent/residual factors and preserve critical hard-control semantics. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-013` | Map every threat to assets, flows, controls, tests and treatment status. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-014` | Keep threat-model outputs advisory and unable to change authority, state, routes or deployment. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-015` | Preserve exactly one active AGT-001 and inactive WP-008. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-016` | Provide runnable local code, schemas, validation, reports and tests. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |
| `S09A-REQ-017` | Update all ten source-of-truth artefacts and pass the consistency audit. | `CMP-008`, `CMP-011` | `DATA-165`-`176`, `INT-130`-`139` | `TEST-685`-`736`, `EVAL-169`-`184` |

All inherited requirements remain accepted. S08D metric thresholds and deployment promotion requirements are not implemented by this overlay.
