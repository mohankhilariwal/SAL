# Stage 5B Technical Sources

Verified 2026-08-01. Primary or official sources are preferred. Vendor guidance is used as an implementation reference, not an industry standard.

1. **NorthStar Stage 5A Handoff Pack** — supplied project baseline. `docs/baseline/Stage-5A-Handoff-Pack-supplied.md`.
2. **Anthropic, “Effective context engineering for AI agents”** (2025-09-29). https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
3. **Anthropic, “Effective harnesses for long-running agents”** (2025-11-26). https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
4. **Liu et al., “Lost in the Middle: How Language Models Use Long Contexts”** (TACL 2024; arXiv 2023). https://arxiv.org/abs/2307.03172
5. **Packer et al., “MemGPT: Towards LLMs as Operating Systems”** (2023/2024). https://arxiv.org/abs/2310.08560
6. **Park et al., “Generative Agents: Interactive Simulacra of Human Behavior”** (2023). https://arxiv.org/abs/2304.03442
7. **LangChain/LangGraph documentation, “Memory overview”** (accessed 2026-08-01). https://docs.langchain.com/oss/python/concepts/memory
8. **NIST AI Risk Management Framework and Playbook** (AI RMF 1.0; Playbook page updated 2026-06-10). https://www.nist.gov/itl/ai-risk-management-framework and https://airc.nist.gov/airmf-resources/playbook/
9. **NIST AI RMF Playbook — Govern** (data provenance and documentation prompts). https://airc.nist.gov/airmf-resources/playbook/govern/
10. **NIST Privacy Framework** (data lifecycle from collection through disposal). https://www.nist.gov/privacy-framework
11. **Office of the Privacy Commissioner of Canada, PIPEDA Fair Information Principle 5 — Limiting Use, Disclosure, and Retention**. https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/principles/p_use/
12. **Office of the Privacy Commissioner of Canada, PIPEDA Fair Information Principle 7 — Safeguards**. https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/principles/p_safeguards/
13. **Regulation (EU) 2016/679, Article 5 and Article 17** (storage limitation and erasure; legal applicability requires counsel). https://eur-lex.europa.eu/eli/reg/2016/679/oj
14. **OWASP AI Agent Security Cheat Sheet** (memory poisoning and agent security controls). https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
15. **OWASP Agentic AI — Threats and Mitigations / Top 10 for Agentic Applications 2026**. https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ and https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

## Source interpretation notes

- Memory taxonomies are useful conceptual aids but do not imply that every system requires every memory type.
- MemGPT and generative-agent research demonstrate possible memory architectures; they do not establish that unconstrained model-written memory is suitable for regulated enterprise workflows.
- Privacy sources support purpose limitation, retention, accuracy, safeguards and deletion principles. This playbook does not provide legal conclusions or select a lawful basis.
- The local implementation uses character budgets and local JSON files. Production token accounting, IAM/PDP, KMS, database isolation, backup erasure, legal hold and records schedules remain unresolved.
