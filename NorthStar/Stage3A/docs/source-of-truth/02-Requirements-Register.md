# 02 — Requirements Register

**Version:** `0.5.0`

`FR-001`–`FR-048`, `NFR-001`–`NFR-037`, `POL-*`, and `CTL-001`–`CTL-018` retain their accepted meanings from the supplied S02B handoff. S03A adds the following requirements without renumbering prior items.

## New functional requirements

| ID | Requirement | Status |
|---|---|---|
| `FR-049` | Maintain a versioned allowlisted catalogue of typed tool capabilities. | Implemented locally. |
| `FR-050` | Validate all tool inputs and outputs against strict schemas before use. | Implemented. |
| `FR-051` | Resolve authorization before an adapter receives arguments. | Implemented with local unauthenticated claims. |
| `FR-052` | Classify every tool by impact and reject prohibited classes. | Implemented for S03A. |
| `FR-053` | Require idempotency and conflict detection for reversible writes. | Implemented in memory/local store. |
| `FR-054` | Bound timeout, result size, rate, circuit state and permitted retry. | Implemented locally. |
| `FR-055` | Expose authorized evidence retrieval as a tool without widening S02B access. | Implemented with local adapter. |
| `FR-056` | Create only an unapproved, human-review-required draft case artefact. | Implemented locally. |
| `FR-057` | Save only an unaccepted candidate policy/control mapping. | Implemented locally. |
| `FR-058` | Queue a human-review request without granting approval or sending externally. | Implemented locally. |
| `FR-059` | Return a consistent typed result/error envelope and execution evidence. | Implemented. |
| `FR-060` | Prevent model/agent direct adapter execution; defer action selection. | Implemented by architecture/repository boundary. |

## New non-functional requirements

| ID | Requirement | Status |
|---|---|---|
| `NFR-038` | Descriptor identity must be deterministic and change-detectable. | SHA-256 implemented. |
| `NFR-039` | Contract, registry and policy failures must fail closed. | Implemented. |
| `NFR-040` | Repeated writes must be replay-safe within the local runtime. | Implemented; durability open. |
| `NFR-041` | Execution must have bounded timeout, attempts and result bytes. | Implemented. |
| `NFR-042` | Canonical contracts must remain provider/protocol neutral. | Implemented. |
| `NFR-043` | Execution evidence must hash arguments and support field redaction. | Implemented locally. |
| `NFR-044` | The local proof must be reproducible with synthetic data. | Implemented/tested. |
| `NFR-045` | No agent, graph, memory or irreversible authority may be falsely claimed. | Enforced by tests/audit. |
| `NFR-046` | Tool/schema versions must be explicit; mismatches must be rejected. | Implemented. |

## New controls

| ID | Control |
|---|---|
| `CTL-019` | Exact allowlisted tool ID/version resolution and descriptor hashing. |
| `CTL-020` | Draft 2020-12 input/output validation with `additionalProperties=false`. |
| `CTL-021` | Deterministic gateway PEP and local policy decision before adapter execution. |
| `CTL-022` | Impact classification, mandatory write idempotency, no automatic write retry. |
| `CTL-023` | Timeout, rate limit, circuit breaker, result-size limit and bounded read retry. |
| `CTL-024` | Output validation and preservation of S02B untrusted-evidence notice/access boundary. |
| `CTL-025` | Argument hashing, configured redaction and local execution-event evidence. |
| `CTL-026` | Application-owned draft/unapproved/human-review invariants. |

## Traceability

| Requirement | Components | Data/interfaces | Controls | Evidence |
|---|---|---|---|---|
| `FR-049`, `NFR-038`, `NFR-046` | `CMP-005`, `CMP-011` | `DATA-035`, `INT-016` | `CTL-019` | `TEST-047`–`TEST-051`, `EVAL-014` |
| `FR-050`, `FR-059`, `NFR-039` | `CMP-005`, `CMP-008` | `DATA-036`, `DATA-038`, `INT-017`, `INT-019` | `CTL-020`, `CTL-024` | `TEST-052`, `TEST-057`, `TEST-066` |
| `FR-051` | `CMP-005`, `CMP-007` | `DATA-034`, `DATA-037`, `INT-018` | `CTL-021` | `TEST-058`, `TEST-062` |
| `FR-052`–`FR-054` | `CMP-005`, `CMP-010` | `DATA-039`, `INT-017` | `CTL-022`, `CTL-023` | `TEST-050`, `TEST-054`–`TEST-056`, `TEST-060`, `TEST-063`–`TEST-069` |
| `FR-055` | `CMP-004`, `CMP-005` | `DATA-032`, `INT-014`, `INT-019` | `CTL-024` | `TEST-059`, `TEST-072`, `EVAL-016` |
| `FR-056`–`FR-058` | `CMP-005`, future `CMP-006` | Tool-specific schemas via `DATA-035` | `CTL-022`, `CTL-026` | `TEST-053`, `TEST-071`, demo |
| `FR-060`, `NFR-045` | `CMP-003`, `CMP-005`, `CMP-011` | none | `CTL-019`, `CTL-026` | `TEST-073`, consistency audit |
