from __future__ import annotations

from agentforge.application.observability.service import ObservabilityService
from agentforge.domain.tools import ToolDefinition, ToolExecutionStatus, ToolInvocation, ToolKind
from agentforge.infrastructure.persistence.observability_store import InMemoryObservabilityStore
from agentforge.infrastructure.tools.local import EchoToolAdapter
from agentforge.runtime.tools.executor import SafeToolExecutor
from agentforge.runtime.tools.observable_executor import ObservableToolExecutor
from agentforge.runtime.tools.registry import ToolRegistry


def test_observable_tool_executor_records_successful_tool_execution() -> None:
    definition = ToolDefinition(
        tool_id="tool.echo",
        name="Echo",
        description="Echo a message.",
        kind=ToolKind.LOCAL,
        required_arguments=("message",),
    )
    registry = ToolRegistry()
    registry.register(EchoToolAdapter(definition=definition))
    store = InMemoryObservabilityStore()
    executor = ObservableToolExecutor(
        executor=SafeToolExecutor(registry=registry),
        observability_service=ObservabilityService(store=store),
    )

    result = executor.execute(
        ToolInvocation(
            tool_id="tool.echo",
            caller_id="plugin.planner",
            arguments={"message": "hello"},
            workflow_id="workflow-1",
            node_id="node-1",
        )
    )

    assert result.status == ToolExecutionStatus.SUCCESS
    event_names = [event.name for event in store.list_events(trace_id="workflow-1")]
    assert "tool.execution.started" in event_names
    assert "tool.execution.success" in event_names
    assert store.list_metrics(name="tool.execution.finished_total")
    assert store.list_spans(trace_id="workflow-1")
