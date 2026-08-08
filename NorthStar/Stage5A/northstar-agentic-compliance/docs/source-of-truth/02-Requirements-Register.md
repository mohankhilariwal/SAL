# 02 — Requirements Register

**Version:** `1.1.0`  
All inherited requirements remain accepted. S05A adds the following items.

## Functional requirements

| ID | Requirement | Owner/components | Control/evidence | Status |
|---|---|---|---|---|
| `FR-120` | Maintain one versioned machine-readable specification for `AGT-001`. | `CMP-011`, `CMP-003` | `CTL-072`; `TEST-183`, `EVAL-042` | Implemented locally |
| `FR-121` | Specify purpose, users, goals and non-goals. | `CMP-011` | `CTL-072`; `TEST-186` | Implemented |
| `FR-122` | Specify inputs, outputs, preconditions, postconditions and invariants. | `CMP-003`, `CMP-011` | `CTL-073`; `TEST-190` | Implemented |
| `FR-123` | Specify exact authority, prohibited actions and allowed tool versions. | `CMP-005`, `CMP-007` | `CTL-074`; `TEST-201`–`203`, `EVAL-044` | Implemented |
| `FR-124` | Bind existing context selection/access/budget rules into `DATA-077`. | `CMP-004`, `CMP-007` | `CTL-075`; `TEST-204`–`206`, `EVAL-045` | Implemented |
| `FR-125` | Specify external human approval, SoD, expiry, timeout and late-decision behavior. | `CMP-006` | `CTL-076`; `TEST-196`, `212` | Implemented |
| `FR-126` | Specify application-owned termination, guard and wait semantics. | `CMP-003`, `GRAPH-001` | `CTL-077`; runtime assertions | Implemented |
| `FR-127` | Specify typed fail-closed error semantics and no prompt override. | `CMP-003`, `CMP-008` | `CTL-078`; negative tests | Implemented |
| `FR-128` | Specify provisional control-path SLOs without claiming production service SLOs. | `CMP-010` | `CTL-079`; benchmark | Implemented locally |
| `FR-129` | Specify required evaluations, tests and release evidence. | `CMP-008` | `CTL-080`; `EVAL-042`–`047` | Implemented |
| `FR-130` | Validate schema structure and cross-contract semantics before start. | `CMP-003`, `CMP-008` | `CTL-073`; `TEST-183`–`191` | Implemented |
| `FR-131` | Bind specification ID/version/digest to the harness manifest/session. | `CMP-003`, `CMP-010` | `CTL-081`; `TEST-192`, `193` | Implemented |
| `FR-132` | Execute deterministic pre-start and post-result assertions. | `CMP-003`, `CMP-008` | `CTL-082`; `TEST-194`–`197`, `207`, `208` | Implemented |
| `FR-133` | Deny release/start when mandatory test/evaluation/security evidence is absent. | `CMP-008`, `CMP-010` | `CTL-083`; `TEST-198`, `199`, `211`, `212` | Implemented locally |
| `FR-134` | Define ownership, lifecycle, change policy and retirement criteria. | `CMP-011` | `CTL-084`; `TEST-189`, `191`, `200`, `EVAL-047` | Implemented |
| `FR-135` | Deny new starts for a retired specification. | `CMP-003` | `CTL-084`; `TEST-200` | Implemented |
| `FR-136` | Preserve one-agent/no-memory/no-concurrency boundaries and all S04C authority semantics. | `CMP-003`–`010` | `CTL-074`–`084`; all tests | Implemented |

## Non-functional requirements

| ID | Requirement | Verification/status |
|---|---|---|
| `NFR-096` | Canonical specification serialization and digest are deterministic. | `TEST-184`; local pass |
| `NFR-097` | Unknown top-level properties fail closed. | `TEST-185`; pass |
| `NFR-098` | Stable IDs and versions cannot drift silently. | `TEST-187`, `188`, `192`, `193`; pass |
| `NFR-099` | Validation, assertions and gates use standard-library runtime dependencies only. | Compilation/manifest inspection; pass |
| `NFR-100` | Specification validation local P95 target <=50 ms. | Local microbenchmark only; pass in executed environment |
| `NFR-101` | Runtime assertion local P95 target <=20 ms. | Local microbenchmark only; pass |
| `NFR-102` | Deployment gate local P95 target <=20 ms. | Local microbenchmark only; pass |
| `NFR-103` | No raw callback token, unrestricted credential or hidden reasoning is persisted by S05A code. | `TEST-207`; pass within local boundary |
| `NFR-104` | Specification errors are deterministic and machine-readable. | Validation reports and tests; pass |
| `NFR-105` | Gate decisions are reproducible for identical evidence. | deterministic code/tests; pass |
| `NFR-106` | No production availability, throughput, model-quality or legal-validity claim is inferred from local controls. | documentation/audit; passed with caveat |
| `NFR-107` | Changes remain traceable across specification, manifest, ADRs, schemas, tests and registers. | consistency audit; pass with reconstruction exception |

## Controls

| ID | Control |
|---|---|
| `CTL-072` | Repository-controlled versioned `DATA-071` with required ownership and scope fields. |
| `CTL-073` | JSON Schema artefact plus strict application semantic validator and unknown-property rejection. |
| `CTL-074` | Exact `AGT-001`, `GRAPH-001`, `DATA-009`, `TOOL-001`–`006`, gateway and non-authority assertions. |
| `CTL-075` | `DATA-077` allow/prohibit lists, authorization-before-load, provenance/hash and size budgets. |
| `CTL-076` | External `CMP-006` human-decision, SoD, expiry, timeout and no-final-closure invariants. |
| `CTL-077` | Graph/application ownership of routes, termination and postconditions. |
| `CTL-078` | Typed fail-closed specification/compatibility/assertion/gate errors with no prompt override. |
| `CTL-079` | Explicitly provisional local control-path latency targets and benchmark labels. |
| `CTL-080` | Specification-derived required evaluation/test evidence. |
| `CTL-081` | Canonical SHA-256 digest bound into `DATA-072` and manifest. |
| `CTL-082` | Pre-start and post-result deterministic assertions. |
| `CTL-083` | Deny-by-default `DATA-076` gate with zero blocking local security findings. |
| `CTL-084` | Active/deprecated/retired lifecycle, retirement criteria and denial of retired new starts. |

## Traceability summary

`FR-120`–`136` trace to `DATA-071`–`078`, `INT-047`–`052`, `ADR-036`–`039`, `CTL-072`–`084`, `TEST-183`–`212` and `EVAL-042`–`047`. No requirement is represented as enterprise-production complete.
