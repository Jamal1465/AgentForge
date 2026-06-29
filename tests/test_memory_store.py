from __future__ import annotations

import pytest

from agentforge.domain.memory import MemoryKind, MemoryQuery, MemoryRecord, MemoryScope
from agentforge.infrastructure.persistence.memory_store import InMemoryMemoryStore, MemoryStoreError


def test_memory_store_adds_and_gets_record() -> None:
    store = InMemoryMemoryStore()
    record = MemoryRecord(
        scope=MemoryScope.PROJECT,
        kind=MemoryKind.REQUIREMENT,
        owner_id="project-1",
        content="Use PostgreSQL for durable persistence.",
        tags=("database",),
    )

    store.add(record)

    assert store.get(record.record_id) == record


def test_memory_store_rejects_duplicate_record_id() -> None:
    store = InMemoryMemoryStore()
    record = MemoryRecord(
        record_id="fixed",
        scope=MemoryScope.PROJECT,
        kind=MemoryKind.REQUIREMENT,
        owner_id="project-1",
        content="Use Docker.",
    )
    store.add(record)

    with pytest.raises(MemoryStoreError, match="Memory already exists"):
        store.add(record)


def test_memory_store_filters_by_scope_owner_kind_and_tags() -> None:
    store = InMemoryMemoryStore()
    matching = MemoryRecord(
        scope=MemoryScope.PROJECT,
        kind=MemoryKind.DECISION,
        owner_id="project-1",
        content="Use plugin architecture for agents.",
        tags=("architecture", "plugins"),
        importance=0.9,
    )
    other = MemoryRecord(
        scope=MemoryScope.AGENT,
        kind=MemoryKind.AGENT_NOTE,
        owner_id="agent-1",
        content="Planner prefers small tasks.",
        tags=("planning",),
    )
    store.add(matching)
    store.add(other)

    results = store.search(
        MemoryQuery(
            text="plugin architecture",
            scopes=(MemoryScope.PROJECT,),
            owner_ids=("project-1",),
            kinds=(MemoryKind.DECISION,),
            tags=("plugins",),
        )
    )

    assert len(results) == 1
    assert results[0].record == matching
    assert results[0].score > 0


def test_memory_store_lists_records_by_scope_and_owner() -> None:
    store = InMemoryMemoryStore()
    first = MemoryRecord(
        scope=MemoryScope.WORKFLOW,
        kind=MemoryKind.WORKFLOW_EVENT,
        owner_id="workflow-1",
        content="Workflow started.",
    )
    second = MemoryRecord(
        scope=MemoryScope.WORKFLOW,
        kind=MemoryKind.WORKFLOW_EVENT,
        owner_id="workflow-2",
        content="Workflow completed.",
    )
    store.add(first)
    store.add(second)

    records = store.list_by_scope(MemoryScope.WORKFLOW, owner_id="workflow-1")

    assert records == (first,)
