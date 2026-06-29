from __future__ import annotations

from agentforge.application.observability.service import ObservabilityService
from agentforge.domain.observability import TelemetryEventType, TraceContext
from agentforge.infrastructure.persistence.observability_store import InMemoryObservabilityStore


def test_observability_service_records_event_metric_and_span() -> None:
    store = InMemoryObservabilityStore()
    service = ObservabilityService(store=store)
    context = TraceContext.for_workflow("workflow-1", node_id="node-1")

    event = service.emit_event(
        name="workflow.started",
        event_type=TelemetryEventType.WORKFLOW,
        message="Started.",
        context=context,
    )
    metric = service.increment_counter(name="workflow.started_total", context=context)
    span = service.start_span(name="workflow.run", context=context)
    completed = service.complete_span(span, metadata={"status": "completed"})

    assert store.list_events(trace_id="workflow-1") == (event,)
    assert store.list_metrics(name="workflow.started_total") == (metric,)
    assert store.list_spans(trace_id="workflow-1") == (completed,)
    assert store.list_metrics(name="span.duration_ms")


def test_observability_store_filters_by_trace_and_metric_name() -> None:
    store = InMemoryObservabilityStore()
    service = ObservabilityService(store=store)

    service.emit_event(
        name="workflow.started",
        event_type=TelemetryEventType.WORKFLOW,
        message="Started.",
        context=TraceContext.for_workflow("workflow-a"),
    )
    service.emit_event(
        name="workflow.started",
        event_type=TelemetryEventType.WORKFLOW,
        message="Started.",
        context=TraceContext.for_workflow("workflow-b"),
    )
    service.increment_counter(
        name="workflow.started_total", context=TraceContext.for_workflow("workflow-a")
    )
    service.record_gauge(name="registry.plugins", value=3)

    assert len(store.list_events(trace_id="workflow-a")) == 1
    assert len(store.list_events()) == 2
    assert len(store.list_metrics(name="workflow.started_total")) == 1
    assert len(store.list_metrics()) == 2
