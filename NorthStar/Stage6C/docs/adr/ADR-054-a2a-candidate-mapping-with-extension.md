# ADR-054 — Map A2A 1.0 to Agent Task Lifecycle Only With a Required NorthStar Extension

- **Status:** Accepted
- **Context:** A2A provides Agent Cards, interfaces, messages, tasks, artifacts, status and cancellation, but NorthStar also requires exact attenuated authority, deadline, causation, approval-boundary and CMP-003 termination ownership.
- **Decision:** Create a conformance-only A2A 1.0 profile. Native A2A objects carry discovery/task/artifact/status semantics. A required NorthStar extension carries the remaining invariants. Do not serve an A2A endpoint or allocate AGT-002.
- **Alternatives:** A2A without extension; custom protocol only; activate the candidate endpoint as an agent.
- **Rationale:** Tests interoperability without weakening accepted controls or manufacturing promotion evidence.
- **Consequences:** Interoperability requires extension recognition; third-party endpoints that ignore it are rejected.
- **Risks:** Extension stripping, false capability claims, unsigned Agent Cards.
- **Mitigations:** Required extension declaration, card digest/signature target, exact version and security-scheme validation.
- **Review trigger:** Evidence gate justifies an independent agent and production trust/discovery are designed.
