# 01 — Business and User Story Baseline — Version 1.15.0 Overlay

All accepted NorthStar business scope, eight personas and `US-001–012` remain unchanged.

## S10A narrative increment

Maya Chen requires a defensible explanation of how `CASE-2026-0001` moved from intake through evidence retrieval, tool-mediated review and Aisha Rahman's request for changes. Liam O'Connor requires end-to-end operational traces and metrics. Sofia Alvarez requires a complete, version-bound accountability record. Marcus Green requires minimization, redaction, anti-tamper controls and proof that correlation/audit cannot grant authority. Priya Raman requires a provider-neutral design that does not imply the missing S09D enterprise control plane.

## Business acceptance criteria

- A run can be correlated across current NorthStar components without treating identifiers as credentials.
- Required human, authorization, tool and state events are retained independently of operational sampling.
- Sensitive content is not captured by default.
- A local evidence package detects record tampering and binds the accepted versions/digests.
- No human accountability is transferred to `AGT-001` or `CMP-009`.
- Production-readiness, WORM, legal-admissibility, Stage 8D and Stage 9D claims remain explicitly denied.
