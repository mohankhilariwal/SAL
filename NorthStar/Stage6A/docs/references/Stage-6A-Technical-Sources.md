# Stage 6A Technical Sources
**Verification date:** 2026-08-01

1. OpenAI, *A practical guide to building AI agents* (official guide, 2025): incremental approach; maximize one agent first; split only when prompt/tool complexity remains problematic. https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
2. Anthropic, *Building effective agents* (official engineering article, 2024): simple composable patterns and deliberate escalation. https://www.anthropic.com/research/building-effective-agents
3. Anthropic, *How we built our multi-agent research system* (official engineering article, 2025): lead agent plus parallel subagents for a genuinely parallel research workload; workload-specific, not universal. https://www.anthropic.com/engineering/multi-agent-research-system
4. Microsoft, *Agent Framework overview* and *Workflows* (official documentation, current in 2026): separates agent autonomy from graph/workflow control. https://learn.microsoft.com/en-us/agent-framework/overview/ and https://learn.microsoft.com/en-us/agent-framework/workflows/
5. Cemri et al., *Why Do Multi-Agent LLM Systems Fail?* (2025): multi-agent failure taxonomy spanning specification, inter-agent alignment, verification and termination. https://arxiv.org/abs/2503.13657
6. Qian et al., *Towards a Science of Scaling Agent Systems* (preprint, 2025): task/topology-dependent effects; parallel tasks may benefit while sequential tasks may degrade. https://arxiv.org/abs/2512.08296
7. Anthropic, *Demystifying evals for AI agents* (official article, 2026): trajectory errors compound and repeated trials are required. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

**Classification:** least-complexity, explicit contracts and deterministic authority are established engineering practice; framework abstractions are vendor-specific; scaling results are emerging research; NorthStar's exact selection is an architectural inference from its accepted shared state, authority, memory and workflow constraints.
