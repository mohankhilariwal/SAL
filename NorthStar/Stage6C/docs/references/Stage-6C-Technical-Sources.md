# Stage 6C Technical Sources

Verification date: **2026-08-01**. Primary specifications and maintainer documentation are authoritative for the protocol facts used in this stage.

1. Model Context Protocol, **Specification 2026-07-28** — https://modelcontextprotocol.io/specification/2026-07-28
2. MCP, **Versioning and Compatibility 2026-07-28** — https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning
3. MCP, **Transports 2026-07-28** — https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
4. MCP, **Tools 2026-07-28** — https://modelcontextprotocol.io/specification/2026-07-28/server/tools
5. MCP, **Resources 2026-07-28** — https://modelcontextprotocol.io/specification/2026-07-28/server/resources
6. MCP, **Authorization 2026-07-28** — https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
7. MCP, **Key Changes 2026-07-28** — https://modelcontextprotocol.io/specification/2026-07-28/changelog
8. MCP, **Specification 2025-11-25** (compatibility baseline only) — https://modelcontextprotocol.io/specification/2025-11-25
9. Agent2Agent Protocol, **Latest Specification / v1** — https://a2a-protocol.org/latest/specification/
10. A2A, **Protocol Definitions** — https://a2a-protocol.org/latest/definitions/
11. A2A, **Life of a Task** — https://a2a-protocol.org/latest/topics/life-of-a-task/
12. A2A, **Streaming and Asynchronous Operations** — https://a2a-protocol.org/latest/topics/streaming-and-async/
13. A2A, **What’s New in v1.0** — https://a2a-protocol.org/latest/whats-new-v1/
14. gRPC, **Deadlines** — https://grpc.io/docs/guides/deadlines/
15. gRPC, **Cancellation** — https://grpc.io/docs/guides/cancellation/
16. gRPC, **Status Codes** — https://grpc.io/docs/guides/status-codes/
17. gRPC, **Retry** — https://grpc.io/docs/guides/retry/
18. IETF, **HTTP Semantics, RFC 9110** — https://www.rfc-editor.org/rfc/rfc9110
19. CNCF, **CloudEvents 1.0.2** — https://github.com/cloudevents/spec
20. W3C, **Trace Context Recommendation** — https://www.w3.org/TR/trace-context/
21. Apache Kafka, **Design / delivery semantics** — https://kafka.apache.org/documentation/#design
22. OpenAI Agents SDK, **Handoffs** — https://openai.github.io/openai-agents-python/handoffs/

## Source interpretation

- MCP is treated as a protocol for connecting AI hosts/clients to server-exposed context, resources, prompts and tools. It is not treated as a substitute for NorthStar's full delegated-agent task and termination contract.
- A2A is treated as a candidate mapping target for independent-agent discovery and task lifecycle. Its native objects do not automatically satisfy NorthStar's exact authority, approval-boundary, causation and system-termination invariants; the local conformance profile therefore requires an explicit NorthStar extension.
- HTTP/JSON is used only as a minimal serialized reference transport. It is not claimed as the final production deployment topology.
- gRPC, brokers and framework-native handoffs remain alternatives, not implemented production selections.
