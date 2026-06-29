"""MCP adapter boundary for AgentForge tools.

This module deliberately does not import a concrete MCP SDK. Instead, it defines
an internal protocol and adapter shape that can be backed by ADK MCP toolsets,
stdio MCP clients, streamable HTTP clients, or test doubles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from agentforge.domain.tools import ToolDefinition, ToolExecutionStatus, ToolInvocation, ToolResult


class MCPClient(Protocol):
    """Minimal MCP client boundary required by AgentForge."""

    def call_tool(self, tool_name: str, arguments: dict[str, str]) -> dict[str, str]:
        """Call an external MCP tool and return a string-keyed response payload."""
        ...


@dataclass(frozen=True, slots=True)
class MCPToolAdapter:
    """Converts an AgentForge ToolInvocation into an MCP tool call."""

    definition: ToolDefinition
    mcp_tool_name: str
    client: MCPClient

    def execute(self, invocation: ToolInvocation) -> ToolResult:
        payload = self.client.call_tool(self.mcp_tool_name, dict(invocation.arguments))
        output = payload.get("output", "")
        summary = payload.get("summary", "MCP tool executed successfully.")
        error = payload.get("error")
        if error:
            return ToolResult(
                status=ToolExecutionStatus.FAILED,
                summary=summary,
                error=error,
                retryable=payload.get("retryable", "false").lower() == "true",
                metadata={"mcp_tool_name": self.mcp_tool_name},
            )
        return ToolResult(
            status=ToolExecutionStatus.SUCCESS,
            summary=summary,
            output=output,
            metadata={"mcp_tool_name": self.mcp_tool_name},
        )
