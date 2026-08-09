# ADR-062 — Distribution-first, joint ISL/OSL workload modelling

- **Status:** Accepted
- **Context:** Fixed token lengths hide NorthStar's short, long and tail workloads and can produce unsafe capacity conclusions.
- **Decision:** Model each profile as a versioned weighted mixture of joint ISL/OSL buckets plus model-call, tool-call, retrieval-call and turn distributions. Record tokenizer identity and profile digest.
- **Alternatives:** One fixed length; independent marginal ISL and OSL distributions; production trace only.
- **Rationale:** Joint mixtures retain meaningful correlation, remain understandable to architects and can bootstrap before production traces exist.
- **Consequences:** More configuration and validation; capacity results are profile-specific.
- **Risks:** Synthetic mixtures may not resemble reality.
- **Mitigations:** Prefer trace replay when available; compare measured quantiles and correlations; version every profile.
- **Review trigger:** Material traffic, tokenizer, graph, prompt, model or document-mix change.
