"""Application ports for workflow orchestration."""

from __future__ import annotations

from typing import Protocol

from agentforge.domain.workflow import WorkflowGraph


class WorkflowStore(Protocol):
    """Persistence boundary used by the workflow runner."""

    def save(self, workflow: WorkflowGraph) -> None:
        """Persist the latest workflow state."""
        ...

    def get(self, workflow_id: str) -> WorkflowGraph:
        """Load a workflow by ID."""
        ...
