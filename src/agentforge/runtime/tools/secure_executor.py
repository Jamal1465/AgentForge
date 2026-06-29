"""Security-aware tool executor for AgentForge."""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.application.security.service import SecurityService
from agentforge.domain.security import SecurityDecisionStatus
from agentforge.domain.tools import ToolExecutionStatus, ToolInvocation, ToolResult
from agentforge.runtime.tools.executor import SafeToolExecutor
from agentforge.runtime.tools.registry import ToolRegistryError


@dataclass(slots=True)
class SecureToolExecutor:
    """Executes tools only after security assessment passes.

    This wrapper composes the existing SafeToolExecutor instead of replacing it.
    The security service handles content, policy, and approval checks; the safe
    executor still owns argument validation, retry handling, and adapter isolation.
    """

    executor: SafeToolExecutor
    security_service: SecurityService

    def execute(self, invocation: ToolInvocation) -> ToolResult:
        """Assess and execute one tool invocation."""
        try:
            adapter = self.executor.registry.get(invocation.tool_id)
        except ToolRegistryError as exc:
            return ToolResult(
                status=ToolExecutionStatus.FAILED,
                summary="Tool lookup failed before security assessment.",
                error=str(exc),
            )

        decision = self.security_service.assess_tool_invocation(adapter.definition, invocation)
        if decision.status == SecurityDecisionStatus.BLOCK:
            return ToolResult(
                status=ToolExecutionStatus.BLOCKED,
                summary="Tool execution blocked by security policy.",
                error=decision.reason,
                metadata={"security_decision_id": decision.decision_id},
            )
        if decision.status == SecurityDecisionStatus.REQUIRES_APPROVAL:
            return ToolResult(
                status=ToolExecutionStatus.REQUIRES_APPROVAL,
                summary="Tool execution requires human approval by security policy.",
                error=decision.reason,
                metadata={"security_decision_id": decision.decision_id},
            )

        result = self.executor.execute(invocation)
        redacted_output = self.security_service.redact_secrets(result.output)
        redacted_error = (
            self.security_service.redact_secrets(result.error) if result.error else None
        )
        if redacted_output == result.output and redacted_error == result.error:
            return result
        return ToolResult(
            status=result.status,
            summary=result.summary,
            output=redacted_output,
            error=redacted_error,
            retryable=result.retryable,
            attempts=result.attempts,
            metadata=dict(result.metadata),
        )
