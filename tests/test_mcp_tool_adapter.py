from __future__ import annotations

from dataclasses import dataclass, field

from agentforge.domain.tools import ToolDefinition, ToolExecutionStatus, ToolInvocation, ToolKind
from agentforge.infrastructure.tools.mcp import MCPToolAdapter


@dataclass(slots=True)
class FakeMCPClient:
    response: dict[str, str]
    calls: list[tuple[str, dict[str, str]]] = field(default_factory=list)

    def call_tool(self, tool_name: str, arguments: dict[str, str]) -> dict[str, str]:
        self.calls.append((tool_name, arguments))
        return dict(self.response)


def make_definition() -> ToolDefinition:
    return ToolDefinition(
        tool_id="mcp.docs.search",
        name="Developer Docs Search",
        description="Search developer documentation through an MCP server.",
        kind=ToolKind.MCP,
        required_arguments=("query",),
    )


def test_mcp_tool_adapter_converts_successful_response() -> None:
    client = FakeMCPClient(response={"summary": "Found docs.", "output": "ADK tools docs"})
    adapter = MCPToolAdapter(
        definition=make_definition(),
        mcp_tool_name="google_docs_search",
        client=client,
    )

    result = adapter.execute(
        ToolInvocation(
            tool_id="mcp.docs.search",
            caller_id="agent.research",
            arguments={"query": "ADK MCP tools"},
        )
    )

    assert result.status == ToolExecutionStatus.SUCCESS
    assert result.output == "ADK tools docs"
    assert result.metadata["mcp_tool_name"] == "google_docs_search"
    assert client.calls == [("google_docs_search", {"query": "ADK MCP tools"})]


def test_mcp_tool_adapter_converts_error_response() -> None:
    client = FakeMCPClient(
        response={
            "summary": "MCP request failed.",
            "error": "server unavailable",
            "retryable": "true",
        }
    )
    adapter = MCPToolAdapter(
        definition=make_definition(),
        mcp_tool_name="google_docs_search",
        client=client,
    )

    result = adapter.execute(
        ToolInvocation(
            tool_id="mcp.docs.search",
            caller_id="agent.research",
            arguments={"query": "ADK MCP tools"},
        )
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert result.retryable is True
    assert result.error == "server unavailable"
