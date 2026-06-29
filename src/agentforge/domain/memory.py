"""Domain model for AgentForge memory.

The memory domain is framework-free. It models durable knowledge that can be
attached to a project, workflow, agent, or user session and later retrieved as
structured context for agent execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4


class MemoryDomainError(ValueError):
    """Raised when a memory object violates a domain invariant."""


class MemoryScope(StrEnum):
    """Logical ownership boundary for a memory record."""

    PROJECT = "project"
    WORKFLOW = "workflow"
    AGENT = "agent"
    SESSION = "session"


class MemoryKind(StrEnum):
    """Semantic classification for stored memory."""

    REQUIREMENT = "requirement"
    DECISION = "decision"
    CONSTRAINT = "constraint"
    ARTIFACT_SUMMARY = "artifact_summary"
    WORKFLOW_EVENT = "workflow_event"
    AGENT_NOTE = "agent_note"
    SECURITY_NOTE = "security_note"
    EVALUATION_NOTE = "evaluation_note"


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    """One durable unit of AgentForge memory.

    A record is intentionally small and immutable. Updating memory should create
    a new record rather than mutating historical context. This keeps execution
    auditable and makes later evaluation easier.
    """

    scope: MemoryScope
    kind: MemoryKind
    content: str
    owner_id: str
    record_id: str = field(default_factory=lambda: str(uuid4()))
    tags: tuple[str, ...] = ()
    importance: float = 0.5
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise MemoryDomainError("Memory content cannot be empty.")
        if not self.owner_id.strip():
            raise MemoryDomainError("Memory owner_id cannot be empty.")
        if not self.record_id.strip():
            raise MemoryDomainError("Memory record_id cannot be empty.")
        if not 0.0 <= self.importance <= 1.0:
            raise MemoryDomainError("Memory importance must be between 0.0 and 1.0.")
        normalized_tags = tuple(_normalize_tag(tag) for tag in self.tags if tag.strip())
        object.__setattr__(self, "tags", tuple(dict.fromkeys(normalized_tags)))

    def matches_scope(self, scope: MemoryScope, owner_id: str | None = None) -> bool:
        """Return True when this record belongs to the requested scope boundary."""
        if self.scope != scope:
            return False
        if owner_id is None:
            return True
        return self.owner_id == owner_id


@dataclass(frozen=True, slots=True)
class MemoryQuery:
    """Search request used by memory stores and context assemblers."""

    text: str = ""
    scopes: tuple[MemoryScope, ...] = ()
    owner_ids: tuple[str, ...] = ()
    kinds: tuple[MemoryKind, ...] = ()
    tags: tuple[str, ...] = ()
    limit: int = 10

    def __post_init__(self) -> None:
        if self.limit < 1:
            raise MemoryDomainError("Memory query limit must be at least 1.")
        normalized_tags = tuple(_normalize_tag(tag) for tag in self.tags if tag.strip())
        object.__setattr__(self, "tags", tuple(dict.fromkeys(normalized_tags)))


@dataclass(frozen=True, slots=True)
class MemorySearchResult:
    """A memory record with a deterministic relevance score."""

    record: MemoryRecord
    score: float

    def __post_init__(self) -> None:
        if self.score < 0:
            raise MemoryDomainError("Memory search score cannot be negative.")


def _normalize_tag(tag: str) -> str:
    normalized = tag.strip().lower().replace(" ", "-")
    if not normalized:
        raise MemoryDomainError("Memory tag cannot be empty.")
    return normalized
