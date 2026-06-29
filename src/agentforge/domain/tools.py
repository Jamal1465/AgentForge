"""Pure domain model for AgentForge tool execution.

Tools are external capabilities that agents can request through a controlled
runtime boundary. The domain model intentionally avoids importing MCP SDKs,
network clients, subprocess APIs, or framework-specific classes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4

from agentforge.domain.value_objects import RiskLevel


class ToolDomainError(ValueError):
    """Raised when a tool domain object violates invariants."""


class ToolKind(StrEnum):
    """Classifies how a tool is implemented behind the port."""

    LOCAL = "local"
    MCP = "mcp"
    REMOTE_API = "remote_api"


class ToolExecutionStatus(StrEnum):
    """Standard result statuses for tool execution."""

    SUCCESS = "success"
    FAILED = "failed"
    REQUIRES_APPROVAL = "requires_approval"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    """Public metadata for a callable tool.

    The registry and safety wrapper use this definition to decide whether a tool
    exists, what arguments it requires, and whether human approval is required
    before execution.
    """

    tool_id: str
    name: str
    description: str
    kind: ToolKind
    risk_level: RiskLevel = RiskLevel.LOW
    required_arguments: tuple[str, ...] = ()
    optional_arguments: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    is_destructive: bool = False

    def __post_init__(self) -> None:
        if not self.tool_id.strip():
            raise ToolDomainError("Tool ID cannot be empty.")
        if not self.name.strip():
            raise ToolDomainError("Tool name cannot be empty.")
        if not self.description.strip():
            raise ToolDomainError("Tool description cannot be empty.")
        normalized_required = _normalize_names(self.required_arguments, "required argument")
        normalized_optional = _normalize_names(self.optional_arguments, "optional argument")
        overlap = set(normalized_required).intersection(normalized_optional)
        if overlap:
            duplicate = ", ".join(sorted(overlap))
            raise ToolDomainError(
                f"Tool arguments cannot be both required and optional: {duplicate}"
            )
        normalized_tags = _normalize_names(self.tags, "tag")
        object.__setattr__(self, "required_arguments", normalized_required)
        object.__setattr__(self, "optional_arguments", normalized_optional)
        object.__setattr__(self, "tags", normalized_tags)

    def validate_arguments(self, arguments: dict[str, str]) -> None:
        """Validate required and declared arguments for this tool."""
        normalized_arguments = {_normalize_name(name, "argument") for name in arguments}
        missing = set(self.required_arguments) - normalized_arguments
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise ToolDomainError(f"Missing required tool arguments: {missing_text}")

        declared = set(self.required_arguments).union(self.optional_arguments)
        if declared:
            unknown = normalized_arguments - declared
            if unknown:
                unknown_text = ", ".join(sorted(unknown))
                raise ToolDomainError(f"Unknown tool arguments: {unknown_text}")


@dataclass(frozen=True, slots=True)
class ToolInvocation:
    """A request to execute one tool through the controlled runtime."""

    tool_id: str
    arguments: dict[str, str]
    caller_id: str
    workflow_id: str | None = None
    node_id: str | None = None
    approval_granted: bool = False
    invocation_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.tool_id.strip():
            raise ToolDomainError("Tool invocation tool_id cannot be empty.")
        if not self.caller_id.strip():
            raise ToolDomainError("Tool invocation caller_id cannot be empty.")
        if not self.invocation_id.strip():
            raise ToolDomainError("Tool invocation ID cannot be empty.")
        normalized_arguments: dict[str, str] = {}
        for key, value in self.arguments.items():
            normalized_arguments[_normalize_name(key, "argument")] = str(value)
        object.__setattr__(self, "arguments", normalized_arguments)


@dataclass(frozen=True, slots=True)
class ToolResult:
    """Structured result returned by every tool adapter."""

    status: ToolExecutionStatus
    summary: str
    output: str = ""
    error: str | None = None
    retryable: bool = False
    attempts: int = 1
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ToolDomainError("Tool result summary cannot be empty.")
        if self.attempts < 1:
            raise ToolDomainError("Tool result attempts must be at least 1.")
        if (
            self.status in {ToolExecutionStatus.FAILED, ToolExecutionStatus.BLOCKED}
            and self.error is not None
            and not self.error.strip()
        ):
            raise ToolDomainError("Tool result error cannot be blank when provided.")

    def with_attempts(self, attempts: int) -> ToolResult:
        """Return a copy of the result with the final attempt count attached."""
        return ToolResult(
            status=self.status,
            summary=self.summary,
            output=self.output,
            error=self.error,
            retryable=self.retryable,
            attempts=attempts,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True, slots=True)
class ToolExecutionPolicy:
    """Safety and retry policy applied before a tool adapter is called."""

    max_attempts: int = 2
    approval_required_for: tuple[RiskLevel, ...] = (RiskLevel.HIGH, RiskLevel.CRITICAL)
    allow_destructive_tools: bool = False

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ToolDomainError("Tool policy max_attempts must be at least 1.")


def _normalize_names(values: tuple[str, ...], label: str) -> tuple[str, ...]:
    normalized = tuple(_normalize_name(value, label) for value in values if value.strip())
    return tuple(dict.fromkeys(normalized))


def _normalize_name(value: str, label: str) -> str:
    normalized = value.strip().lower().replace(" ", "_")
    if not normalized:
        raise ToolDomainError(f"Tool {label} cannot be empty.")
    return normalized
