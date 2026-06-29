"""AgentForge platform composition root.

The platform object wires together domain, application, runtime, and
infrastructure components. Interfaces such as CLI, HTTP, tests, and future ADK
entry points should depend on this object instead of reconstructing services.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.agents.planner.plugin import PlannerAgentPlugin
from agentforge.application.evaluation.service import EvaluationService
from agentforge.application.memory.service import MemoryService
from agentforge.application.observability.service import ObservabilityService
from agentforge.application.security.service import SecurityService
from agentforge.application.workflows.runner import WorkflowRunner, WorkflowRunResult
from agentforge.domain.entities import ProjectTask
from agentforge.domain.value_objects import Capability
from agentforge.domain.workflow import WorkflowGraph, WorkflowNode, WorkflowStatus
from agentforge.infrastructure.config import AgentForgeSettings, load_settings
from agentforge.infrastructure.persistence.evaluation_store import InMemoryEvaluationStore
from agentforge.infrastructure.persistence.memory_store import InMemoryMemoryStore
from agentforge.infrastructure.persistence.observability_store import InMemoryObservabilityStore
from agentforge.infrastructure.persistence.security_audit_store import InMemorySecurityAuditStore
from agentforge.infrastructure.persistence.workflow_store import InMemoryWorkflowStore
from agentforge.runtime.plugins.contracts import AgentPlugin
from agentforge.runtime.registry.agent_registry import AgentRegistry
from agentforge.runtime.routing.capability_router import CapabilityRouter


@dataclass(frozen=True, slots=True)
class PlatformHealth:
    """Health or readiness status exposed by interfaces."""

    status: str
    service: str
    version: str
    registered_plugins: int
    details: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        """Serialize health status for CLI or HTTP responses."""
        return {
            "status": self.status,
            "service": self.service,
            "version": self.version,
            "registered_plugins": self.registered_plugins,
            "details": dict(self.details),
        }


@dataclass(slots=True)
class ProjectRunSummary:
    """Interface-friendly summary for a project workflow execution."""

    workflow_id: str
    status: str
    executed_node_ids: tuple[str, ...]
    pending_approval_node_id: str | None
    error: str | None
    events: tuple[dict[str, str | None], ...]
    output_path: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Serialize project workflow summary."""
        return {
            "workflow_id": self.workflow_id,
            "status": self.status,
            "executed_node_ids": list(self.executed_node_ids),
            "pending_approval_node_id": self.pending_approval_node_id,
            "error": self.error,
            "events": list(self.events),
            "output_path": self.output_path,
        }


