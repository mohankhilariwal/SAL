from __future__ import annotations

import threading

class RunCancelled(RuntimeError):
    pass

class CancellationToken:
    def __init__(self) -> None:
        self._event = threading.Event()
        self.reason = "external_cancellation"

    def cancel(self, reason: str = "external_cancellation") -> None:
        self.reason = reason
        self._event.set()

    @property
    def cancelled(self) -> bool:
        return self._event.is_set()

    def raise_if_cancelled(self) -> None:
        if self.cancelled:
            raise RunCancelled(self.reason)
