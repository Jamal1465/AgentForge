from __future__ import annotations

from dataclasses import dataclass

from agentforge.application.workflows.runner import WorkflowRunner
from agentforge.domain.entities import ProjectTask
from agentforge.domain.value_objects import Capability, RiskLevel
from agentforge.domain.workflow import (
    WorkflowGraph,
    WorkflowNode,
    WorkflowNodeStatus,
    WorkflowStatus,
)
from agentforge.infrastructure.persistence.workflow_store import InMemoryWorkflowStore
from agentforge.runtime.plugins.contracts import (
    AgentExecutionStatus,
    AgentMetadata,
    AgentResult,
)
from agentforge.runtime.registry.agent_registry import AgentRegistry
from agentforge.runtime.routing.capability_router import CapabilityRouter


@dataclass(slots=True)
class StaticAgent:
    capability: Capability
    status: AgentExecutionStatus = AgentExecutionStatus.SUCCESS
    calls: int = 0

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_id=f"test.{self.capability.name}",
            name=f"Test {self.capability.name}",
            version="0.1.0",
            capabilities=(self.capability,),
            risk_level=RiskLevel.LOW,
        )

    def execute(self, task: ProjectTask) -> AgentResult:
        self.calls += 1
        return AgentResult(
            status=self.status,
            summary=f"Handled {task.title}",
            errors=("forced failure",) if self.status == AgentExecutionStatus.FAILED else (),
        )


@dataclass(slots=True)
class FlakyAgent:
    calls: int = 0

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_id="test.flaky",
            name="Flaky Agent",
            version="0.1.0",
            capabilities=(Capability("testing"),),
        )

    def execute(self, task: ProjectTask) -> AgentResult:
        self.calls += 1
        if self.calls == 1:
            return AgentResult(
                status=AgentExecutionStatus.FAILED,
                summary="Temporary failure",
                errors=("temporary failure",),
            )
        return AgentResult(status=AgentExecutionStatus.SUCCESS, summary=f"Recovered {task.title}")


def build_runner(agent: object) -> WorkflowRunner:
    registry = AgentRegistry()
    registry.register(agent)  # type: ignore[arg-type]
    router = CapabilityRouter(registry)
    store = InMemoryWorkflowStore()
    return WorkflowRunner(registry=registry, router=router, store=store)


def test_workflow_runner_completes_dependency_order() -> None:
    capability = Capability("planning")
    agent = StaticAgent(capability=capability)
    runner = build_runner(agent)
    first = WorkflowNode(
        node_id="first",
        title="Plan",
        task=ProjectTask(title="Plan", required_capabilities=(capability,)),
    )
    second = WorkflowNode(
        node_id="second",
        title="Plan details",
        task=ProjectTask(title="Plan details", required_capabilities=(capability,)),
        dependencies=("first",),
    )
    graph = WorkflowGraph(name="Planning workflow", nodes={"first": first, "second": second})

    result = runner.run(graph)

    assert result.status == WorkflowStatus.COMPLETED
    assert result.executed_node_ids == ("first", "second")
    assert first.status == WorkflowNodeStatus.COMPLETED
    assert second.status == WorkflowNodeStatus.COMPLETED
    assert agent.calls == 2


def test_workflow_runner_pauses_and_resumes_for_human_approval() -> None:
    capability = Capability("planning")
    agent = StaticAgent(capability=capability)
    runner = build_runner(agent)
    first = WorkflowNode(
        node_id="approval",
        title="Approve architecture",
        task=ProjectTask(title="Approve architecture", required_capabilities=(capability,)),
        requires_approval=True,
    )
    graph = WorkflowGraph(name="Approval workflow", nodes={"approval": first})

    paused = runner.run(graph)

    assert paused.status == WorkflowStatus.WAITING_FOR_APPROVAL
    assert paused.pending_approval_node_id == "approval"
    assert first.status == WorkflowNodeStatus.WAITING_FOR_APPROVAL
    assert agent.calls == 0

    resumed = runner.resume_after_approval(graph.workflow_id, "approval", approved=True)

    assert resumed.status == WorkflowStatus.COMPLETED
    assert first.status == WorkflowNodeStatus.COMPLETED
    assert agent.calls == 1


def test_workflow_runner_fails_when_approval_rejected() -> None:
    capability = Capability("planning")
    agent = StaticAgent(capability=capability)
    runner = build_runner(agent)
    node = WorkflowNode(
        node_id="approval",
        title="Approve architecture",
        task=ProjectTask(title="Approve architecture", required_capabilities=(capability,)),
        requires_approval=True,
    )
    graph = WorkflowGraph(name="Approval workflow", nodes={"approval": node})

    runner.run(graph)
    result = runner.resume_after_approval(graph.workflow_id, "approval", approved=False)

    assert result.status == WorkflowStatus.FAILED
    assert node.status == WorkflowNodeStatus.FAILED
    assert agent.calls == 0


def test_workflow_runner_retries_failed_agent_result() -> None:
    agent = FlakyAgent()
    runner = build_runner(agent)
    node = WorkflowNode(
        node_id="test",
        title="Run tests",
        task=ProjectTask(title="Run tests", required_capabilities=(Capability("testing"),)),
        max_attempts=2,
    )
    graph = WorkflowGraph(name="Retry workflow", nodes={"test": node})

    result = runner.run(graph)

    assert result.status == WorkflowStatus.COMPLETED
    assert node.status == WorkflowNodeStatus.COMPLETED
    assert agent.calls == 2
    assert node.attempt_count == 2


def test_workflow_runner_fails_when_no_agent_can_route_task() -> None:
    registry = AgentRegistry()
    runner = WorkflowRunner(
        registry=registry,
        router=CapabilityRouter(registry),
        store=InMemoryWorkflowStore(),
    )
    node = WorkflowNode(
        node_id="backend",
        title="Build backend",
        task=ProjectTask(title="Build backend", required_capabilities=(Capability("backend"),)),
    )
    graph = WorkflowGraph(name="No route workflow", nodes={"backend": node})

    result = runner.run(graph)

    assert result.status == WorkflowStatus.FAILED
    assert node.status == WorkflowNodeStatus.FAILED
    assert "No registered agent" in (result.error or "")
