# ADR-009 — Provider-Neutral Model Contract

- **Status:** Accepted
- **Context:** Stage 1 needs a real managed-model option without making the repository or schemas vendor-specific.
- **Decision:** Define a minimal `SummaryModel` protocol. Provide a deterministic offline test double and an optional OpenAI Responses API adapter behind the contract.
- **Alternatives:** hard-code one SDK; use only a mock; self-host a model in Stage 1.
- **Rationale:** Provider isolation preserves portability and makes local tests reproducible while retaining a real LLM path.
- **Consequences:** Adapter-specific behavior still requires separate verification; the mock proves application behavior, not semantic model quality.
- **Risks:** schema/API drift, provider retention settings, cost and unavailable credentials.
- **Mitigations:** environment variables, `store=false`, no default model name, recorded verification boundary and change-controlled adapter tests.
- **Review trigger:** production provider selection, data-residency requirement or model-routing requirement.
