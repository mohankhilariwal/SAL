# 03 — Architecture Baseline

**Architecture version:** `1.4.0`

## Preserved baseline

- `CMP-001`–`011` unchanged.
- `AGT-001` only active agent; specification `1.1.0`.
- `GRAPH-001 1.1.0` remains sequential and application-owned.
- `DATA-009 1.1.0` remains authoritative.
- `TOOL-001`–`006` remain gateway-only.
- `CMP-006` remains the external human decision owner.
- `DATA-081` remains optional harness-owned case-working memory.

## S06B architectural change

S06B adds a protocol-neutral handoff contract layer inside existing boundaries:

- `CMP-003`: endpoint validation, envelope creation, lifecycle and termination.
- `CMP-007`: grant mint/attenuate/verify/revoke.
- `CMP-008`: contract and boundary evaluation.
- `CMP-009`: local status/receipt evidence, not audit/WORM.
- `CMP-010`: deterministic sequential sandbox.
- `CMP-011`: endpoint status and disabled-capability governance.

No new `CMP-*` component is needed. No production service boundary is claimed.

## Cumulative architecture

```mermaid
flowchart TB
  MAYA["Maya / CMP-001"] --> C3["CMP-003 / GRAPH-001 1.1.0 / DATA-009 1.1.0"]
  C3 --> A1["AGT-001 active / spec 1.1.0"]
  A1 --> GW["CMP-005 / TOOL-001..006 gateway-only"]
  C3 --> H["CMP-006 external human decision"]
  C7["CMP-007"] --> AUTH["INT-064 / DATA-093 attenuated authority"]
  C3 --> ENV["INT-063/065 / DATA-092 signed envelope"]
  ENV --> ART["INT-066 / DATA-095 immutable artefact"]
  ENV -. sandbox only .-> CAND["CAND-EVIDENCE-VERIFIER-001"]
  AUTH --> CAND
  CAND --> RCP["DATA-094 receipt + DATA-096 result"]
  CAND --> EVT["DATA-097 status / DATA-098 failure"]
  RCP --> C3
  EVT --> C3 --> TERM["INT-070 / DATA-099 termination record"]
  DISABLED["No second active agent, concurrency or protocol selection"] -. constrains .-> CAND
```

## Trust and state rules

- `CMP-003` is the only protected-state writer and route owner.
- `CMP-007` is the only authority issuer.
- Recipient checks authorization before content load.
- Candidate endpoint is a separate sandbox trust boundary but has no production status.
- Artefact exchange is immutable and case/subject scoped.
- Private scratch is ephemeral; shared mutable state and shared memory are prohibited.

## Runtime/deployment status

Local sequential Python only. No network transport, queue, worker, concurrency or remote identity system.
