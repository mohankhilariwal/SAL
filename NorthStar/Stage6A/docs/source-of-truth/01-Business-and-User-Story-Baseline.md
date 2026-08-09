# 01 — Business and User Story Baseline
**Version:** `1.3.0`

NorthStar Financial Services, the eight accepted personas and `US-001`–`012` remain unchanged.

Maya's case can now resume with bounded context. Priya assesses whether `AGT-001`'s research, extraction, mapping, risk, verification and reporting tasks require multiple agents. Marcus requires a new identity only for a real security/fault boundary. Sofia requires measured benefit and governance evidence. Elena and Liam require operability, latency and failure-surface evidence.

The six tasks remain roles within one governed case workflow: they share authoritative state, gateway, approval path, memory scope, tenant/user/case, termination owner and sequential dependencies.

### Acceptance criteria
- Preserve preliminary, evidence-backed, human-accountable semantics.
- Improve task focus without identity, delegation or handoffs.
- Make verification explicit and separately evaluated, but not a second agent or approver.
- Profiles expose only subsets of `TOOL-001`–`006` and never bypass `CMP-005`.
- Multi-agent promotion is deny-by-default and ADR/change-review controlled.
- No-memory resume remains valid; optional working memory stays subordinate and case-local.
