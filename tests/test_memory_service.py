from __future__ import annotations

from agentforge.application.memory.service import MemoryService
from agentforge.domain.memory import MemoryKind, MemoryQuery, MemoryScope
from agentforge.infrastructure.persistence.memory_store import InMemoryMemoryStore


def test_memory_service_remembers_project_requirement_and_renders_context() -> None:
    service = MemoryService(store=InMemoryMemoryStore())
    record = service.remember_project_requirement(
        "project-1",
        "AgentForge must support plugin-based agents.",
        tags=("architecture", "plugins"),
    )

    context = service.retrieve_context(
        MemoryQuery(text="plugin agents", scopes=(MemoryScope.PROJECT,), owner_ids=("project-1",))
    )

    assert context.records == (record,)
    assert "Retrieved AgentForge Memory" in context.rendered_text
    assert "plugin-based agents" in context.rendered_text


def test_memory_service_records_workflow_events_with_node_metadata() -> None:
    service = MemoryService(store=InMemoryMemoryStore())

    record = service.remember_workflow_event(
        "workflow-1",
        "Workflow node completed successfully.",
        tags=("node", "completed"),
        node_id="node-1",
    )

    assert record.scope == MemoryScope.WORKFLOW
    assert record.kind == MemoryKind.WORKFLOW_EVENT
    assert record.metadata == {"node_id": "node-1"}


def test_memory_service_returns_empty_context_message() -> None:
    service = MemoryService(store=InMemoryMemoryStore())

    context = service.retrieve_context(MemoryQuery(text="missing"))

    assert context.is_empty
    assert context.rendered_text == "No relevant memory found."
