"""Pure domain model for AgentForge workflow graphs.

The domain workflow model is intentionally framework-free. It represents the
minimum concepts required for deterministic orchestration: workflow nodes,
dependencies, approval gates, retry limits, and state transitions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4

from agentforge.domain.entities import Artifact, ProjectTask


class WorkflowStatus(StrEnum):
    """Lifecycle state for a workflow graph."""

    PENDING = "pending"
    RUNNING = "running"
    WAITING_FOR_APPROVAL = "waiting_for_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowNodeStatus(StrEnum):
    """Lifecycle state for an individual workflow node."""

    PENDING = "pending"
    RUNNING = "running"
    WAITING_FOR_APPROVAL = "waiting_for_approval"
    APPROVED = "approved"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowDomainError(ValueError):
    """Raised when a workflow graph violates domain invariants."""


@dataclass(slots=True)
class WorkflowNode:
    """One executable unit inside a workflow graph.

    A node may wrap a ProjectTask that can be routed to an agent. Nodes can also
    represent approval gates or future non-agent actions, so ``task`` is optional.
    """

    title: str
    task: ProjectTask | None = None
    dependencies: tuple[str, ...] = ()
    requires_approval: bool = False
    max_attempts: int = 1
    node_id: str = field(default_factory=lambda: str(uuid4()))
    status: WorkflowNodeStatus = WorkflowNodeStatus.PENDING
    attempt_count: int = 0
    approval_granted: bool = False
    last_error: str | None = None
    artifacts: tuple[Artifact, ...] = ()

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise WorkflowDomainError("Workflow node title cannot be empty.")
        if self.max_attempts < 1:
            raise WorkflowDomainError("Workflow node max_attempts must be at least 1.")
        if self.node_id in self.dependencies:
            raise WorkflowDomainError("Workflow node cannot depend on itself.")

    def is_terminal(self) -> bool:
        """Return True when this node no longer needs execution."""
        return self.status in {
            WorkflowNodeStatus.COMPLETED,
            WorkflowNodeStatus.FAILED,
            WorkflowNodeStatus.SKIPPED,
        }

    def is_ready(self, completed_node_ids: set[str]) -> bool:
        """Return True when all dependencies have completed."""
        return self.status == WorkflowNodeStatus.PENDING and set(self.dependencies).issubset(
            completed_node_ids
        )


@dataclass(frozen=True, slots=True)
class WorkflowEvent:
    """Immutable audit event emitted by workflow execution."""

    workflow_id: str
    event_type: str
    message: str
    node_id: str | None = None

    def __post_init__(self) -> None:
        if not self.workflow_id.strip():
            raise WorkflowDomainError("Workflow event workflow_id cannot be empty.")
        if not self.event_type.strip():
            raise WorkflowDomainError("Workflow event event_type cannot be empty.")
        if not self.message.strip():
            raise WorkflowDomainError("Workflow event message cannot be empty.")


@dataclass(slots=True)
class WorkflowGraph:
    """Directed acyclic graph of workflow nodes."""

    name: str
    nodes: dict[str, WorkflowNode]
    workflow_id: str = field(default_factory=lambda: str(uuid4()))
    status: WorkflowStatus = WorkflowStatus.PENDING
    events: list[WorkflowEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise WorkflowDomainError("Workflow name cannot be empty.")
        if not self.nodes:
            raise WorkflowDomainError("Workflow graph must contain at least one node.")
        self._validate_node_keys()
        self._validate_dependencies_exist()
        self._validate_acyclic()

    def _validate_node_keys(self) -> None:
        for node_id, node in self.nodes.items():
            if node_id != node.node_id:
                raise WorkflowDomainError("Workflow node dictionary key must match node_id.")

    def _validate_dependencies_exist(self) -> None:
        known = set(self.nodes)
        for node in self.nodes.values():
            missing = set(node.dependencies) - known
            if missing:
                missing_list = ", ".join(sorted(missing))
                raise WorkflowDomainError(f"Workflow node has unknown dependencies: {missing_list}")

    def _validate_acyclic(self) -> None:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in visited:
                return
            if node_id in visiting:
                raise WorkflowDomainError("Workflow graph cannot contain dependency cycles.")
            visiting.add(node_id)
            for dependency_id in self.nodes[node_id].dependencies:
                visit(dependency_id)
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in self.nodes:
            visit(node_id)

    def record_event(
        self,
        event_type: str,
        message: str,
        node_id: str | None = None,
    ) -> None:
        """Append an auditable workflow event."""
        self.events.append(
            WorkflowEvent(
                workflow_id=self.workflow_id,
                event_type=event_type,
                message=message,
                node_id=node_id,
            )
        )

    def completed_node_ids(self) -> set[str]:
        """Return node IDs that completed successfully."""
        return {
            node_id
            for node_id, node in self.nodes.items()
            if node.status == WorkflowNodeStatus.COMPLETED
        }

    def ready_nodes(self) -> tuple[WorkflowNode, ...]:
        """Return pending nodes whose dependencies have completed."""
        completed = self.completed_node_ids()
        return tuple(node for node in self.nodes.values() if node.is_ready(completed))

    def has_failed_nodes(self) -> bool:
        """Return True when at least one node has failed."""
        return any(node.status == WorkflowNodeStatus.FAILED for node in self.nodes.values())

    def all_nodes_completed(self) -> bool:
        """Return True when all nodes completed successfully."""
        return all(node.status == WorkflowNodeStatus.COMPLETED for node in self.nodes.values())