@dataclass(slots=True)
class AgentForgePlatform:
    """High-level composition root used by all external interfaces."""

    settings: AgentForgeSettings
    registry: AgentRegistry
    router: CapabilityRouter
    workflow_store: InMemoryWorkflowStore
    workflow_runner: WorkflowRunner
    memory_service: MemoryService
    security_service: SecurityService
    evaluation_service: EvaluationService
    observability_service: ObservabilityService

    @classmethod
    def create_default(
        cls,
        *,
        settings: AgentForgeSettings | None = None,
        plugins: tuple[AgentPlugin, ...] | None = None,
    ) -> AgentForgePlatform:
        """Create a local in-memory AgentForge runtime."""
        active_settings = settings or load_settings()
        registry = AgentRegistry()
        if plugins is None:
            from agentforge.agents.artifact_agents import (
                ArchitectureAgentPlugin,
                BriefAgentPlugin,
                ImplementationAgentPlugin,
                OperationsAgentPlugin,
                RequirementsAgentPlugin,
            )
            plugins = (
                PlannerAgentPlugin(),
                BriefAgentPlugin(),
                RequirementsAgentPlugin(),
                ArchitectureAgentPlugin(),
                ImplementationAgentPlugin(),
                OperationsAgentPlugin(),
            )
        for plugin in plugins:
            registry.register(plugin)

        router = CapabilityRouter(registry)
        workflow_store = InMemoryWorkflowStore()
        memory_service = MemoryService(store=InMemoryMemoryStore())
        security_service = SecurityService(audit_store=InMemorySecurityAuditStore())
        evaluation_service = EvaluationService(store=InMemoryEvaluationStore())
        observability_service = ObservabilityService(store=InMemoryObservabilityStore())
        runner = WorkflowRunner(
            registry=registry,
            router=router,
            store=workflow_store,
            memory_service=memory_service,
            security_service=security_service,
            evaluation_service=evaluation_service,
            observability_service=observability_service,
        )
        return cls(
            settings=active_settings,
            registry=registry,
            router=router,
            workflow_store=workflow_store,
            workflow_runner=runner,
            memory_service=memory_service,
            security_service=security_service,
            evaluation_service=evaluation_service,
            observability_service=observability_service,
        )

    def health(self) -> PlatformHealth:
        """Return liveness information."""
        return PlatformHealth(
            status="ok",
            service=self.settings.app_name,
            version="0.1.0",
            registered_plugins=len(self.registry.list_agents()),
            details={"environment": self.settings.environment.value},
        )

    def readiness(self) -> PlatformHealth:
        """Return readiness information for deployment health checks."""
        planner_available = bool(self.registry.find_by_capability(Capability("planning")))
        status = "ready" if planner_available else "not_ready"
        return PlatformHealth(
            status=status,
            service=self.settings.app_name,
            version="0.1.0",
            registered_plugins=len(self.registry.list_agents()),
            details={"planning_capability": str(planner_available).lower()},
        )

    def create_planning_workflow(self, description: str) -> WorkflowGraph:
        """Create a capability-routed planning workflow from a project idea."""
        task = ProjectTask(
            title="Create initial project plan",
            description=description,
            required_capabilities=(Capability("planning"),),
        )
        nodes = {
            "plan": WorkflowNode(node_id="plan", title="Create initial project plan", task=task)
        }

        # Add 10 artifact nodes, which depend on "plan"
        artifact_specs = [
            ("01_project_brief", "01_Project_Brief.md", "project-brief-generation"),
            (
                "02_functional_requirements",
                "02_Functional_Requirements.md",
                "requirements-analysis",
            ),
            (
                "03_non_functional_requirements",
                "03_Non_Functional_Requirements.md",
                "non-functional-requirements-analysis",
            ),
            ("04_feasibility_study", "04_Feasibility_Study.md", "feasibility-analysis"),
            ("05_system_architecture", "05_System_Architecture.md", "architecture-documentation"),
            ("06_technology_stack", "06_Technology_Stack.md", "technology-stack-recommendation"),
            ("07_implementation_plan", "07_Implementation_Plan.md", "implementation-planning"),
            ("08_testing_strategy", "08_Testing_Strategy.md", "testing-strategy"),
            ("09_deployment_plan", "09_Deployment_Plan.md", "deployment-planning"),
            ("10_risk_assessment", "10_Risk_Assessment.md", "risk-analysis"),
        ]

        for node_id, filename, capability in artifact_specs:
            nodes[node_id] = WorkflowNode(
                node_id=node_id,
                title=f"Generate {filename}",
                task=ProjectTask(
                    title=f"Generate {filename}",
                    description=description,
                    required_capabilities=(Capability(capability),),
                ),
                dependencies=("plan",),
            )

        return WorkflowGraph(
            name="AgentForge project planning workflow", nodes=nodes
        )

    def _write_workflow_artifacts(
        self,
        result_status: WorkflowStatus,
        workflow: WorkflowGraph,
    ) -> None:
        import os
        if result_status == WorkflowStatus.COMPLETED:
            output_dir = os.path.join("generated_projects", workflow.workflow_id)
            os.makedirs(output_dir, exist_ok=True)
            for node in workflow.nodes.values():
                for artifact in node.artifacts:
                    file_path = os.path.join(output_dir, artifact.name)
                    # Dynamically replace workflow_id placeholder
                    content = artifact.content.replace("{{workflow_id}}", workflow.workflow_id)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)

    def run_project_request(self, description: str) -> ProjectRunSummary:
        """Create and execute the planning workflow for a natural-language request."""
        workflow = self.create_planning_workflow(description)
        result = self.workflow_runner.run(workflow)
        stored = self.workflow_store.get(result.workflow_id)
        self._write_workflow_artifacts(result.status, stored)
        return self._summarize(result, stored)

    def approve_workflow(
        self,
        *,
        workflow_id: str,
        node_id: str,
        approved: bool,
    ) -> ProjectRunSummary:
        """Resume a workflow that is waiting for human approval."""
        result = self.workflow_runner.resume_after_approval(
            workflow_id=workflow_id,
            node_id=node_id,
            approved=approved,
        )
        workflow = self.workflow_store.get(result.workflow_id)
        self._write_workflow_artifacts(result.status, workflow)
        return self._summarize(result, workflow)

    @staticmethod
    def _summarize(result: WorkflowRunResult, workflow: WorkflowGraph) -> ProjectRunSummary:
        events = tuple(
            {
                "event_type": event.event_type,
                "message": event.message,
                "node_id": event.node_id,
            }
            for event in workflow.events
        )
        is_completed = result.status == WorkflowStatus.COMPLETED
        output_path = (
            f"generated_projects/{result.workflow_id}"
            if is_completed
            else None
        )
        return ProjectRunSummary(
            workflow_id=result.workflow_id,
            status=result.status.value,
            executed_node_ids=result.executed_node_ids,
            pending_approval_node_id=result.pending_approval_node_id,
            error=result.error,
            events=events,
            output_path=output_path,
        )
