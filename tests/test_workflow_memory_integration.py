from __future__ import annotations

from dataclasses import dataclass

from agentforge.application.memory.service import MemoryService
from agentforge.application.workflows.runner import WorkflowRunner
from agentforge.domain.entities import ProjectTask
from agentforge.domain.memory import MemoryQuery, MemoryScope
from agentforge.domain.value_objects import Capability
from agentforge.domain.workflow import WorkflowGraph, WorkflowNode, WorkflowStatus
from agentforge.infrastructure.persistence.memory_store import InMemoryMemoryStore
from agentforge.infrastructure.persistence.workflow_store import InMemoryWorkflowStore
from agentforge.runtime.plugins.contracts import AgentExecutionStatus, AgentMetadata, AgentResult
from agentforge.runtime.registry.agent_registry import AgentRegistry
from agentforge.runtime.routing.capability_router import CapabilityRouter


@dataclass(slots=True)
class MemoryAwareTestAgent:
    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_id="test.memory",
            name="Memory Test Agent",
            version="0.1.0",
            capabilities=(Capability("planning"),),
        )

    def execute(self, task: ProjectTask) -> AgentResult:
        return AgentResult(status=AgentExecutionStatus.SUCCESS, summary=f"Completed {task.title}")


def test_workflow_runner_records_workflow_memory() -> None:
    registry = AgentRegistry()
    registry.register(MemoryAwareTestAgent())
    memory_store = InMemoryMemoryStore()
    memory_service = MemoryService(store=memory_store)
    runner = WorkflowRunner(
        registry=registry,
        router=CapabilityRouter(registry),
        store=InMemoryWorkflowStore(),
        memory_service=memory_service,
    )
    node = WorkflowNode(
        node_id="plan",
        title="Plan",
        task=ProjectTask(title="Plan", required_capabilities=(Capability("planning"),)),
    )
    graph = WorkflowGraph(name="Memory workflow", nodes={"plan": node})

    result = runner.run(graph)

    assert result.status == WorkflowStatus.COMPLETED
    context = memory_service.retrieve_context(
        MemoryQuery(
            text="workflow completed",
            scopes=(MemoryScope.WORKFLOW,),
            owner_ids=(graph.workflow_id,),
        )
    )
    assert not context.is_empty
    assert any("Workflow execution completed" in record.content for record in context.records)
