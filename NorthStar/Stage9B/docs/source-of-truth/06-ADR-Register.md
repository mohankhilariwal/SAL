# 06 - ADR Register (S09B overlay)

Preserve `ADR-001`-`094`. Add:

## ADR-095 - Execute combined S09B identity/authorization/blast-radius scope; stop before broader guardrails/control plane.

**Status:** Accepted. **Review triggers:** material identity/token/policy/tool/tier/protocol/deployment change; production pilot; new agent; security incident.

## ADR-096 - Separate identity types and bind agent execution to human/workload/case/run/task.

**Status:** Accepted. **Review triggers:** material identity/token/policy/tool/tier/protocol/deployment change; production pilot; new agent; security incident.

## ADR-097 - Use token exchange and attenuated short-lived grants; prohibit user-token passthrough.

**Status:** Accepted. **Review triggers:** material identity/token/policy/tool/tier/protocol/deployment change; production pilot; new agent; security incident.

## ADR-098 - Use mTLS or DPoP sender constraint in production; local Ed25519 proof is nonconformant teaching code.

**Status:** Accepted. **Review triggers:** material identity/token/policy/tool/tier/protocol/deployment change; production pilot; new agent; security incident.

## ADR-099 - Use hybrid RBAC, ABAC/PBAC and targeted ReBAC with receiver enforcement.

**Status:** Accepted. **Review triggers:** material identity/token/policy/tool/tier/protocol/deployment change; production pilot; new agent; security incident.

## ADR-100 - Require stateful nonce/use/revocation/approval checks beyond signed claims.

**Status:** Accepted. **Review triggers:** material identity/token/policy/tool/tier/protocol/deployment change; production pilot; new agent; security incident.

## ADR-101 - Keep blast-radius budgets orthogonal to grants and atomically reserve at receivers.

**Status:** Accepted. **Review triggers:** material identity/token/policy/tool/tier/protocol/deployment change; production pilot; new agent; security incident.

## ADR-102 - Adopt authority tiers 0-5; no tier-4 tools and tier 5 prohibited autonomously.

**Status:** Accepted. **Review triggers:** material identity/token/policy/tool/tier/protocol/deployment change; production pilot; new agent; security incident.

## ADR-103 - Production adapters must preserve semantics and pass conformance/security review.

**Status:** Accepted. **Review triggers:** material identity/token/policy/tool/tier/protocol/deployment change; production pilot; new agent; security incident.

