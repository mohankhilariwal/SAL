# Stage 3A Technical Sources

**Verification date:** 2026-07-31

The Stage 3A implementation is vendor-neutral and local-first. These sources support terminology and protocol comparisons; they do not prove the local implementation is production-ready.

- **[S1] JSON Schema specification.** The official specification page identifies Draft 2020-12 as the current published version and separates Core and Validation. https://json-schema.org/specification
- **[S2] OpenAPI Specification.** Official OAS publication index, including 3.2.0 and 3.1.x, and notes on schema/specification precedence. https://spec.openapis.org/oas/
- **[S3] OpenAI function calling guide.** Official documentation for defining callable functions with JSON schemas and strict-schema behavior. https://developers.openai.com/api/docs/guides/function-calling
- **[S4] Anthropic tool-use implementation guide.** Official documentation describing client-side tools and JSON Schema input definitions. https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use
- **[S5] Model Context Protocol specification, 2025-11-25.** Official specification for hosts, clients, servers, resources, tools, JSON-RPC, capability negotiation, and security principles. https://modelcontextprotocol.io/specification/2025-11-25
- **[S6] NIST, “Lessons Learned from the Consortium: Tool Use in Agent Systems,” 2025-08.** Primary NIST discussion of tool-use categories and agent-system considerations. https://www.nist.gov/news-events/news/2025/08/lessons-learned-consortium-tool-use-agent-systems
- **[S7] OWASP Top 10 for Agentic Applications 2026.** Primary OWASP GenAI Security Project publication describing agentic-system risks, including excessive agency and tool misuse. https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- **[S8] NIST CAISI, “Insights into AI Agent Security from a Large-Scale Red-Teaming Competition.”** Primary NIST report on agent hijacking and security evaluation. https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition

## Architectural interpretation

JSON Schema is used as the internal canonical contract because it can be validated locally and adapted to function-calling or API descriptions later. OpenAPI and MCP are not selected as the Stage 3A runtime because the current implementation is in-process and does not yet need network discovery, transport negotiation, or remote server trust. This is an architectural choice, not a claim that either protocol is unsuitable in general.
