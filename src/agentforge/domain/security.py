"""Domain model for AgentForge security decisions.

The security domain is capability-first. It protects tasks, plugins, tools, and
text artifacts without depending on specific agent class names such as backend,
frontend, or database agents. Policy is expressed in terms of capabilities,
risk levels, tool metadata, and content findings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4

from agentforge.domain.value_objects import Capability, RiskLevel


class SecurityDomainError(ValueError):
    """Raised when a security domain object violates invariants."""


class SecurityFindingType(StrEnum):
    """Categories of security findings emitted by guardrails."""

    PROMPT_INJECTION = "prompt_injection"
    SECRET_EXPOSURE = "secret_exposure"
    PII_EXPOSURE = "pii_exposure"
    DESTRUCTIVE_OPERATION = "destructive_operation"
    HIGH_RISK_CAPABILITY = "high_risk_capability"
    BLOCKED_CAPABILITY = "blocked_capability"
    UNTRUSTED_PLUGIN = "untrusted_plugin"
    TOOL_POLICY_VIOLATION = "tool_policy_violation"


class SecurityDecisionStatus(StrEnum):
    """Final outcome of a security assessment."""

    ALLOW = "allow"
    REQUIRES_APPROVAL = "requires_approval"
    BLOCK = "block"


@dataclass(frozen=True, slots=True)
class SecurityFinding:
    """One normalized security finding produced by a scanner or policy check."""

    finding_type: SecurityFindingType
    severity: RiskLevel
    message: str
    subject_id: str
    evidence: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    finding_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.message.strip():
            raise SecurityDomainError("Security finding message cannot be empty.")
        if not self.subject_id.strip():
            raise SecurityDomainError("Security finding subject_id cannot be empty.")
        if not self.finding_id.strip():
            raise SecurityDomainError("Security finding ID cannot be empty.")


@dataclass(frozen=True, slots=True)
class SecurityDecision:
    """Immutable decision returned by the security layer."""

    status: SecurityDecisionStatus
    subject_id: str
    reason: str
    findings: tuple[SecurityFinding, ...] = ()
    decision_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.subject_id.strip():
            raise SecurityDomainError("Security decision subject_id cannot be empty.")
        if not self.reason.strip():
            raise SecurityDomainError("Security decision reason cannot be empty.")
        if not self.decision_id.strip():
            raise SecurityDomainError("Security decision ID cannot be empty.")

    @property
    def is_allowed(self) -> bool:
        """Return True only when execution may continue immediately."""
        return self.status == SecurityDecisionStatus.ALLOW


@dataclass(frozen=True, slots=True)
class SecurityAuditEvent:
    """Audit record for security decisions and scanner findings."""

    event_type: str
    subject_id: str
    decision_status: SecurityDecisionStatus
    message: str
    actor_id: str | None = None
    finding_ids: tuple[str, ...] = ()
    event_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.event_type.strip():
            raise SecurityDomainError("Security audit event type cannot be empty.")
        if not self.subject_id.strip():
            raise SecurityDomainError("Security audit subject_id cannot be empty.")
        if not self.message.strip():
            raise SecurityDomainError("Security audit message cannot be empty.")
        if not self.event_id.strip():
            raise SecurityDomainError("Security audit event ID cannot be empty.")


@dataclass(frozen=True, slots=True)
class SecurityPolicy:
    """Capability-first security policy for AgentForge.

    The policy deliberately references capabilities, risk levels, and tool flags
    instead of concrete agent class names. This keeps AgentForge extensible when
    new plugins are installed.
    """

    blocked_capabilities: tuple[Capability, ...] = ()
    approval_required_capabilities: tuple[Capability, ...] = ()
    approval_required_risk_levels: tuple[RiskLevel, ...] = (RiskLevel.HIGH, RiskLevel.CRITICAL)
    trusted_plugin_ids: tuple[str, ...] = ()
    require_trusted_plugins: bool = False
    allow_destructive_tools: bool = False
    block_prompt_injection: bool = True
    block_secret_exposure: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "blocked_capabilities",
            _dedupe_capabilities(self.blocked_capabilities),
        )
        object.__setattr__(
            self,
            "approval_required_capabilities",
            _dedupe_capabilities(self.approval_required_capabilities),
        )
        trusted = tuple(
            dict.fromkeys(
                plugin_id.strip() for plugin_id in self.trusted_plugin_ids if plugin_id.strip()
            )
        )
        object.__setattr__(self, "trusted_plugin_ids", trusted)

    def is_capability_blocked(self, capability: Capability) -> bool:
        """Return True when a capability is completely disabled."""
        return capability in self.blocked_capabilities

    def does_capability_require_approval(self, capability: Capability) -> bool:
        """Return True when a capability needs human approval before execution."""
        return capability in self.approval_required_capabilities


def _dedupe_capabilities(capabilities: tuple[Capability, ...]) -> tuple[Capability, ...]:
    return tuple(dict.fromkeys(capabilities))
