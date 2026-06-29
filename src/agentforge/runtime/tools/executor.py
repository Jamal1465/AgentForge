"""Safe tool execution wrapper for AgentForge.

The executor is the only application-facing component that should call concrete
ToolAdapter implementations. It validates the tool definition, enforces approval
policy, blocks destructive actions by default, catches adapter errors, and
retries explicitly retryable failures.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.domain.tools import (
    ToolDomainError,
    ToolExecutionPolicy,
    ToolExecutionStatus,
    ToolInvocation,
    ToolResult,
)
from agentforge.runtime.tools.registry import ToolRegistry, ToolRegistryError


@dataclass(slots=True)
class SafeToolExecutor:
    """Executes tools through a deterministic safety and retry policy."""

    registry: ToolRegistry
    policy: ToolExecutionPolicy = ToolExecutionPolicy()

    def execute(self, invocation: ToolInvocation) -> ToolResult:
        """Validate and execute a tool invocation."""
        try:
            adapter = self.registry.get(invocation.tool_id)
        except ToolRegistryError as exc:
            return ToolResult(
                status=ToolExecutionStatus.FAILED,
                summary="Tool lookup failed.",
                error=str(exc),
                retryable=False,
            )

        definition = adapter.definition
        try:
            definition.validate_arguments(invocation.arguments)
        except ToolDomainError as exc:
            return ToolResult(
                status=ToolExecutionStatus.FAILED,
                summary="Tool argument validation failed.",
                error=str(exc),
                retryable=False,
            )

        if definition.is_destructive and not self.policy.allow_destructive_tools:
            return ToolResult(
                status=ToolExecutionStatus.BLOCKED,
                summary="Tool execution blocked by policy.",
                error="Destructive tools are disabled by the current execution policy.",
                retryable=False,
            )

        if (
            definition.risk_level in self.policy.approval_required_for
            and not invocation.approval_granted
        ):
            return ToolResult(
                status=ToolExecutionStatus.REQUIRES_APPROVAL,
                summary="Tool execution requires human approval.",
                error=f"Tool risk level is {definition.risk_level.value}.",
                retryable=False,
            )

        last_result: ToolResult | None = None
        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                result = adapter.execute(invocation).with_attempts(attempt)
            except Exception as exc:  # noqa: BLE001 - adapter boundary must not leak failures.
                result = ToolResult(
                    status=ToolExecutionStatus.FAILED,
                    summary="Tool adapter raised an exception.",
                    error=str(exc),
                    retryable=True,
                    attempts=attempt,
                )

            last_result = result
            if result.status == ToolExecutionStatus.SUCCESS:
                return result
            if not result.retryable:
                return result

        if last_result is None:
            return ToolResult(
                status=ToolExecutionStatus.FAILED,
                summary="Tool execution did not run.",
                error="No execution attempts were made.",
                retryable=False,
            )
        return last_result.with_attempts(self.policy.max_attempts)
