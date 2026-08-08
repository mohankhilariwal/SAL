# ADR-017 — Exact Citations and Retrieval-First RAG Evaluation

- **Status:** Accepted
- **Context:** A plausible answer is insufficient for regulatory impact analysis. Evidence must be reconstructable, and the retrieval subsystem must be evaluated independently from any model generator.
- **Decision:** Build citations only from immutable chunk/source-version identifiers, normalized source hash and exact line coordinates; independently validate excerpts. Evaluate retrieval precision, recall, reciprocal rank, citation correctness, forbidden hits, duplicate spans and latency. Defer faithfulness and answer-relevance claims until a generation contract is implemented.
- **Alternatives:** model-written citations; URL-only attribution; answer-only evaluation; LLM-as-a-judge at this stage.
- **Rationale:** Deterministic citation integrity and retrieval metrics isolate defects before a probabilistic generator can mask them.
- **Consequences:** S02B returns cited context, not an accepted impact assessment or generated answer.
- **Risks:** exact citations can still support an incorrect interpretation; small synthetic labels can overstate quality.
- **Mitigations:** candidate-only semantics, permission cases, transparent metric denominators and future human labeling.
- **Review trigger:** grounded generation, production data, model-based evaluation or legal/compliance pilot.
