"""Local deterministic tool adapters used by tests and starter workflows."""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.domain.tools import ToolDefinition, ToolExecutionStatus, ToolInvocation, ToolResult


@dataclass(frozen=True, slots=True)
class EchoToolAdapter:
    """A dependency-free local tool that echoes one input value.

    This adapter is useful for validating the tool registry and safe execution
    path before external MCP clients are connected.
    """

    definition: ToolDefinition
    argument_name: str = "message"

    def execute(self, invocation: ToolInvocation) -> ToolResult:
        value = invocation.arguments.get(self.argument_name, "")
        return ToolResult(
            status=ToolExecutionStatus.SUCCESS,
            summary="Echo tool executed successfully.",
            output=value,
            metadata={"tool_id": self.definition.tool_id},
        )
