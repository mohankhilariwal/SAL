# Stage 4C Technical Sources

Verified 2026-07-31. These sources map representative framework/runtime capabilities; NorthStar's selected implementation remains framework-neutral and standard-library-only.

1. OpenAI Agents SDK — overview, context, tools, guardrails, tracing and human-in-the-loop: https://openai.github.io/openai-agents-python/
2. LangGraph — runtime context, persistence/checkpointers and runtime: https://docs.langchain.com/oss/python/langgraph/
3. Microsoft Agent Framework overview (updated 2026-04-06) and migration guidance (updated 2026-07-10): https://learn.microsoft.com/en-us/agent-framework/overview/
4. OpenTelemetry Semantic Conventions 1.43.0 and GenAI observability material: https://opentelemetry.io/docs/specs/semconv/

Important interpretation: framework sessions, persistence, guardrails and tracing are product/runtime features, not proof that prompts enforce authorization, that traces are audit ledgers or that a local adapter has distributed durability.
