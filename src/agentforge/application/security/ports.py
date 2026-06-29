"""Application ports for security audit persistence."""

from __future__ import annotations

from typing import Protocol

from agentforge.domain.security import SecurityAuditEvent


class SecurityAuditStore(Protocol):
    """Persistence boundary for security audit events."""

    def record(self, event: SecurityAuditEvent) -> None:
        """Persist one security audit event."""
        ...

    def list_events(self, subject_id: str | None = None) -> tuple[SecurityAuditEvent, ...]:
        """Return security audit events, optionally filtered by subject."""
        ...
