# 00 - Project Constitution (S09B compatible overlay)

Version `1.13.0`. Preserve all accepted prior constitutional provisions. S09B adds these invariants:

1. Exactly one active `AGT-001`; no agent or model is a human principal.
2. Human, workload, agent, service and tool identities remain distinct.
3. `CMP-007` is the sole grant issuer; user tokens/credentials are never passed unrestricted.
4. Every derived grant is short-lived, audience/tool-specific, request-bound and monotonically attenuated.
5. `CMP-004` and `CMP-005` enforce authorization at the receiver before data/tool access.
6. A valid signature is insufficient without semantic, proof, replay, use, revocation, approval and budget checks.
7. Humans own approval/finalization; approval claims reference, but never create, human decisions.
8. Authority tiers 0-5 apply; tier 4 has no current tools; tier 5 is never autonomously delegable.
9. `CMP-003` owns run budgets and protected state; authorization cannot mutate `DATA-106`.
10. Broader guardrails/control plane and Stage 8D promotion gates remain unresolved.
