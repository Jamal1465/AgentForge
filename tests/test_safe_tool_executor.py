from __future__ import annotations

from dataclasses import dataclass

from agentforge.domain.tools import (
    ToolDefinition,
    ToolExecutionPolicy,
    ToolExecutionStatus,
    ToolInvocation,
    ToolKind,
    ToolResult,
)
from agentforge.domain.value_objects import RiskLevel
from agentforge.infrastructure.tools.local import EchoToolAdapter
from agentforge.runtime.tools.executor import SafeToolExecutor
from agentforge.runtime.tools.registry import ToolRegistry


def make_definition(
    *,
    tool_id: str = "tool.echo",
    risk_level: RiskLevel = RiskLevel.LOW,
    is_destructive: bool = False,
) -> ToolDefinition:
    return ToolDefinition(
        tool_id=tool_id,
        name="Echo",
        description="Echo a message.",
        kind=ToolKind.LOCAL,
        risk_level=risk_level,
        required_arguments=("message",),
        is_destructive=is_destructive,
    )


def make_executor(adapter: object) -> SafeToolExecutor:
    registry = ToolRegistry()
    registry.register(adapter)  # type: ignore[arg-type]
    return SafeToolExecutor(registry=registry)


def test_safe_tool_executor_executes_valid_tool() -> None:
    executor = make_executor(EchoToolAdapter(definition=make_definition()))

    result = executor.execute(
        ToolInvocation(
            tool_id="tool.echo",
            caller_id="agent.planner",
            arguments={"message": "hello"},
        )
    )

    assert result.status == ToolExecutionStatus.SUCCESS
    assert result.output == "hello"
    assert result.attempts == 1


def test_safe_tool_executor_returns_failed_result_for_unknown_tool() -> None:
    executor = SafeToolExecutor(registry=ToolRegistry())

    result = executor.execute(
        ToolInvocation(tool_id="missing", caller_id="agent.planner", arguments={})
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert "Unknown tool" in (result.error or "")


def test_safe_tool_executor_validates_arguments_before_execution() -> None:
    executor = make_executor(EchoToolAdapter(definition=make_definition()))

    result = executor.execute(
        ToolInvocation(tool_id="tool.echo", caller_id="agent.planner", arguments={})
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert "Missing required" in (result.error or "")


def test_safe_tool_executor_requires_approval_for_high_risk_tool() -> None:
    executor = make_executor(EchoToolAdapter(definition=make_definition(risk_level=RiskLevel.HIGH)))

    result = executor.execute(
        ToolInvocation(
            tool_id="tool.echo",
            caller_id="agent.planner",
            arguments={"message": "hello"},
        )
    )

    assert result.status == ToolExecutionStatus.REQUIRES_APPROVAL
    assert "high" in (result.error or "")


def test_safe_tool_executor_runs_high_risk_tool_after_approval() -> None:
    executor = make_executor(EchoToolAdapter(definition=make_definition(risk_level=RiskLevel.HIGH)))

    result = executor.execute(
        ToolInvocation(
            tool_id="tool.echo",
            caller_id="agent.planner",
            arguments={"message": "approved"},
            approval_granted=True,
        )
    )

    assert result.status == ToolExecutionStatus.SUCCESS
    assert result.output == "approved"


def test_safe_tool_executor_blocks_destructive_tool_by_default() -> None:
    executor = make_executor(EchoToolAdapter(definition=make_definition(is_destructive=True)))

    result = executor.execute(
        ToolInvocation(
            tool_id="tool.echo",
            caller_id="agent.planner",
            arguments={"message": "delete"},
        )
    )

    assert result.status == ToolExecutionStatus.BLOCKED
    assert "Destructive" in (result.error or "")


@dataclass(slots=True)
class FlakyToolAdapter:
    definition: ToolDefinition
    calls: int = 0

    def execute(self, invocation: ToolInvocation) -> ToolResult:
        self.calls += 1
        if self.calls == 1:
            return ToolResult(
                status=ToolExecutionStatus.FAILED,
                summary="Temporary tool failure.",
                error="temporary",
                retryable=True,
            )
        return ToolResult(
            status=ToolExecutionStatus.SUCCESS,
            summary="Recovered.",
            output=invocation.arguments["message"],
        )


def test_safe_tool_executor_retries_retryable_failures() -> None:
    adapter = FlakyToolAdapter(definition=make_definition())
    registry = ToolRegistry()
    registry.register(adapter)
    executor = SafeToolExecutor(
        registry=registry,
        policy=ToolExecutionPolicy(max_attempts=2),
    )

    result = executor.execute(
        ToolInvocation(
            tool_id="tool.echo",
            caller_id="agent.planner",
            arguments={"message": "ok"},
        )
    )

    assert result.status == ToolExecutionStatus.SUCCESS
    assert result.output == "ok"
    assert result.attempts == 2
    assert adapter.calls == 2


@dataclass(slots=True)
class ExplodingToolAdapter:
    definition: ToolDefinition

    def execute(self, invocation: ToolInvocation) -> ToolResult:
        raise RuntimeError("network down")


def test_safe_tool_executor_catches_adapter_exceptions() -> None:
    registry = ToolRegistry()
    registry.register(ExplodingToolAdapter(definition=make_definition()))
    executor = SafeToolExecutor(
        registry=registry,
        policy=ToolExecutionPolicy(max_attempts=2),
    )

    result = executor.execute(
        ToolInvocation(
            tool_id="tool.echo",
            caller_id="agent.planner",
            arguments={"message": "hello"},
        )
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert result.attempts == 2
    assert "network down" in (result.error or "")
