# Stage 10A Primary Sources — Observability and Audit

**Verification date:** 2026-08-01

NorthStar uses the sources below as engineering references. Standards and specifications are not treated as automatic proof of legal, regulatory or certification compliance.

## Distributed tracing and telemetry

1. **W3C, Trace Context, Recommendation, 23 November 2021.** Defines interoperable `traceparent` and `tracestate` propagation. NorthStar uses these values for correlation only; they are never accepted as authentication, authorization or tenant identity.  
   https://www.w3.org/TR/trace-context/

2. **OpenTelemetry Specification 1.59.0.** Defines the provider-neutral telemetry model and SDK/collector architecture used as the future adapter target.  
   https://opentelemetry.io/docs/specs/otel/

3. **OpenTelemetry Semantic Conventions 1.43.0.** Defines standard attribute naming where stable conventions exist. NorthStar retains a canonical internal schema because GenAI/agent conventions continue to evolve and because audit semantics exceed ordinary telemetry.  
   https://opentelemetry.io/docs/specs/semconv/

4. **OpenTelemetry Logs Data Model.** Defines the stable log record model and trace/log correlation fields.  
   https://opentelemetry.io/docs/specs/otel/logs/data-model/

5. **OpenTelemetry Tracing SDK.** Defines sampling and span-processing semantics. NorthStar applies sampling only to operational telemetry, never to required accountability events.  
   https://opentelemetry.io/docs/specs/otel/trace/sdk/

6. **OpenTelemetry Collector.** Provides a vendor-neutral receiver/processor/exporter pipeline suitable for production adapters. Stage 10A does not deploy a production collector.  
   https://opentelemetry.io/docs/collector/

7. **OpenTelemetry, Handling sensitive data.** Supports minimization, filtering and redaction before export. NorthStar additionally hashes sensitive payloads and records references rather than raw content by default.  
   https://opentelemetry.io/docs/security/handling-sensitive-data/

8. **OpenTelemetry, Generative AI semantic conventions repository.** Used only as an evolving crosswalk; NorthStar does not make runtime correctness depend on unstable vendor- or framework-specific attribute names.  
   https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai

## Logging and accountability

9. **NIST SP 800-92, Guide to Computer Security Log Management, September 2006.** Establishes the operational discipline of log generation, protection, analysis, retention and response.  
   https://csrc.nist.gov/pubs/sp/800/92/final

10. **NIST SP 800-92 Rev. 1 Initial Public Draft, Cybersecurity Log Management Planning Guide, October 2023.** Used as draft planning guidance only; it is not represented as final.  
    https://csrc.nist.gov/pubs/sp/800/92/r1/ipd

11. **NIST SP 800-53 Rev. 5, Update 1.** Audit and accountability, access control, incident response, system integrity and records-related controls are used as a control-design crosswalk, not as a certification claim.  
    https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

## Tamper evidence, signing and trusted time

12. **IETF RFC 5848, Signed Syslog Messages, May 2010.** Demonstrates cryptographic origin authentication, integrity and sequencing for log records. NorthStar’s local HMAC chain is a bounded analogue, not a conforming signed-syslog implementation.  
    https://www.rfc-editor.org/rfc/rfc5848

13. **IETF RFC 3161, Internet X.509 Public Key Infrastructure Time-Stamp Protocol, August 2001.** Identifies a standards-based future option for trusted timestamps. Stage 10A does not operate a time-stamp authority.  
    https://www.rfc-editor.org/rfc/rfc3161

## Source interpretation

- **Established:** W3C trace context, structured logs/metrics/traces, contextual correlation, deterministic redaction, cryptographic hashes, append-only records and independent access controls.
- **Emerging:** GenAI and agent semantic conventions, cross-provider prompt/tool telemetry schemas and standardized agent-operation spans.
- **NorthStar inference:** Separate sampled operational observability from mandatory accountability audit; require durable audit intent/outcome around protected effects; retain business truth in `DATA-106`; and use local provider-neutral schemas with future OpenTelemetry adapters.
- **Not claimed:** WORM compliance, qualified electronic signatures, trusted timestamping, production collector availability, multi-region durability, records-schedule sufficiency, legal admissibility or certification.
