# Stage 9B Primary Sources

Verified 2026-08-01. Standards status and vendor implementation support must be rechecked before production procurement or deployment.

- **R1 - IETF RFC 9700, Best Current Practice for OAuth 2.0 Security (January 2025).** Current OAuth security BCP; used for the baseline that sensitive deployments must avoid known insecure patterns and use defense in depth. https://www.rfc-editor.org/info/rfc9700/
- **R2 - IETF RFC 8693, OAuth 2.0 Token Exchange (January 2020).** Defines a security token service pattern for exchanging tokens, including delegation and impersonation semantics. https://www.rfc-editor.org/info/rfc8693/
- **R3 - IETF RFC 9449, OAuth 2.0 Demonstrating Proof of Possession (September 2023).** Defines application-layer sender-constrained OAuth tokens and replay detection using proof-of-possession. https://www.rfc-editor.org/info/rfc9449/
- **R4 - IETF RFC 8705, OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens (February 2020).** Defines mTLS client authentication and certificate-bound access tokens. https://www.rfc-editor.org/info/rfc8705/
- **R5 - IETF RFC 9068, JWT Profile for OAuth 2.0 Access Tokens (October 2021).** Interoperable signed JWT access-token profile and receiver validation guidance. https://www.rfc-editor.org/info/rfc9068/
- **R6 - IETF RFC 7009, OAuth 2.0 Token Revocation (August 2013).** Revocation endpoint semantics and cascading considerations. https://www.rfc-editor.org/info/rfc7009/
- **R7 - IETF RFC 7662, OAuth 2.0 Token Introspection (October 2015).** Protected-resource query for current token state and metadata. https://www.rfc-editor.org/info/rfc7662/
- **R8 - IETF RFC 8707, Resource Indicators for OAuth 2.0 (February 2020).** Resource/audience targeting for access tokens. https://www.rfc-editor.org/info/rfc8707/
- **R9 - IETF RFC 9396, OAuth 2.0 Rich Authorization Requests (May 2023).** Structured authorization details for fine-grained operations and resources. https://www.rfc-editor.org/info/rfc9396/
- **R10 - OpenID Connect Core 1.0 Final (February 2014).** Authentication layer over OAuth 2.0 and stable end-user subject claims. https://openid.net/specs/openid-connect-core-1_0-final.html
- **R11 - NIST SP 800-207, Zero Trust Architecture (August 2020).** No implicit trust based on network location; authenticate and authorize before resource access. https://csrc.nist.gov/pubs/sp/800/207/final
- **R12 - NIST SP 800-207A, Zero Trust Access Control for Cloud-Native Applications (September 2023).** Application/service identity, identity-tier policy, API gateways, sidecars and granular policy enforcement. https://csrc.nist.gov/pubs/sp/800/207/a/final
- **R13 - NIST SP 800-162, Guide to ABAC (updated August 2019).** Authorization based on subject, object, action and environmental attributes. https://csrc.nist.gov/pubs/sp/800/162/upd2/final
- **R14 - SPIFFE Concepts and Specifications.** Workload identity and SVID concepts; used as a production workload-identity mapping, not as an implemented NorthStar service. https://spiffe.io/docs/latest/spiffe/concepts/
- **R15 - SPIRE Concepts.** Attestation and issuance implementation for SPIFFE identities; production design option only. https://spiffe.io/docs/latest/spire-about/spire-concepts/
- **R16 - Birgisson et al., Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud (2014).** Primary research for attenuated, caveat-bearing authorization credentials. https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/
- **R17 - Pang et al., Zanzibar: Google's Consistent, Global Authorization System (USENIX ATC 2019).** Primary research for relationship-based authorization at scale. https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/
- **R18 - Open Policy Agent documentation.** Example of a general-purpose policy decision engine and local/sidecar enforcement trade-offs. https://www.openpolicyagent.org/docs/

## Source interpretation

OAuth, OIDC, SPIFFE, DPoP, mTLS, JWT, macaroons and Zanzibar are not interchangeable. OIDC authenticates a human and communicates identity claims; OAuth delegates API access; token exchange derives a new token for a target context; SPIFFE identifies workloads; DPoP and mTLS sender-constrain tokens; macaroons are a capability-style attenuation construction; Zanzibar describes a relationship-oriented authorization system. NorthStar combines concepts architecturally but does not claim that one token format solves every identity, authorization, policy, approval, budget and audit requirement.

- **R-S09A - Supplied NorthStar Stage 9A Threat Modelling Handoff Pack (2026-08-01).** Authoritative reconstruction basis for architecture `1.12.0`, current invariants and the unresolved identity/authorization problem.
