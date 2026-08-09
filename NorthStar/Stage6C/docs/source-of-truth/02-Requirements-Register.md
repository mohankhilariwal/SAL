# 02 — Requirements Register

**Version:** 1.5.0

All `FR-001`–`189`, inherited NFRs and controls remain accepted. S06C adds:

| ID | Requirement | Status |
|---|---|---|
| `FR-190` | Versioned protocol profiles. | Verified locally |
| `FR-191` | Capability advertisement without authority/allocation. | Verified locally |
| `FR-192` | Exact version and approved binding. | Verified locally |
| `FR-193` | Canonical serialization preservation. | Verified locally |
| `FR-194` | Receiver header/digest/version checks. | Verified locally |
| `FR-195` | Authorization before content use. | Verified locally |
| `FR-196` | Delivery receipt and semantic-loss evidence. | Verified locally |
| `FR-197` | MCP tools remain CMP-005 governed. | Verified locally |
| `FR-198` | MCP resources are immutable authorized references. | Verified locally |
| `FR-199` | MCP full agent-handoff mapping must fail when semantics are missing. | Verified locally |
| `FR-200` | Candidate A2A Agent Card without allocation. | Verified locally |
| `FR-201` | A2A Message/Task mapping. | Verified locally |
| `FR-202` | A2A Artifact mapping without shared state. | Verified locally |
| `FR-203` | Lifecycle mapping with stricter NorthStar rules. | Verified locally |
| `FR-204` | Required NorthStar A2A extension. | Verified locally |
| `FR-205` | Adapter conformance record. | Verified locally |
| `FR-206` | Reject loss/downgrade/extension stripping. | Verified locally |
| `FR-207` | One active agent and sequential execution. | Verified locally |
| `FR-208` | Defer gRPC/broker/framework activation. | Verified locally |

`NFR-150`–`165`: deterministic canonicalization, exact negotiation, fail-closed validation, stable correlation/digests, receiver PEP, no retries/concurrency, loopback reference, bounded/minimized payloads/errors, local reproducibility, explicit implementation statuses, transparent benchmarks and backward compatibility.

`CTL-131`–`148`: profile allowlists; exact negotiation; digest headers; receiver PEP; candidate status/power checks; MCP/A2A domain rules; required extension; gateway/state/memory/agent/concurrency invariants; semantic-loss rejection; loopback warning and release audit.

See the Stage 6C chapter Section 22 for traceability.

Evaluation trace: `EVAL-070`–`EVAL-078`; terminal profile-status evidence is `EVAL-078`.
