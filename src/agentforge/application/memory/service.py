"""Memory application service for AgentForge.

The service centralizes how architecture, workflow, and agent components write
and retrieve context. It deliberately depends on a MemoryStore port rather than
on a database implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.application.memory.ports import MemoryStore
from agentforge.domain.memory import MemoryKind, MemoryQuery, MemoryRecord, MemoryScope


@dataclass(frozen=True, slots=True)
class MemoryContextPack:
    """Retrieved memory prepared for agent context injection."""

    query: MemoryQuery
    records: tuple[MemoryRecord, ...]
    rendered_text: str

    @property
    def is_empty(self) -> bool:
        """Return True when no memory matched the query."""
        return not self.records


@dataclass(slots=True)
class MemoryService:
    """High-level use cases for storing and retrieving project context."""

    store: MemoryStore

    def remember_project_requirement(
        self,
        project_id: str,
        content: str,
        *,
        tags: tuple[str, ...] = (),
        importance: float = 0.7,
    ) -> MemoryRecord:
        """Store a project-level requirement."""
        return self._add(
            scope=MemoryScope.PROJECT,
            kind=MemoryKind.REQUIREMENT,
            owner_id=project_id,
            content=content,
            tags=tags,
            importance=importance,
        )

    def remember_decision(
        self,
        owner_id: str,
        content: str,
        *,
        scope: MemoryScope = MemoryScope.PROJECT,
        tags: tuple[str, ...] = (),
        importance: float = 0.8,
    ) -> MemoryRecord:
        """Store a durable architecture or workflow decision."""
        return self._add(
            scope=scope,
            kind=MemoryKind.DECISION,
            owner_id=owner_id,
            content=content,
            tags=tags,
            importance=importance,
        )

    def remember_workflow_event(
        self,
        workflow_id: str,
        content: str,
        *,
        tags: tuple[str, ...] = (),
        importance: float = 0.5,
        node_id: str | None = None,
    ) -> MemoryRecord:
        """Store an auditable workflow event."""
        metadata = {"node_id": node_id} if node_id is not None else {}
        return self._add(
            scope=MemoryScope.WORKFLOW,
            kind=MemoryKind.WORKFLOW_EVENT,
            owner_id=workflow_id,
            content=content,
            tags=tags,
            importance=importance,
            metadata=metadata,
        )

    def remember_agent_note(
        self,
        agent_id: str,
        content: str,
        *,
        tags: tuple[str, ...] = (),
        importance: float = 0.5,
    ) -> MemoryRecord:
        """Store a note owned by an agent plugin."""
        return self._add(
            scope=MemoryScope.AGENT,
            kind=MemoryKind.AGENT_NOTE,
            owner_id=agent_id,
            content=content,
            tags=tags,
            importance=importance,
        )

    def retrieve_context(self, query: MemoryQuery) -> MemoryContextPack:
        """Retrieve matching memory and render it into a compact context block."""
        results = self.store.search(query)
        records = tuple(result.record for result in results)
        return MemoryContextPack(
            query=query,
            records=records,
            rendered_text=self._render(records),
        )

    def _add(
        self,
        *,
        scope: MemoryScope,
        kind: MemoryKind,
        owner_id: str,
        content: str,
        tags: tuple[str, ...],
        importance: float,
        metadata: dict[str, str] | None = None,
    ) -> MemoryRecord:
        record = MemoryRecord(
            scope=scope,
            kind=kind,
            owner_id=owner_id,
            content=content,
            tags=tags,
            importance=importance,
            metadata=metadata or {},
        )
        self.store.add(record)
        return record

    @staticmethod
    def _render(records: tuple[MemoryRecord, ...]) -> str:
        if not records:
            return "No relevant memory found."
        lines = ["# Retrieved AgentForge Memory"]
        for index, record in enumerate(records, start=1):
            tag_text = ", ".join(record.tags) if record.tags else "none"
            lines.append(
                f"{index}. [{record.scope.value}/{record.kind.value}] "
                f"owner={record.owner_id} importance={record.importance:.2f} "
                f"tags={tag_text}\n   {record.content}"
            )
        return "\n".join(lines)
