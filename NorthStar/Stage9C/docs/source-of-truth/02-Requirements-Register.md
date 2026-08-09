# 02 — Requirements Register

**Version:** 1.14.0

Preserve all accepted requirements. Add:

| ID | Requirement | Status | Trace |
|---|---|---|---|
| S09C-REQ-001 | Bounded combined scope; no full production control plane claim. | implemented | ADR-104, CP-001, TEST-801/879/880 |
| S09C-REQ-002 | Guardrails at ten stages. | implemented | GR-001, TEST-793–880 |
| S09C-REQ-003 | Compose, never replace, AUTH-001 and BR-001. | implemented | GR-CTL-013/024/025 |
| S09C-REQ-004 | Guardrail allow/evidence authority effect none. | implemented | DATA-196/197, TEST-869/870 |
| S09C-REQ-005 | Hard controls synchronous/non-overrideable. | implemented | policy.py, TEST-795/796/803/804/867 |
| S09C-REQ-006 | Model-assisted controls advisory only. | implemented | GR-CTL-005/034, TEST-797 |
| S09C-REQ-007 | Contain untrusted input/context/tool-result instructions. | implemented | GR-CTL-004/009/010/031/047 |
| S09C-REQ-008 | Evidence provenance, scope, citations and freshness. | implemented | GR-CTL-008/012–017 |
| S09C-REQ-009 | Deny policy/route/agent creation/tier escalation plans. | implemented | GR-CTL-018–023 |
| S09C-REQ-010 | Preserve tool gateway, schemas, approval and one write. | implemented | GR-CTL-024–031 |
| S09C-REQ-011 | Control output approval claims, citations, secrets and tenant scope. | implemented | GR-CTL-032–038 |
| S09C-REQ-012 | Preserve CMP-003 state/Data-106/idempotency/transition invariants. | implemented | GR-CTL-039–043 |
| S09C-REQ-013 | Govern memory tenant/case/provenance/retention/consent. | implemented | GR-CTL-044–049 |
| S09C-REQ-014 | Bind human reviews to identity, role, SoD, digest and expiry. | implemented | GR-CTL-050–055 |
| S09C-REQ-015 | Runtime emergency/bundle/staleness/Stage 8D gates. | implemented | GR-CTL-056–059 |
| S09C-REQ-016 | Govern policy lifecycle and two-human release. | implemented | GOV-001, TEST-863–866 |
| S09C-REQ-017 | Soft-only, scoped, expiring exceptions. | implemented | DATA-207/208, TEST-867/868 |
| S09C-REQ-018 | Immutable local policy distribution and pinning. | implemented | CP-001, DATA-212/213 |
| S09C-REQ-019 | Minimized, digest-based guardrail evidence. | implemented | DATA-197, TEST-869 |
| S09C-REQ-020 | Preserve one agent/current tools/inactive routes. | implemented | TEST-877–879 |
| S09C-REQ-021 | Stage 8D remains unresolved; promotion denied. | implemented | GR-CTL-059, TEST-876/880 |
| S09C-REQ-022 | Threat-model delta. | implemented | TM-001/1.2.0 |
| S09C-REQ-023 | Runnable local package and tests. | implemented | scripts, 88 pytest cases |
| S09C-REQ-024 | Future policy adapter conformance criteria. | designed | ADR-113 |
