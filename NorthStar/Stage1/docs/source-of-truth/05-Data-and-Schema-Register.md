# 05 - Data and Schema Register

**Version:** 0.2.0

## Preserved S00 objects

- `DATA-001 RegulatoryPublication` - source document and immutable provenance; owner CMP-002. **Executable in S01.**
- `DATA-002 RegulatoryCase` - principal business and workflow state; owner CMP-003. **Conceptual; not created in S01.**
- `DATA-003 CandidateObligation` - discrete source-linked obligation candidate; owner CMP-003. **Conceptual; S01 uses source facts, not accepted obligations.**
- `DATA-004 EvidenceReference` - immutable evidence locator and provenance; owner CMP-004. **Executable line-based specialization in S01.**
- `DATA-005 PolicyControlMapping` - conceptual; not implemented.
- `DATA-006 RiskAssessment` - conceptual; not implemented.
- `DATA-007 ReviewDecision` - conceptual append-only human decision; not implemented.
- `DATA-008 RemediationAction` - conceptual; not implemented.
- `DATA-009 AgentRunState` - future checkpointed execution state; not implemented.
- `DATA-010 AuthorizationGrant` - future scoped delegation; not implemented.
- `DATA-011 EvaluationRecord` - versioned evaluation evidence; local test results specialize this concept.
- `DATA-012 AuditEvent` - attributable audit event; S01 stores an invocation record but not a production audit event.
- `DATA-013 ExecutiveSummary` - approved-finding-derived summary; not implemented because S01 output is unapproved.
- `DATA-014 ArchitectureArtefact` - cumulative project record; implemented and updated.

## New S01 objects

### DATA-015 PreliminaryRegulatorySummary

Schema version `1.0.0`. Fields: publication ID/title, executive summary, source facts, candidate affected areas, deadline candidates, missing information, uncertainties, fixed disposition, human-review flag, approval status, legal-conclusion marker, prompt/schema versions.

### DATA-016 SummaryClaim

Fields: statement, kind (`source_fact` or `candidate_interpretation`), one or more `DATA-004` evidence references, concise uncertainty. S01 currently persists only `source_fact` claims in the source-facts collection.

### DATA-017 ModelInvocationRecord

Fields: invocation ID, provider/model, prompt/schema version, start/end timestamps, input SHA-256, success/failure, bounded error metadata and available usage counts.

### DATA-018 PublicationMetadata

Executable metadata projection for `DATA-001`: publication ID, title, source URI, jurisdiction, received timestamp, file name, SHA-256, line count, byte count and schema version.

## Data invariants

1. `DATA-015.disposition` is always `preliminary_unapproved`.
2. `DATA-015.human_review_required` is always true.
3. `DATA-015.approval_status` is always `not_requested` in S01.
4. `DATA-015.legal_conclusion` is always `not_provided`.
5. Every source fact and deadline reference matches `DATA-001` hash, existing lines and exact excerpt.
6. `DATA-015` is not `DATA-013`; it must not be used as an approved executive summary.
7. No `DATA-002` case or `DATA-009` agent state is created.
