# Changelog

## 0.7.0 — 2026-07-31

- Added runtime budget policy and budget ledger.
- Added typed failure envelopes and recovery records.
- Added bounded model fallback, read retry/fallback, dead-end replanning, cancellation and partial completion.
- Added ambiguous-write reconciliation with idempotency-key lookup; no blind write retry.
- Added atomic local checkpoint/resume with checksum validation.
- Preserved exactly one agent and all Stage 3B authority/completion invariants.
