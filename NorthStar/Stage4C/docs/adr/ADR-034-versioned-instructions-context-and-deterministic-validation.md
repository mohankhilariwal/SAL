# ADR-034 — Versioned Instructions, Bounded Context and Deterministic Validation

- **Status:** Accepted
- **Context:** Prompt text, context loading and validation are not repeatable or consistently bounded.
- **Decision:** Bind a hashed instruction bundle and a provenance-bearing, access-filtered, size-bounded context envelope into a versioned harness manifest; run deterministic validators at lifecycle boundaries.
- **Alternatives:** One large prompt; dynamic unversioned prompt assembly; rely on model refusal; move policy into instructions.
- **Rationale:** Reproducibility and context economics improve while critical authority remains outside model reasoning.
- **Consequences:** Configuration changes require version/hash updates; context sources require typed adapters and provenance.
- **Risks:** Stale instructions, context truncation and false confidence from a valid hash.
- **Mitigations:** Evaluation, change review, omitted-source evidence, access-before-loader tests and explicit statement that hashes prove integrity, not correctness.
- **Review trigger:** Formal specification stage, model/prompt registry adoption, context compression or memory introduction.
