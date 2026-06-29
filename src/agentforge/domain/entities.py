"""Core domain entities for AgentForge."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4

from agentforge.domain.value_objects import Capability, RiskLevel


class TaskStatus(StrEnum):
    """Lifecycle state for a project task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_APPROVAL = "requires_approval"


@dataclass(frozen=True, slots=True)
class ProjectRequest:
    """Natural-language request submitted by a user."""

    description: str

    def __post_init__(self) -> None:
        if not self.description.strip():
            raise ValueError("Project description cannot be empty.")


@dataclass(slots=True)
class ProjectTask:
    """Atomic task that can be routed to an agent plugin."""

    title: str
    required_capabilities: tuple[Capability, ...]
    description: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    task_id: str = field(default_factory=lambda: str(uuid4()))
    status: TaskStatus = TaskStatus.PENDING

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Task title cannot be empty.")
        if not self.required_capabilities:
            raise ValueError("Task must require at least one capability.")


@dataclass(frozen=True, slots=True)
class Artifact:
    """Reference to generated output from an agent or workflow."""

    name: str
    content: str
    artifact_type: str = "markdown"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Artifact name cannot be empty.")
