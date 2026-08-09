# 05 — Data and Schema Register

**Version:** 1.14.0

Preserve `DATA-001`–`192`, `INT-001`–`154` and `TOOL-001`–`006`. Add:

## Data objects

| ID | Object | Owner | Notes |
|---|---|---|---|
| DATA-193 | GuardrailPolicy | CMP-007/011 | Single control metadata; authority none. |
| DATA-194 | GuardrailPolicyBundle | CMP-011 | Immutable released control set and digest. |
| DATA-195 | GuardrailDecisionRequest | PEP owner | Bounded stage attributes/payload. |
| DATA-196 | GuardrailDecision | PEP owner | Allow/deny/quarantine/review for current stage only; authority none. |
| DATA-197 | GuardrailEvidence | CMP-009 | Minimized identifiers/digests/reason codes. |
| DATA-198 | InputSafetyAssessment | CMP-002 | Intake disposition. |
| DATA-199 | ContextAssemblyManifest | CMP-003 | Source provenance/isolation/budget. |
| DATA-200 | RetrievalGuardrailAssessment | CMP-004 | Scope/limits/citations/freshness. |
| DATA-201 | PlanGuardrailAssessment | CMP-003 | Action/tier/step constraints. |
| DATA-202 | ToolGuardrailAssessment | CMP-005 | AUTH/BR/gateway/schema/approval/result. |
| DATA-203 | OutputGuardrailAssessment | CMP-003/008 | Schema/evidence/approval/tenant/secrets. |
| DATA-204 | StateMutationGuardrailAssessment | CMP-003 | Does not mutate state itself. |
| DATA-205 | MemoryWriteGuardrailAssessment | CMP-003 | Does not write memory itself. |
| DATA-206 | HumanReviewControlRecord | CMP-006 | References an actual human decision. |
| DATA-207 | PolicyExceptionRequest | CMP-011 | Soft-control request only. |
| DATA-208 | PolicyExceptionDecision | human governance owners | Scoped/expiring/compensated. |
| DATA-209 | GuardrailControlOwnerRecord | CMP-011 | Owner/RACI/review triggers. |
| DATA-210 | PolicyChangeSet | CMP-011 | Change rationale/impact. |
| DATA-211 | PolicyTestResult | CMP-008 | Validation/regression evidence. |
| DATA-212 | PolicyReleaseManifest | CMP-011 | Immutable digest and approvers. |
| DATA-213 | PolicyDistributionReceipt | CMP-010/PEP | Local cache receipt/pin. |
| DATA-214 | GuardrailIncidentRecord | CMP-009/011 | Detection/containment/recovery. |
| DATA-215 | GuardrailSnapshot | CMP-011 | Architecture/policy/control snapshot. |
| DATA-216 | Stage9CReport | CMP-008/011 | Stage report/evaluation status. |

JSON schemas: `schemas/DATA-193.schema.json` through `DATA-216.schema.json`. Every schema requires `authority_effect: none`.

## Interfaces

| ID | Interface |
|---|---|
| INT-155 | Evaluate input guardrails |
| INT-156 | Quarantine/release intake artefact |
| INT-157 | Build/validate context manifest |
| INT-158 | Evaluate retrieval guardrails |
| INT-159 | Evaluate plan guardrails |
| INT-160 | Evaluate tool guardrails |
| INT-161 | Validate tool-result envelope |
| INT-162 | Evaluate output guardrails |
| INT-163 | Evaluate state-mutation guardrails |
| INT-164 | Evaluate memory-write guardrails |
| INT-165 | Validate human-review control record |
| INT-166 | Submit policy change set |
| INT-167 | Validate policy schema/invariants |
| INT-168 | Execute policy test suite |
| INT-169 | Approve/release immutable policy bundle |
| INT-170 | Register/distribute policy bundle |
| INT-171 | Acknowledge/pin bundle receipt |
| INT-172 | Request/decide policy exception |
| INT-173 | Emit minimized guardrail evidence |
| INT-174 | Raise/contain guardrail incident |
| INT-175 | Export guardrail snapshot/report |
| INT-176 | Validate Stage 9C consistency |
