from __future__ import annotations

from dataclasses import dataclass

from agentforge.application.observability.service import ObservabilityService
from agentforge.application.workflows.runner import WorkflowRunner
from agentforge.domain.entities import Artifact, ProjectTask
from agentforge.domain.value_objects import Capability, RiskLevel
from agentforge.domain.workflow import WorkflowGraph, WorkflowNode, WorkflowStatus
from agentforge.infrastructure.persistence.observability_store import InMemoryObservabilityStore
from agentforge.infrastructure.persistence.workflow_store import InMemoryWorkflowStore
from agentforge.runtime.plugins.contracts import AgentExecutionStatus, AgentMetadata, AgentResult
from agentforge.runtime.registry.agent_registry import AgentRegistry
from agentforge.runtime.routing.capability_router import CapabilityRouter


@dataclass(slots=True)
class ObservableAgent:
    capability: Capability

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_id="test.observable",
            name="Observable Agent",
            version="0.1.0",
            capabilities=(self.capability,),
            risk_level=RiskLevel.LOW,
        )

    def execute(self, task: ProjectTask) -> AgentResult:
        return AgentResult(
            status=AgentExecutionStatus.SUCCESS,
            summary=f"Handled {task.title}",
            confidence=0.95,
            artifacts=(Artifact(name="output.md", content="# Output\n\nDetailed content."),),
        )


def test_workflow_runner_emits_workflow_node_routing_and_plugin_telemetry() -> None:
    capability = Capability("api-development")
    agent = ObservableAgent(capability=capability)
    registry = AgentRegistry()
    registry.register(agent)
    telemetry_store = InMemoryObservabilityStore()
    runner = WorkflowRunner(
        registry=registry,
        router=CapabilityRouter(registry),
        store=InMemoryWorkflowStore(),
        observability_service=ObservabilityService(store=telemetry_store),
    )
    node = WorkflowNode(
        node_id="api",
        title="Design API",
        task=ProjectTask(title="Design API", required_capabilities=(capability,)),
    )
    workflow = WorkflowGraph(name="Observable workflow", nodes={"api": node})

    result = runner.run(workflow)

    assert result.status == WorkflowStatus.COMPLETED
    events = telemetry_store.list_events(trace_id=workflow.workflow_id)
    event_names = {event.name for event in events}
    assert "workflow.started" in event_names
    assert "node.started" in event_names
    assert "routing.routed" in event_names
    assert "plugin.execution.success" in event_names
    assert "node.completed" in event_names
    assert "workflow.completed" in event_names
    assert telemetry_store.list_metrics(name="workflow.finished_total")
