# 02 - Requirements Register

**Version:** 0.2.0

## Accepted functional baseline

`FR-001` through `FR-020` remain accepted with their S00 meanings covering intake, analysis, evidence, workflow, approval, remediation, audit, authorization, evaluation and change control. This file records S01 status without renumbering or replacing the baseline.

### S01 requirement disposition

| ID | Preserved requirement meaning | S01 disposition | Evidence |
|---|---|---|---|
| FR-001 | Register and validate a regulatory publication with immutable provenance. | Implemented for one UTF-8 text/Markdown file. | `intake.py`; TEST-008 to TEST-011 |
| FR-002 | Produce a preliminary AI-assisted summary while separating source facts, candidate interpretation and uncertainty. | Implemented through provider-neutral single-turn model contract. | `schemas.py`, `service.py`; TEST-012 to TEST-014 |
| FR-007 | Identify candidate affected jurisdictions/business areas without treating candidates as accepted mappings. | Partially implemented as source-bounded candidate area labels. | mock/provider payload and fixed limitations |
| FR-014 | Preserve human accountability and route material findings to review. | Status semantics implemented; review service remains planned. | fixed `human_review_required`; TEST-012, TEST-016, TEST-017 |
| FR-019 | Preserve model/prompt/schema/configuration identity for reproducibility and assurance. | Implemented for invocation metadata. | `ModelInvocationRecord`; persisted artifacts |
| FR-020 | Maintain versioned project, identifiers, decisions and cross-stage consistency. | Updated to 0.2.0. | source-of-truth validator and audit |

Other functional requirements remain accepted and planned.

## Stage 1 relevant non-functional requirements

| ID | S01 interpretation | Status |
|---|---|---|
| NFR-001 | Human accountability and advisory-only output. | Enforced |
| NFR-002 | Evidence provenance and exact source references. | Enforced at line/excerpt level |
| NFR-003 | Input is untrusted and cannot widen authority. | Partially enforced; no tools or secrets |
| NFR-004 | Privacy and production-data restrictions for local labs. | Synthetic dataset only |
| NFR-005 | Case/user isolation. | Not implemented; single-user local lab |
| NFR-006 | Availability and graceful manual fallback. | Manual fallback documented; no HA |
| NFR-007 | Interactive response expectations. | Measured only for local mock; no production SLO |
| NFR-008 | Bounded cost and input size. | Input byte limit; no managed-cost benchmark |
| NFR-009 | Portability and provider isolation. | Enforced by protocol and standard library |
| NFR-010 | Explainable evidence presentation. | Exact citations and uncertainty fields |
| NFR-011 | Auditability without hidden chain-of-thought. | Invocation/evidence records; no CoT |
| NFR-012 | Vendor-neutral contracts. | Enforced |
| NFR-013 | Testability and deterministic validation. | Enforced |
| NFR-014 | Versioned dependencies, prompts and schemas. | Enforced with recorded exceptions |
| NFR-015 | Separation of concerns. | Enforced by modules |
| NFR-016 | Provider-specific code behind a boundary. | Enforced |
| NFR-017 | Secure secret handling. | Environment variable only; no secret store |
| NFR-018 | Data residency/provider policy. | Not implemented |
| NFR-019 | Evidence summaries rather than hidden reasoning. | Enforced |
| NFR-020 | Analyst-readable structured output. | Enforced as JSON |
| NFR-021 | Accessibility/usability beyond CLI. | Planned |
| NFR-022 | Compatibility and change-control evidence. | Enforced; Python 3.12 direct run open |

## Policies and controls

`POL-001` through `POL-012` and `CTL-001` through `CTL-015` retain their S00 meanings. S01 implements the following constrained control outcomes:

- `CTL-001`: source provenance and integrity hash.
- `CTL-002`: deterministic schema/evidence validation and application-owned disposition.
- `CTL-006`: mandatory human-review semantics; no executable review service.
- `CTL-010`: local evaluation cases and regression tests.
- `CTL-014`: prompt/schema/package/configuration version evidence.

## Traceability

| Requirement | Components | Data | Tests/evaluation |
|---|---|---|---|
| FR-001 | CMP-001, CMP-002, CMP-010 | DATA-001, DATA-014 | TEST-008 to TEST-011 |
| FR-002 | CMP-001, CMP-003, CMP-008 | DATA-015, DATA-016 | TEST-012 to TEST-014; EVAL-001 to EVAL-004 |
| FR-007 | CMP-003 | DATA-015 | EVAL-002, EVAL-004 |
| FR-014 | CMP-001, CMP-006 planned, CMP-008 | DATA-015 | TEST-012, TEST-016, TEST-017 |
| FR-019 | CMP-003, CMP-009 | DATA-017, DATA-018 | TEST-015; validation audit |
| FR-020 | CMP-011 | DATA-014 | TEST-001 to TEST-007 retained; S01 validator |
