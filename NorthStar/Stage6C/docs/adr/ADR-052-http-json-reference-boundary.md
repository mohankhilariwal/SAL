# ADR-052 — Select a Sequential HTTP/JSON Reference Boundary, Not a Production Topology

- **Status:** Accepted
- **Context:** The local direct sandbox did not prove serialization, process isolation or receiver-side validation.
- **Decision:** Implement one synchronous HTTP/JSON request across a separate local process. Carry exact contract version, content digest, authority digest and correlation headers. Disable retries and concurrency.
- **Alternatives:** Direct calls; REST product API; gRPC; broker; framework handoff; A2A endpoint.
- **Rationale:** Smallest implementation that proves the canonical semantics survive a real boundary.
- **Consequences:** Provides evidence for serialization and PEP placement but not durability, scale or production security.
- **Risks:** Mistaken promotion of the reference server into production.
- **Mitigations:** Loopback default, explicit warnings, no TLS/IAM claim, status `selected_reference_boundary`.
- **Review trigger:** Deployment topology, SLOs or independent lifecycle require a production transport.
