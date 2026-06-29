"""Application ports for observability persistence."""

from __future__ import annotations

from typing import Protocol

from agentforge.domain.observability import MetricPoint, SpanRecord, TelemetryEvent


class ObservabilityStore(Protocol):
    """Persistence boundary for telemetry events, metrics, and trace spans."""

    def record_event(self, event: TelemetryEvent) -> None:
        """Persist one telemetry event."""
        ...

    def record_metric(self, metric: MetricPoint) -> None:
        """Persist one metric point."""
        ...

    def save_span(self, span: SpanRecord) -> None:
        """Persist or update one trace span."""
        ...

    def list_events(self, *, trace_id: str | None = None) -> tuple[TelemetryEvent, ...]:
        """Return events, optionally filtered by trace ID."""
        ...

    def list_metrics(self, *, name: str | None = None) -> tuple[MetricPoint, ...]:
        """Return metrics, optionally filtered by metric name."""
        ...

    def list_spans(self, *, trace_id: str | None = None) -> tuple[SpanRecord, ...]:
        """Return spans, optionally filtered by trace ID."""
        ...
