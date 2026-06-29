"""Observability wrapper for AgentForge tool execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from agentforge.application.observability.service import ObservabilityService
from agentforge.domain.observability import TelemetryEventType, TelemetrySeverity, TraceContext
from agentforge.domain.tools import ToolExecutionStatus, ToolInvocation, ToolResult


class ToolExecutor(Protocol):
    """Minimal protocol implemented by safe and secure tool executors."""

    def execute(self, invocation: ToolInvocation) -> ToolResult:
        """Execute a tool invocation."""
        ...


@dataclass(slots=True)
class ObservableToolExecutor:
    """Adds telemetry around any compatible tool executor."""

    executor: ToolExecutor
    observability_service: ObservabilityService

    def execute(self, invocation: ToolInvocation) -> ToolResult:
        """Execute a tool invocation with events, metrics, and a span."""
        context = TraceContext(
            trace_id=invocation.workflow_id or invocation.invocation_id,
            workflow_id=invocation.workflow_id,
            node_id=invocation.node_id,
        )
        span = self.observability_service.start_span(
            name="tool.execute",
            context=context,
            tool_id=invocation.tool_id,
            metadata={"caller_id": invocation.caller_id},
        )
        self.observability_service.emit_event(
            name="tool.execution.started",
            event_type=TelemetryEventType.TOOL,
            message="Tool execution started.",
            context=context,
            tool_id=invocation.tool_id,
            metadata={"caller_id": invocation.caller_id},
        )
        self.observability_service.increment_counter(
            name="tool.execution.started_total",
            context=context,
            labels={"tool_id": invocation.tool_id},
        )

        result = self.executor.execute(invocation)
        severity = TelemetrySeverity.INFO
        if result.status in {ToolExecutionStatus.FAILED, ToolExecutionStatus.BLOCKED}:
            severity = TelemetrySeverity.ERROR
        elif result.status == ToolExecutionStatus.REQUIRES_APPROVAL:
            severity = TelemetrySeverity.WARNING

        self.observability_service.emit_event(
            name=f"tool.execution.{result.status.value}",
            event_type=TelemetryEventType.TOOL,
            severity=severity,
            message=result.summary,
            context=context,
            tool_id=invocation.tool_id,
            metadata={"attempts": str(result.attempts)},
        )
        self.observability_service.increment_counter(
            name="tool.execution.finished_total",
            context=context,
            labels={"tool_id": invocation.tool_id, "status": result.status.value},
        )

        if result.status == ToolExecutionStatus.SUCCESS:
            self.observability_service.complete_span(
                span,
                metadata={"status": result.status.value, "attempts": str(result.attempts)},
            )
        else:
            self.observability_service.fail_span(
                span,
                metadata={"status": result.status.value, "attempts": str(result.attempts)},
            )
        return result
