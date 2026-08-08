# Stage 3C Technical Sources

**Verification date:** 2026-07-31. Primary or official sources were preferred.

- **[S1] Python documentation — Coroutines and Tasks.** Cancellation is cooperative; cancellation raises `CancelledError` at an await point, and structured concurrency has explicit cancellation semantics. https://docs.python.org/3/library/asyncio-task.html
- **[S2] Amazon Builders’ Library — Timeouts, retries, and backoff with jitter.** Timeouts bound waiting; retries can recover transient faults but can also amplify load; backoff and jitter reduce synchronized retry storms. https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- **[S3] Amazon Builders’ Library — Making retries safe with idempotent APIs.** Stable request identifiers and idempotent API design allow clients to retry without duplicating intended effects. https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- **[S4] Google Cloud Storage documentation — Retry strategy.** Retry safety depends on both the response/failure and request idempotency; non-idempotent actions can cause races or duplicate effects. https://cloud.google.com/storage/docs/retry-strategy
- **[S5] RFC 9110 — HTTP Semantics, §9.2.2.** Idempotency means multiple identical requests have the same intended server effect as one request; logging/history may still differ. https://www.rfc-editor.org/rfc/rfc9110.html
- **[S6] Python `os` documentation.** `os.fsync` forces file data to disk and `os.replace` provides replacement semantics used by the local checkpoint implementation. https://docs.python.org/3/library/os.html
- **[S7] OpenTelemetry Semantic Conventions 1.43.0 and GenAI guidance.** Token usage attributes exist but GenAI semantic conventions remain in movement/development; NorthStar therefore keeps its internal budget contract provider-neutral. https://opentelemetry.io/docs/specs/semconv/
- **[S8] Temporal documentation.** Durable execution systems can resume workflows after failures; Stage 3C deliberately does not claim those distributed guarantees and uses a local checkpoint only. https://docs.temporal.io/

## Source interpretation

The retry/idempotency sources describe distributed API principles. NorthStar applies them architecturally to its tool gateway; this mapping is an architectural inference, not a claim that the tutorial’s local tools are HTTP or cloud-storage APIs. The local checkpoint uses standard-library primitives but does not provide database transactions, directory fsync guarantees on every filesystem, cryptographic signatures or enterprise durability.
