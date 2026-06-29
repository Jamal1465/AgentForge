from __future__ import annotations

import pytest

from agentforge.domain.memory import (
    MemoryDomainError,
    MemoryKind,
    MemoryQuery,
    MemoryRecord,
    MemoryScope,
)


def test_memory_record_normalizes_tags_and_preserves_order() -> None:
    record = MemoryRecord(
        scope=MemoryScope.PROJECT,
        kind=MemoryKind.REQUIREMENT,
        owner_id="project-1",
        content="Use FastAPI and React.",
        tags=(" Backend ", "backend", "React App"),
    )

    assert record.tags == ("backend", "react-app")


def test_memory_record_rejects_empty_content() -> None:
    with pytest.raises(MemoryDomainError, match="Memory content cannot be empty"):
        MemoryRecord(
            scope=MemoryScope.PROJECT,
            kind=MemoryKind.REQUIREMENT,
            owner_id="project-1",
            content="   ",
        )


def test_memory_record_rejects_invalid_importance() -> None:
    with pytest.raises(MemoryDomainError, match="importance"):
        MemoryRecord(
            scope=MemoryScope.PROJECT,
            kind=MemoryKind.REQUIREMENT,
            owner_id="project-1",
            content="Valid content",
            importance=2.0,
        )


def test_memory_query_requires_positive_limit() -> None:
    with pytest.raises(MemoryDomainError, match="limit"):
        MemoryQuery(limit=0)
