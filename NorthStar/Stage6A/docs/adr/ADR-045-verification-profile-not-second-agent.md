# ADR-045

— Verification Is a Profile/Node, Not a Second Agent
- **Status:** Accepted, 2026-08-01.
- **Decision:** `TPR-005` uses separate instructions, context/output and evaluation under `AGT-001`; deterministic checks and human accountability remain.
- **Alternatives:** self-check only; verifier agent; human-only verification.
- **Rationale:** independent evaluation logic does not automatically need an independently acting identity.
- **Consequences/Risks:** correlated model errors remain; mitigate through deterministic checks, adversarial cases and future cross-model evaluation.
- **Review trigger:** evidence that same-agent verification cannot meet accepted thresholds.
