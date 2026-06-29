"""Application ports for AgentForge memory persistence."""

from __future__ import annotations

from typing import Protocol

from agentforge.domain.memory import MemoryQuery, MemoryRecord, MemoryScope, MemorySearchResult


class MemoryStore(Protocol):
    """Persistence boundary used by the memory application service."""

    def add(self, record: MemoryRecord) -> None:
        """Persist a memory record."""
        ...

    def get(self, record_id: str) -> MemoryRecord:
        """Load a memory record by ID."""
        ...

    def search(self, query: MemoryQuery) -> tuple[MemorySearchResult, ...]:
        """Search memory records using structured filters and lexical relevance."""
        ...

    def list_by_scope(
        self,
        scope: MemoryScope,
        owner_id: str | None = None,
    ) -> tuple[MemoryRecord, ...]:
        """List memory records inside a scope boundary."""
        ...

    def delete(self, record_id: str) -> None:
        """Delete a memory record by ID."""
        ...
