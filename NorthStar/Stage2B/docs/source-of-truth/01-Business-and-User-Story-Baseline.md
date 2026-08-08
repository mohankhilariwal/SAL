# 01 — Business and User Story Baseline

## Context carried from S02A

Maya Chen can inspect immutable, access-labelled NorthStar chunks, but manual inspection of all chunks recreates the original bottleneck. Daniel Brooks asks which passages best support candidate lending, payments and customer-data impacts. Priya Raman must answer without introducing autonomy.

## Personas preserved

| Persona | S02B role |
|---|---|
| Maya Chen — Regulatory Compliance Analyst | Submits evidence queries and inspects ranked citations. |
| Daniel Brooks — Chief Compliance Officer | Requires evidence quality, uncertainty and human accountability. |
| Priya Raman — Enterprise Agentic AI Architect | Selects the bounded retrieval design and preserves stage boundaries. |
| Elena Petrov — AI Platform Engineer | Implements the local retrieval/index contracts and measures latency. |
| Marcus Green — Cybersecurity Architect | Requires authorization before candidate scoring and treats retrieved text as untrusted. |
| Sofia Alvarez — AI Governance and Model Risk Lead | Defines evaluation cases and receives restricted-content access only in a separate negative/positive boundary test. |
| Liam O'Connor — Site Reliability and AgentOps Engineer | Reviews rebuild triggers, operational evidence and failure behavior. |
| Aisha Rahman — Business Process and Controls Owner | Validates source authority and business-domain meaning. |

## User-story status

`US-001` through `US-012` retain their accepted meanings. S02B materially advances the evidence-backed portion of the primary analyst story but does not complete the end-to-end regulatory-change workflow.

- Maya can locate ranked, authorized internal evidence for candidate impacts.
- She can inspect exact source version, lines, excerpt and ranking reasons.
- She cannot accept an obligation, approve a mapping, create a remediation action or route a formal review.
- Daniel remains accountable; the output remains evidence context, not a compliance conclusion.

## Narrative outcome

For the lending query, the local demonstration ranks the Responsible Lending Policy and Regulatory Change Taxonomy first. For payments and customer-data queries, it surfaces the corresponding process/control and taxonomy passages. When Maya asks about the restricted Project Borealis prior assessment, that assessment is neither scored nor returned. When Sofia uses a restricted, appropriately grouped test context, it becomes retrievable. These are synthetic functional outcomes, not legal-quality findings.

## Next unresolved business problem

Evidence is now discoverable, but Maya still performs every external operation manually. The application cannot search a live regulator source, query authoritative enterprise services, save a draft case or send a review request. That is the next business boundary; it is not implemented in S02B.
