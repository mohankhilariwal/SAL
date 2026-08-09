from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..models import AdapterConformanceRecord, TransportDeliveryReceipt


class ProtocolAdapter(ABC):
    profile_id: str

    @abstractmethod
    def deliver(self, payload: dict[str, Any]) -> TransportDeliveryReceipt:
        raise NotImplementedError

    @abstractmethod
    def conformance(self) -> AdapterConformanceRecord:
        raise NotImplementedError
