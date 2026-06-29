"""Application ports for AgentForge tool execution."""

from __future__ import annotations

from typing import Protocol

from agentforge.domain.tools import ToolDefinition, ToolInvocation, ToolResult


class ToolAdapter(Protocol):
    """Boundary implemented by concrete local, MCP, or remote tool adapters."""

    @property
    def definition(self) -> ToolDefinition:
        """Return public tool metadata."""
        ...

    def execute(self, invocation: ToolInvocation) -> ToolResult:
        """Execute the tool and return a structured result."""
        ...
