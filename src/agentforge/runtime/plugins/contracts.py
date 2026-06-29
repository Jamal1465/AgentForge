"""Agent plugin contracts.

Concrete agents implement this protocol so the orchestrator can discover and route
work by capability instead of hardcoded class names.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from agentforge.domain.entities import Artifact, ProjectTask
from agentforge.domain.value_objects import Capability, RiskLevel


class AgentExecutionStatus(StrEnum):
    """Standard execution statuses returned by agent plugins."""

    SUCCESS = "success"
    FAILED = "failed"
    NEEDS_APPROVAL = "needs_approval"


@dataclass(frozen=True, slots=True)
class AgentMetadata:
    """Public metadata used by the registry and router."""

    agent_id: str
    name: str
    version: str
    capabilities: tuple[Capability, ...]
    required_tools: tuple[str, ...] = ()
    risk_level: RiskLevel = RiskLevel.LOW

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise ValueError("Agent ID cannot be empty.")
        if not self.name.strip():
            raise ValueError("Agent name cannot be empty.")
        if not self.version.strip():
            raise ValueError("Agent version cannot be empty.")
        if not self.capabilities:
            raise ValueError("Agent must declare at least one capability.")


@dataclass(frozen=True, slots=True)
class AgentResult:
    """Structured result returned by every agent plugin."""

    status: AgentExecutionStatus
    summary: str
    artifacts: tuple[Artifact, ...] = ()
    decisions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    confidence: float = 1.0
    next_actions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0.")


class AgentPlugin(Protocol):
    """Protocol implemented by all AgentForge agents."""

    @property
    def metadata(self) -> AgentMetadata:
        """Return plugin metadata."""
        ...

    def execute(self, task: ProjectTask) -> AgentResult:
        """Execute a routed task and return a structured result."""
        ...
