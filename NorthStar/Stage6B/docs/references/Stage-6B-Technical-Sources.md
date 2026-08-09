# Stage 6B Technical Sources

Verified 2026-08-01. NorthStar's exact architecture is an inference from its accepted constraints; the sources below inform specific contract and security choices rather than prescribing an agent protocol.

- **[S1] RFC 8693 — OAuth 2.0 Token Exchange (January 2020).** Primary reference for subject/actor semantics and exchanging one security token for another. NorthStar does not implement OAuth in the local sandbox; it maps the future production authority service to these concepts.
- **[S2] RFC 9396 — OAuth 2.0 Rich Authorization Requests (May 2023).** Primary reference for carrying fine-grained authorization details. It supports NorthStar's explicit operation/resource/data-scope fields.
- **[S3] RFC 9449 — OAuth 2.0 Demonstrating Proof of Possession (September 2023).** Primary reference for sender-constrained OAuth tokens and replay resistance. NorthStar records a proof-key identifier but does not claim a DPoP implementation.
- **[S4] RFC 9700 — Best Current Practice for OAuth 2.0 Security (January 2025).** Current OAuth security guidance, including sender-constrained-token considerations.
- **[S5] NIST SP 800-207 — Zero Trust Architecture (August 2020).** Supports explicit policy decision/enforcement, least privilege, per-request evaluation and no implicit trust based on network location.
- **[S6] W3C Trace Context Level 2 (Candidate Recommendation Draft, March 2024).** Supports portable trace correlation using traceparent/tracestate concepts. NorthStar keeps trace/correlation/causation identifiers protocol-neutral.
- **[S7] CloudEvents Specification 1.0.x.** A protocol-neutral event metadata model that informs message identifiers, source/type/time and transport independence. NorthStar does not claim CloudEvents compliance.
- **[S8] Birgisson et al., “Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud,” NDSS 2014.** Research basis for attenuation by adding caveats. NorthStar's HMAC grant is only a teaching analogue and is not a macaroon implementation.
