# 06 — ADR Register
**Version:** `1.3.0`

`ADR-001`–`043` remain accepted.

## ADR-044 — Retain One Agent and Specialize the Existing Graph
- **Status:** Accepted, 2026-08-01.
- **Context:** Six task roles share one state, gateway, human authority, memory scope and mainly sequential workflow.
- **Decision:** Keep exactly one `AGT-001`; use existing graph work units plus six bounded profiles.
- **Alternatives:** broad prompt; informal prompt switching; manager/specialists; peer handoffs; distributed agents.
- **Rationale:** task breadth is not an independent agent boundary.
- **Consequences:** profile governance/digests added; no delegation/communication runtime.
- **Risks/Mitigations:** drift and false role isolation; exact validation, tests and change review.
- **Review triggers:** persistent failures after profile/node remediation; independent authority/lifecycle/fault domain; representative measured gain.

## ADR-045 — Verification Is a Profile/Node, Not a Second Agent
- **Status:** Accepted, 2026-08-01.
- **Decision:** `TPR-005` uses separate instructions, context/output and evaluation under `AGT-001`; deterministic checks and human accountability remain.
- **Alternatives:** self-check only; verifier agent; human-only verification.
- **Rationale:** independent evaluation logic does not automatically need an independently acting identity.
- **Consequences/Risks:** correlated model errors remain; mitigate through deterministic checks, adversarial cases and future cross-model evaluation.
- **Review trigger:** evidence that same-agent verification cannot meet accepted thresholds.

## ADR-046 — Evidence-Gated Multi-Agent Promotion
- **Status:** Accepted, 2026-08-01.
- **Decision:** `INT-062` permits architecture review—not allocation—only for an independent boundary or representative measured gain after single-agent remediation. Allocation requires a new ADR, requirements, threat/privacy review, schemas, implementation and tests.
- **Alternatives:** allocate specialists now; permanently prohibit; model-selected routing.
- **Rationale:** preserve optionality without treating complexity as progress.
- **Risks/Mitigations:** conservative/gamed gate; use documented baselines, repeated trials, cost/latency/handoff/error metrics and human review.
