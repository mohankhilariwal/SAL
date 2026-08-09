# ADR-044

— Retain One Agent and Specialize the Existing Graph
- **Status:** Accepted, 2026-08-01.
- **Context:** Six task roles share one state, gateway, human authority, memory scope and mainly sequential workflow.
- **Decision:** Keep exactly one `AGT-001`; use existing graph work units plus six bounded profiles.
- **Alternatives:** broad prompt; informal prompt switching; manager/specialists; peer handoffs; distributed agents.
- **Rationale:** task breadth is not an independent agent boundary.
- **Consequences:** profile governance/digests added; no delegation/communication runtime.
- **Risks/Mitigations:** drift and false role isolation; exact validation, tests and change review.
- **Review triggers:** persistent failures after profile/node remediation; independent authority/lifecycle/fault domain; representative measured gain.
