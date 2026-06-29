"""In-memory observability store for tests and local development."""

from __future__ import annotations

from dataclasses import dataclass, field

from agentforge.application.observability.ports import ObservabilityStore
from agentforge.domain.observability import MetricPoint, SpanRecord, TelemetryEvent


class ObservabilityStoreError(RuntimeError):
    """Raised when observability persistence fails."""


@dataclass(slots=True)
class InMemoryObservabilityStore(ObservabilityStore):
    """Deterministic in-memory store for telemetry events, metrics, and spans."""

    _events: list[TelemetryEvent] = field(default_factory=list)
    _metrics: list[MetricPoint] = field(default_factory=list)
    _spans: dict[str, SpanRecord] = field(default_factory=dict)

    def record_event(self, event: TelemetryEvent) -> None:
        if any(existing.event_id == event.event_id for existing in self._events):
            raise ObservabilityStoreError(f"Telemetry event already recorded: {event.event_id}")
        self._events.append(event)

    def record_metric(self, metric: MetricPoint) -> None:
        if any(existing.metric_id == metric.metric_id for existing in self._metrics):
            raise ObservabilityStoreError(f"Metric already recorded: {metric.metric_id}")
        self._metrics.append(metric)

    def save_span(self, span: SpanRecord) -> None:
        self._spans[span.span_id] = span

    def list_events(self, *, trace_id: str | None = None) -> tuple[TelemetryEvent, ...]:
        events = tuple(self._events)
        if trace_id is None:
            return events
        return tuple(event for event in events if event.trace_id == trace_id)

    def list_metrics(self, *, name: str | None = None) -> tuple[MetricPoint, ...]:
        metrics = tuple(self._metrics)
        if name is None:
            return metrics
        return tuple(metric for metric in metrics if metric.name == name)

    def list_spans(self, *, trace_id: str | None = None) -> tuple[SpanRecord, ...]:
        spans = tuple(self._spans.values())
        if trace_id is None:
            return spans
        return tuple(span for span in spans if span.trace_id == trace_id)
