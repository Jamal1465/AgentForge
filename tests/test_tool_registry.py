from __future__ import annotations

import pytest

from agentforge.domain.tools import ToolDefinition, ToolKind
from agentforge.infrastructure.tools.local import EchoToolAdapter
from agentforge.runtime.tools.registry import ToolRegistry, ToolRegistryError


def make_echo_tool(tool_id: str = "tool.echo") -> EchoToolAdapter:
    return EchoToolAdapter(
        definition=ToolDefinition(
            tool_id=tool_id,
            name="Echo",
            description="Echo a message.",
            kind=ToolKind.LOCAL,
            required_arguments=("message",),
        )
    )


def test_tool_registry_registers_and_gets_tool() -> None:
    registry = ToolRegistry()
    tool = make_echo_tool()

    registry.register(tool)

    assert registry.get("tool.echo") is tool
    assert registry.list_tools() == (tool,)


def test_tool_registry_rejects_duplicate_tool_id() -> None:
    registry = ToolRegistry()
    registry.register(make_echo_tool())

    with pytest.raises(ToolRegistryError, match="already registered"):
        registry.register(make_echo_tool())


def test_tool_registry_filters_by_kind() -> None:
    registry = ToolRegistry()
    tool = make_echo_tool()
    registry.register(tool)

    assert registry.find_by_kind(ToolKind.LOCAL) == (tool,)
    assert registry.find_by_kind(ToolKind.MCP) == ()


def test_tool_registry_raises_for_unknown_tool() -> None:
    registry = ToolRegistry()

    with pytest.raises(ToolRegistryError, match="Unknown tool"):
        registry.get("missing")
