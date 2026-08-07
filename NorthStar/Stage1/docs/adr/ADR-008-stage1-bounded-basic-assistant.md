# ADR-008 — Stage 1 Bounded Basic LLM Assistant

- **Status:** Accepted
- **Context:** Maya needs a faster, more consistent first reading of one urgent publication. No internal knowledge retrieval or business action is yet required.
- **Decision:** Implement a single-turn, source-bounded, schema-constrained summarizer with mandatory human review. It is an assistant application, not an agent.
- **Alternatives:** manual only; deterministic rules only; search; RAG; tool-using agent; multi-agent system.
- **Rationale:** The selected design directly addresses semantic summarization while avoiding state, tools, autonomous loops, delegation and coordination overhead.
- **Consequences:** Faster preliminary analysis and reproducible output; residual semantic error and no NorthStar-specific grounding.
- **Risks:** hallucination, prompt injection, automation bias and model/provider variability.
- **Mitigations:** exact citations, fixed disposition, deterministic validation, no tools, human review and offline regression tests.
- **Review trigger:** Maya must compare the publication with internal policies, controls or prior cases.
