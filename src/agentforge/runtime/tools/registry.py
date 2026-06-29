"""Tool registry implementation."""

from __future__ import annotations

from dataclasses import dataclass, field

from agentforge.application.tools.ports import ToolAdapter
from agentforge.domain.tools import ToolKind


class ToolRegistryError(RuntimeError):
    """Raised when tool registry operations are invalid."""


@dataclass(slots=True)
class ToolRegistry:
    """Stores concrete tool adapters behind their public tool definitions."""

    _tools: dict[str, ToolAdapter] = field(default_factory=dict)

    def register(self, adapter: ToolAdapter) -> None:
        """Register a tool adapter by its tool ID."""
        tool_id = adapter.definition.tool_id
        if tool_id in self._tools:
            raise ToolRegistryError(f"Tool already registered: {tool_id}")
        self._tools[tool_id] = adapter

    def get(self, tool_id: str) -> ToolAdapter:
        """Return a registered tool adapter by ID."""
        try:
            return self._tools[tool_id]
        except KeyError as exc:
            raise ToolRegistryError(f"Unknown tool: {tool_id}") from exc

    def list_tools(self) -> tuple[ToolAdapter, ...]:
        """Return all registered tool adapters."""
        return tuple(self._tools.values())

    def find_by_kind(self, kind: ToolKind) -> tuple[ToolAdapter, ...]:
        """Return tools implemented by a specific adapter kind."""
        return tuple(tool for tool in self._tools.values() if tool.definition.kind == kind)
