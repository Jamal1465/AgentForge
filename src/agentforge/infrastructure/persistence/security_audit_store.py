"""Security audit persistence adapters."""

from __future__ import annotations

from dataclasses import dataclass, field

from agentforge.domain.security import SecurityAuditEvent


@dataclass(slots=True)
class InMemorySecurityAuditStore:
    """In-memory audit store for tests and local development."""

    _events: list[SecurityAuditEvent] = field(default_factory=list)

    def record(self, event: SecurityAuditEvent) -> None:
        """Persist one audit event."""
        self._events.append(event)

    def list_events(self, subject_id: str | None = None) -> tuple[SecurityAuditEvent, ...]:
        """Return all audit events or events for one subject."""
        if subject_id is None:
            return tuple(self._events)
        return tuple(event for event in self._events if event.subject_id == subject_id)
