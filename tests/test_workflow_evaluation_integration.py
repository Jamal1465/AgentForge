from __future__ import annotations

from dataclasses import dataclass

from agentforge.application.evaluation.service import EvaluationService
from agentforge.application.workflows.runner import WorkflowRunner
from agentforge.domain.entities import Artifact, ProjectTask
from agentforge.domain.value_objects import Capability
from agentforge.domain.workflow import (
    WorkflowGraph,
    WorkflowNode,
    WorkflowNodeStatus,
    WorkflowStatus,
)
from agentforge.infrastructure.persistence.evaluation_store import InMemoryEvaluationStore
from agentforge.infrastructure.persistence.workflow_store import InMemoryWorkflowStore
from agentforge.runtime.plugins.contracts import AgentExecutionStatus, AgentMetadata, AgentResult
from agentforge.runtime.registry.agent_registry import AgentRegistry
from agentforge.runtime.routing.capability_router import CapabilityRouter


@dataclass(slots=True)
class EvaluatedAgent:
    confidence: float = 0.9

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_id="plugin.evaluated",
            name="Evaluated Plugin",
            version="0.1.0",
            capabilities=(Capability("api-development"),),
        )

    def execute(self, task: ProjectTask) -> AgentResult:
        return AgentResult(
            status=AgentExecutionStatus.SUCCESS,
            summary=f"Handled {task.title}",
            confidence=self.confidence,
            artifacts=(
                Artifact(name="output.md", content="# Output\n\nDetailed output from plugin."),
            ),
        )


def build_runner(agent: EvaluatedAgent, store: InMemoryEvaluationStore) -> WorkflowRunner:
    registry = AgentRegistry()
    registry.register(agent)
    return WorkflowRunner(
        registry=registry,
        router=CapabilityRouter(registry),
        store=InMemoryWorkflowStore(),
        evaluation_service=EvaluationService(store=store),
    )


def test_workflow_runner_records_evaluation_report_for_successful_node() -> None:
    evaluation_store = InMemoryEvaluationStore()
    runner = build_runner(EvaluatedAgent(confidence=0.95), evaluation_store)
    node = WorkflowNode(
        node_id="api",
        title="Implement API",
        task=ProjectTask(
            title="Implement API", required_capabilities=(Capability("api-development"),)
        ),
    )
    graph = WorkflowGraph(name="Evaluation workflow", nodes={"api": node})

    result = runner.run(graph)

    assert result.status == WorkflowStatus.COMPLETED
    assert node.status == WorkflowNodeStatus.COMPLETED
    reports = evaluation_store.list_by_workflow(graph.workflow_id)
    assert len(reports) == 1
    assert reports[0].subject.capabilities == (Capability("api-development"),)
    assert any(event.event_type.startswith("evaluation.") for event in graph.events)


def test_workflow_runner_fails_node_when_evaluation_quality_gate_fails() -> None:
    evaluation_store = InMemoryEvaluationStore()
    runner = build_runner(EvaluatedAgent(confidence=0.1), evaluation_store)
    node = WorkflowNode(
        node_id="api",
        title="Implement API",
        task=ProjectTask(
            title="Implement API", required_capabilities=(Capability("api-development"),)
        ),
    )
    graph = WorkflowGraph(name="Evaluation failure workflow", nodes={"api": node})

    result = runner.run(graph)

    assert result.status == WorkflowStatus.FAILED
    assert node.status == WorkflowNodeStatus.FAILED
    assert "Evaluation quality gate failed" in (node.last_error or "")
    assert evaluation_store.list_by_workflow(graph.workflow_id)
