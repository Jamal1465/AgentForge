from __future__ import annotations

import pytest

from agentforge.domain.tools import (
    ToolDefinition,
    ToolDomainError,
    ToolExecutionPolicy,
    ToolExecutionStatus,
    ToolInvocation,
    ToolKind,
    ToolResult,
)
from agentforge.domain.value_objects import RiskLevel


def test_tool_definition_normalizes_arguments_and_tags() -> None:
    definition = ToolDefinition(
        tool_id="tool.echo",
        name="Echo",
        description="Echo a message.",
        kind=ToolKind.LOCAL,
        required_arguments=("Message", "message"),
        optional_arguments=("Format",),
        tags=("File System", "file system"),
    )

    assert definition.required_arguments == ("message",)
    assert definition.optional_arguments == ("format",)
    assert definition.tags == ("file_system",)


def test_tool_definition_rejects_argument_overlap() -> None:
    with pytest.raises(ToolDomainError, match="both required and optional"):
        ToolDefinition(
            tool_id="tool.bad",
            name="Bad",
            description="Invalid schema.",
            kind=ToolKind.LOCAL,
            required_arguments=("path",),
            optional_arguments=("path",),
        )


def test_tool_definition_validates_required_arguments() -> None:
    definition = ToolDefinition(
        tool_id="tool.write",
        name="Write",
        description="Write text.",
        kind=ToolKind.LOCAL,
        required_arguments=("path", "content"),
    )

    with pytest.raises(ToolDomainError, match="Missing required"):
        definition.validate_arguments({"path": "README.md"})


def test_tool_definition_rejects_unknown_declared_arguments() -> None:
    definition = ToolDefinition(
        tool_id="tool.echo",
        name="Echo",
        description="Echo text.",
        kind=ToolKind.LOCAL,
        required_arguments=("message",),
    )

    with pytest.raises(ToolDomainError, match="Unknown tool arguments"):
        definition.validate_arguments({"message": "hello", "extra": "no"})


def test_tool_invocation_normalizes_argument_names() -> None:
    invocation = ToolInvocation(
        tool_id="tool.echo",
        caller_id="agent.planner",
        arguments={"Message": "hello"},
    )

    assert invocation.arguments == {"message": "hello"}


def test_tool_policy_rejects_invalid_attempt_count() -> None:
    with pytest.raises(ToolDomainError, match="max_attempts"):
        ToolExecutionPolicy(max_attempts=0)


def test_tool_result_tracks_attempts() -> None:
    result = ToolResult(
        status=ToolExecutionStatus.SUCCESS,
        summary="Done.",
        output="ok",
    )

    assert result.with_attempts(3).attempts == 3


def test_high_risk_tool_definition_can_be_created() -> None:
    definition = ToolDefinition(
        tool_id="mcp.git.push",
        name="Git Push",
        description="Push source code.",
        kind=ToolKind.MCP,
        risk_level=RiskLevel.HIGH,
        is_destructive=True,
    )

    assert definition.risk_level == RiskLevel.HIGH
    assert definition.is_destructive is True
