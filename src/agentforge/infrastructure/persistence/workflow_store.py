"""Workflow persistence adapters."""

from __future__ import annotations

from dataclasses import dataclass, field

from agentforge.domain.workflow import WorkflowGraph


class WorkflowStoreError(RuntimeError):
    """Raised when workflow persistence operations fail."""


@dataclass(slots=True)
class InMemoryWorkflowStore:
    """In-memory workflow store used for tests and local development.

    This adapter satisfies the application WorkflowStore port without introducing
    database dependencies. Later milestones can add SQLite, Postgres, or document
    store adapters behind the same port.
    """

    _workflows: dict[str, WorkflowGraph] = field(default_factory=dict)

    def save(self, workflow: WorkflowGraph) -> None:
        """Persist the latest workflow state in memory."""
        self._workflows[workflow.workflow_id] = workflow

    def get(self, workflow_id: str) -> WorkflowGraph:
        """Return a workflow by ID."""
        try:
            return self._workflows[workflow_id]
        except KeyError as exc:
            raise WorkflowStoreError(f"Unknown workflow: {workflow_id}") from exc
