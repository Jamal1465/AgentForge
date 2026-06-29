"""Observability application service for AgentForge.

The service offers a small framework-independent API for emitting telemetry,
metrics, and trace spans. Runtime components depend on this service rather than
on concrete logging, OpenTelemetry, Prometheus, or database libraries.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.application.observability.ports import ObservabilityStore
from agentforge.domain.observability import (
    MetricPoint,
    MetricType,
    SpanRecord,
    TelemetryEvent,
    TelemetryEventType,
    TelemetrySeverity,
    TraceContext,
)


@dataclass(slots=True)
class ObservabilityService:
    """Records operational telemetry through an injected store."""

    store: ObservabilityStore

    def emit_event(
        self,
        *,
        name: str,
        event_type: TelemetryEventType,
        message: str,
        context: TraceContext,
        severity: TelemetrySeverity = TelemetrySeverity.INFO,
        agent_id: str | None = None,
        tool_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> TelemetryEvent:
        """Create and persist a telemetry event."""
        event = TelemetryEvent(
            name=name,
            event_type=event_type,
            severity=severity,
            message=message,
            trace_id=context.trace_id,
            workflow_id=context.workflow_id,
            node_id=context.node_id,
            agent_id=agent_id,
            tool_id=tool_id,
            metadata=metadata or {},
        )
        self.store.record_event(event)
        return event

    def increment_counter(
        self,
        *,
        name: str,
        context: TraceContext | None = None,
        value: float = 1.0,
        labels: dict[str, str] | None = None,
    ) -> MetricPoint:
        """Record a counter metric."""
        return self._record_metric(
            name=name,
            metric_type=MetricType.COUNTER,
            value=value,
            context=context,
            labels=labels,
        )

    def record_gauge(
        self,
        *,
        name: str,
        value: float,
        context: TraceContext | None = None,
        labels: dict[str, str] | None = None,
    ) -> MetricPoint:
        """Record a gauge metric."""
        return self._record_metric(
            name=name,
            metric_type=MetricType.GAUGE,
            value=value,
            context=context,
            labels=labels,
        )

    def record_histogram(
        self,
        *,
        name: str,
        value: float,
        context: TraceContext | None = None,
        labels: dict[str, str] | None = None,
    ) -> MetricPoint:
        """Record a histogram observation."""
        return self._record_metric(
            name=name,
            metric_type=MetricType.HISTOGRAM,
            value=value,
            context=context,
            labels=labels,
        )

    def start_span(
        self,
        *,
        name: str,
        context: TraceContext,
        agent_id: str | None = None,
        tool_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> SpanRecord:
        """Start and persist a trace span."""
        span = SpanRecord(
            name=name,
            trace_id=context.trace_id,
            parent_span_id=context.parent_span_id,
            workflow_id=context.workflow_id,
            node_id=context.node_id,
            agent_id=agent_id,
            tool_id=tool_id,
            metadata=metadata or {},
        )
        self.store.save_span(span)
        return span

    def complete_span(
        self,
        span: SpanRecord,
        *,
        metadata: dict[str, str] | None = None,
    ) -> SpanRecord:
        """Complete an existing trace span and record duration."""
        completed = span.complete(metadata=metadata)
        self.store.save_span(completed)
        if completed.duration_ms is not None:
            self.record_histogram(
                name="span.duration_ms",
                value=completed.duration_ms,
                context=TraceContext(
                    trace_id=completed.trace_id,
                    workflow_id=completed.workflow_id,
                    node_id=completed.node_id,
                    parent_span_id=completed.parent_span_id,
                ),
                labels={"span": completed.name, "status": completed.status.value},
            )
        return completed

    def fail_span(
        self,
        span: SpanRecord,
        *,
        metadata: dict[str, str] | None = None,
    ) -> SpanRecord:
        """Fail an existing trace span and record duration."""
        failed = span.fail(metadata=metadata)
        self.store.save_span(failed)
        if failed.duration_ms is not None:
            self.record_histogram(
                name="span.duration_ms",
                value=failed.duration_ms,
                context=TraceContext(
                    trace_id=failed.trace_id,
                    workflow_id=failed.workflow_id,
                    node_id=failed.node_id,
                    parent_span_id=failed.parent_span_id,
                ),
                labels={"span": failed.name, "status": failed.status.value},
            )
        return failed

    def _record_metric(
        self,
        *,
        name: str,
        metric_type: MetricType,
        value: float,
        context: TraceContext | None,
        labels: dict[str, str] | None,
    ) -> MetricPoint:
        metric = MetricPoint(
            name=name,
            metric_type=metric_type,
            value=value,
            labels=labels or {},
            trace_id=context.trace_id if context is not None else None,
        )
        self.store.record_metric(metric)
        return metric
