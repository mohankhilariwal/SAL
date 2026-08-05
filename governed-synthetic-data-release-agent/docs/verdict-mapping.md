# VERDICT control-to-code mapping

| VERDICT area | Implemented controls | Policy/code | Test/evidence/UI |
|---|---|---|---|
| Identity | requester, agent, approver, recipient | POL-ID-001, POL-AUTH-001; workflow/models | approval/security tests; identity JSON; request tab |
| Validation | sensitive detection, utility, privacy, intended use | POL-PII-001, POL-PRIV-001, POL-UTIL-001, POL-PUR-001 | classification/privacy/acceptance; reports; tabs 2/4 |
| Evidence | profiles, lineage, generation config, reports, approvals, receipt | POL-EVID-001; EvidenceBuilder | evidence verifier; ZIP/manifest; tab 5 |
| Runtime Control | source scope, tool mediation, quarantine, allow-list, suspension | POL-DATA-001, POL-TOOL-001, POL-EXP-001, POL-KILL-001 | injection/export/kill tests; timeline |
| Decisioning | allow, approval, deny, quarantine, regenerate | PythonPolicyEngine | policy/acceptance; decision tab |
| Cost and Compliance | row/runtime/model limits, expiry, purpose, recipient | POL-BUD-001, POL-RET-001, POL-PUR-001, POL-RECIP-001 | settings/policy; plan and receipt |
| Transparency | dataset summary, rationale, limitations, scores, trace | evidence summary + typed decision | evidence tests; tabs 4/5 |

This mapping is an implementation traceability aid, not a certification.
