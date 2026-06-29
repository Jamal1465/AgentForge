"""Memory persistence adapters."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from agentforge.domain.memory import MemoryQuery, MemoryRecord, MemoryScope, MemorySearchResult


class MemoryStoreError(RuntimeError):
    """Raised when memory persistence operations fail."""


@dataclass(slots=True)
class InMemoryMemoryStore:
    """Deterministic in-memory memory store.

    This adapter is intentionally dependency-free and suitable for local tests.
    Later milestones may add SQLite, Postgres, or vector-store adapters behind the
    same MemoryStore port.
    """

    _records: dict[str, MemoryRecord] = field(default_factory=dict)

    def add(self, record: MemoryRecord) -> None:
        """Persist a memory record."""
        if record.record_id in self._records:
            raise MemoryStoreError(f"Memory already exists: {record.record_id}")
        self._records[record.record_id] = record

    def get(self, record_id: str) -> MemoryRecord:
        """Return a memory record by ID."""
        try:
            return self._records[record_id]
        except KeyError as exc:
            raise MemoryStoreError(f"Unknown memory record: {record_id}") from exc

    def search(self, query: MemoryQuery) -> tuple[MemorySearchResult, ...]:
        """Search records using filters and deterministic lexical scoring."""
        results: list[MemorySearchResult] = []
        for record in self._records.values():
            if not _passes_filters(record, query):
                continue
            score = _score_record(record, query)
            if score > 0 or not query.text.strip():
                results.append(MemorySearchResult(record=record, score=score))

        ranked = sorted(
            results,
            key=lambda result: (
                -result.score,
                -result.record.importance,
                result.record.kind.value,
                result.record.record_id,
            ),
        )
        return tuple(ranked[: query.limit])

    def list_by_scope(
        self,
        scope: MemoryScope,
        owner_id: str | None = None,
    ) -> tuple[MemoryRecord, ...]:
        """List memory records inside a scope boundary."""
        records = tuple(
            record
            for record in self._records.values()
            if record.matches_scope(scope=scope, owner_id=owner_id)
        )
        return tuple(sorted(records, key=lambda record: record.record_id))

    def delete(self, record_id: str) -> None:
        """Delete a memory record by ID."""
        try:
            del self._records[record_id]
        except KeyError as exc:
            raise MemoryStoreError(f"Unknown memory record: {record_id}") from exc


def _passes_filters(record: MemoryRecord, query: MemoryQuery) -> bool:
    if query.scopes and record.scope not in query.scopes:
        return False
    if query.owner_ids and record.owner_id not in query.owner_ids:
        return False
    if query.kinds and record.kind not in query.kinds:
        return False
    return not (query.tags and not set(query.tags).issubset(set(record.tags)))


def _score_record(record: MemoryRecord, query: MemoryQuery) -> float:
    query_terms = _tokenize(query.text)
    if not query_terms:
        return record.importance

    record_terms = _tokenize(" ".join((record.content, " ".join(record.tags), record.kind.value)))
    if not record_terms:
        return 0.0

    overlap = query_terms.intersection(record_terms)
    if not overlap:
        return 0.0

    lexical_score = len(overlap) / len(query_terms)
    tag_bonus = 0.1 if set(record.tags).intersection(query_terms) else 0.0
    return lexical_score + tag_bonus + record.importance


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9_+-]+", text.lower()) if token}
