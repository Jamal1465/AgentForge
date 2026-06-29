from __future__ import annotations

import pytest

from agentforge.domain.observability import (
    MetricPoint,
    MetricType,
    ObservabilityDomainError,
    SpanRecord,
    SpanStatus,
    TelemetryEvent,
    TelemetryEventType,
    TelemetrySeverity,
    TraceContext,
)


def test_trace_context_uses_workflow_id_as_trace_id() -> None:
    context = TraceContext.for_workflow("workflow-1", node_id="node-1")

    assert context.trace_id == "workflow-1"
    assert context.workflow_id == "workflow-1"
    assert context.node_id == "node-1"


def test_telemetry_event_validates_required_text() -> None:
    with pytest.raises(ObservabilityDomainError):
        TelemetryEvent(
            name=" ",
            event_type=TelemetryEventType.WORKFLOW,
            severity=TelemetrySeverity.INFO,
            message="Started.",
            trace_id="trace-1",
        )


def test_metric_point_rejects_negative_value() -> None:
    with pytest.raises(ObservabilityDomainError):
        MetricPoint(name="workflow.count", metric_type=MetricType.COUNTER, value=-1)


def test_span_record_can_complete_with_duration() -> None:
    span = SpanRecord(name="workflow.run", trace_id="trace-1")

    completed = span.complete(metadata={"status": "ok"})

    assert completed.status == SpanStatus.COMPLETED
    assert completed.duration_ms is not None
    assert completed.metadata["status"] == "ok"
