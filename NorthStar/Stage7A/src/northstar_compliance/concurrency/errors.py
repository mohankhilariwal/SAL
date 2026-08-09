"""Stage 7A exception types."""


class ConcurrencyError(RuntimeError):
    """Base class for concurrency-runtime errors."""


class AdmissionRejected(ConcurrencyError):
    """Raised when bounded admission cannot accept work before its timeout."""


class AuthorityInvariantViolation(ConcurrencyError):
    """Raised when work would violate an accepted NorthStar authority boundary."""


class IdempotencyConflict(ConcurrencyError):
    """Raised when one idempotency key is reused for different canonical input."""


class TransientBranchError(ConcurrencyError):
    """A retryable read-only or pure-compute branch failure."""


class PermanentBranchError(ConcurrencyError):
    """A non-retryable branch failure."""
