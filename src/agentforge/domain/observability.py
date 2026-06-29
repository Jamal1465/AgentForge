"""Pure domain model for AgentForge observability and telemetry.

Observability is capability-first and plugin-neutral. The core platform records
workflow, task, plugin, tool, security, memory, and evaluation signals without
knowing concrete agent implementations such as backend, frontend, or database
agents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class ObservabilityDomainError(ValueError):
    """Raised when observability domain objects violate invariants."""


class TelemetrySeverity(StrEnum):
    """Severity level for operational events."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class TelemetryEventType(StrEnum):
    """High-level category of an emitted telemetry event."""

    WORKFLOW = "workflow"
    NODE = "node"
    ROUTING = "routing"
    PLUGIN = "plugin"
    TOOL = "tool"
    SECURITY = "security"
    EVALUATION = "evaluation"
    MEMORY = "memory"
    SYSTEM = "system"


class MetricType(StrEnum):
    """Supported metric point types."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


class SpanStatus(StrEnum):
    """Lifecycle state for trace spans."""

    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class TraceContext:
    """Correlation identifiers propagated through a workflow execution."""

    trace_id: str
    workflow_id: str | None = None
    node_id: str | None = None
    parent_span_id: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.trace_id, "Trace ID")
        if self.workflow_id is not None:
            _require_text(self.workflow_id, "Workflow ID")
        if self.node_id is not None:
            _require_text(self.node_id, "Node ID")
        if self.parent_span_id is not None:
            _require_text(self.parent_span_id, "Parent span ID")

    @classmethod
    def for_workflow(cls, workflow_id: str, *, node_id: str | None = None) -> TraceContext:
        """Create a deterministic trace context for one workflow."""
        return cls(trace_id=workflow_id, workflow_id=workflow_id, node_id=node_id)

    def for_node(self, node_id: str) -> TraceContext:
        """Return a copy of this context scoped to a workflow node."""
        return TraceContext(
            trace_id=self.trace_id,
            workflow_id=self.workflow_id,
            node_id=node_id,
            parent_span_id=self.parent_span_id,
        )


@dataclass(frozen=True, slots=True)
class TelemetryEvent:
    """Immutable operational event emitted by AgentForge runtime components."""

    name: str
    event_type: TelemetryEventType
    severity: TelemetrySeverity
    message: str
    trace_id: str
    workflow_id: str | None = None
    node_id: str | None = None
    agent_id: str | None = None
    tool_id: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        _require_text(self.name, "Telemetry event name")
        _require_text(self.message, "Telemetry event message")
        _require_text(self.trace_id, "Telemetry event trace ID")
        _require_text(self.event_id, "Telemetry event ID")
        _validate_optional_text(self.workflow_id, "Workflow ID")
        _validate_optional_text(self.node_id, "Node ID")
        _validate_optional_text(self.agent_id, "Agent ID")
        _validate_optional_text(self.tool_id, "Tool ID")
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class MetricPoint:
    """Single metric observation emitted by runtime components."""

    name: str
    metric_type: MetricType
    value: float
    labels: dict[str, str] = field(default_factory=dict)
    trace_id: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    metric_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        _require_text(self.name, "Metric name")
        _require_text(self.metric_id, "Metric ID")
        if self.value < 0:
            raise ObservabilityDomainError("Metric value cannot be negative.")
        _validate_optional_text(self.trace_id, "Metric trace ID")
        object.__setattr__(self, "labels", _normalize_metadata(self.labels))


@dataclass(frozen=True, slots=True)
class SpanRecord:
    """Trace span representing the duration of a runtime operation."""

    name: str
    trace_id: str
    span_id: str = field(default_factory=lambda: str(uuid4()))
    parent_span_id: str | None = None
    workflow_id: str | None = None
    node_id: str | None = None
    agent_id: str | None = None
    tool_id: str | None = None
    status: SpanStatus = SpanStatus.STARTED
    start_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    end_time: datetime | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.name, "Span name")
        _require_text(self.trace_id, "Span trace ID")
        _require_text(self.span_id, "Span ID")
        _validate_optional_text(self.parent_span_id, "Parent span ID")
        _validate_optional_text(self.workflow_id, "Workflow ID")
        _validate_optional_text(self.node_id, "Node ID")
        _validate_optional_text(self.agent_id, "Agent ID")
        _validate_optional_text(self.tool_id, "Tool ID")
        if self.end_time is not None and self.end_time < self.start_time:
            raise ObservabilityDomainError("Span end time cannot be before start time.")
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))

    @property
    def duration_ms(self) -> float | None:
        """Return span duration in milliseconds when the span has ended."""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds() * 1000

    def complete(self, *, metadata: dict[str, str] | None = None) -> SpanRecord:
        """Return a completed copy of this span."""
        return self._finish(SpanStatus.COMPLETED, metadata=metadata)

    def fail(self, *, metadata: dict[str, str] | None = None) -> SpanRecord:
        """Return a failed copy of this span."""
        return self._finish(SpanStatus.FAILED, metadata=metadata)

    def _finish(
        self,
        status: SpanStatus,
        *,
        metadata: dict[str, str] | None = None,
    ) -> SpanRecord:
        merged_metadata = dict(self.metadata)
        if metadata:
            merged_metadata.update(metadata)
        return SpanRecord(
            name=self.name,
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_span_id=self.parent_span_id,
            workflow_id=self.workflow_id,
            node_id=self.node_id,
            agent_id=self.agent_id,
            tool_id=self.tool_id,
            status=status,
            start_time=self.start_time,
            end_time=datetime.now(UTC),
            metadata=merged_metadata,
        )


def _require_text(value: str, label: str) -> None:
    if not value.strip():
        raise ObservabilityDomainError(f"{label} cannot be empty.")


def _validate_optional_text(value: str | None, label: str) -> None:
    if value is not None and not value.strip():
        raise ObservabilityDomainError(f"{label} cannot be blank.")


def _normalize_metadata(values: dict[str, str]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in values.items():
        clean_key = str(key).strip()
        if not clean_key:
            raise ObservabilityDomainError("Metadata keys cannot be empty.")
        normalized[clean_key] = str(value)
    return normalized
