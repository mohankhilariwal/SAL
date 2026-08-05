# Policy catalogue

Policy version: `2026.08.1`.

| Policy ID | Rule | Code | Principal tests | Evidence/UI |
|---|---|---|---|---|
| POL-ID-001 | active requester and role | `policy_python/engine.py` | `test_policy_engine.py` | identity, decision tab |
| POL-AUTH-001 | request-specific delegated authority | workflow + PDP | policy/acceptance | delegated authority JSON |
| POL-PUR-001 | approved purpose | PDP | policy/acceptance | request + policy decision |
| POL-DATA-001 | column/row scope | workflow + PDP | classification/injection | classification screen |
| POL-PII-001 | direct identifiers prohibited | classification + export | classification/export | field classification JSON |
| POL-TOOL-001 | tool allow-list and constraints | injection + PDP | injection/scenario 4 | security events |
| POL-PRIV-001 | privacy thresholds | evaluators + PDP | privacy/scenario 3 | privacy report |
| POL-UTIL-001 | minimum utility | evaluators + PDP | policy/scenario 1 | utility report |
| POL-RECIP-001 | named recipient boundary | workflow + PDP | scenarios | recipient assessment |
| POL-APP-001 | independent approvals | workflow + PDP | approvals/scenario 2 | approval history/card |
| POL-EXP-001 | destination allow-list | export gateway + PDP | export/injection | receipt or denial |
| POL-EVID-001 | evidence completeness | evidence + PDP + gateway | evidence/acceptance | artifact table |
| POL-BUD-001 | rows/runtime/retries/model budget | settings + workflow + PDP | policy | generation screen |
| POL-RET-001 | expiry and retention | request + receipt | policy/acceptance | dataset card/receipt |
| POL-INJ-001 | injection/authority violation | injection + PDP | injection/scenario 4 | security timeline |
| POL-KILL-001 | kill-switch enforcement | store + PDP + gateway | kill switch | decision screen |

The Python PDP is the default. The OPA adapter executes the sample Rego when the binary is present and normalizes through the same typed decision contract; tests never require OPA.
