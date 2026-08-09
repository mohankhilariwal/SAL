# 00 — Project Constitution (1.9.0 Overlay)

All accepted constitutional items through `1.8.0` remain. This overlay adds Stage 8A evaluation principles:

1. Evaluation evidence must precede final model-routing selection (`ADR-072`).
2. Evaluation is layered and outcome-first; trace evidence is required for assurance (`ADR-073`).
3. Evaluation datasets are immutable, versioned, documented and split-controlled (`ADR-074`).
4. Deterministic controls and human expertise precede LLM-as-a-Judge (`ADR-075`).
5. Evaluation environments are isolated; outputs are advisory (`ADR-076`).
6. A passed evaluation can never grant authority, approve/finalize a case, create an agent, bypass `CMP-005`/`CMP-007`, or mutate `DATA-106`.
7. Raw customer data and hidden chain-of-thought are not permitted in local evaluation evidence.
8. NorthStar retains exactly one active `AGT-001`; `WP-008` remains `inactive_future`.
9. Semantic regulatory-answer caching remains prohibited.
10. Because full historical registers remain unavailable, this is a compatible overlay under `ISS-096`.

**Version:** architecture/repository/handoff `1.9.0`; graph `GRAPH-001/1.5.0`.
