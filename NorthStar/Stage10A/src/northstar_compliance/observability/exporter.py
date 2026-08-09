from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


class ExportUnavailable(RuntimeError):
    pass


class JsonlExporter:
    def __init__(self, path: str | Path, *, fail: bool = False) -> None:
        self.path = Path(path)
        self.fail = fail
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def export(self, records: Iterable[dict[str, Any]]) -> int:
        if self.fail:
            raise ExportUnavailable("telemetry exporter unavailable")
        count = 0
        with self.path.open("a", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
                count += 1
        return count


class BufferedTelemetryPipeline:
    def __init__(self, exporter: JsonlExporter, *, max_buffer: int = 1000) -> None:
        self.exporter = exporter
        self.max_buffer = max_buffer
        self.buffer: list[dict[str, Any]] = []
        self.dropped = 0
        self.last_error: str | None = None

    def submit(self, record: dict[str, Any]) -> None:
        if len(self.buffer) >= self.max_buffer:
            self.buffer.pop(0)
            self.dropped += 1
        self.buffer.append(record)

    def flush(self) -> int:
        if not self.buffer:
            return 0
        snapshot = list(self.buffer)
        try:
            count = self.exporter.export(snapshot)
        except ExportUnavailable as exc:
            self.last_error = str(exc)
            return 0
        self.buffer = self.buffer[count:]
        self.last_error = None
        return count
