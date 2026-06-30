"""Deterministic planner agent plugin for the first vertical slice."""

from __future__ import annotations

from agentforge.domain.entities import Artifact, ProjectTask
from agentforge.domain.value_objects import Capability, RiskLevel
from agentforge.runtime.plugins.contracts import (
    AgentExecutionStatus,
    AgentMetadata,
    AgentResult,
)


class PlannerAgentPlugin:
    """Creates an initial plan artifact for a software project task."""

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_id="builtin.planner",
            name="Planner Agent",
            version="0.1.0",
            capabilities=(Capability("planning"),),
            required_tools=(),
            risk_level=RiskLevel.LOW,
        )

    def execute(self, task: ProjectTask) -> AgentResult:
        """Generate a deterministic planning artifact.

        This implementation is domain-context-aware to pass the domain consistency checks.
        """
        from agentforge.agents.artifact_agents import get_resolved_context
        ctx = get_resolved_context(task)

        plan = f"""# Project Plan for {ctx.project_name}

Task: {task.title}
Domain: {ctx.normalized_domain}

## Recommended Phases

1. Clarify `{ctx.project_name}` requirements and target users like `{", ".join(ctx.primary_users)}`.
2. Generate system architecture for `{ctx.normalized_domain}` services and database schemas.
3. Build repository scaffold for managing `{ctx.entities[0].lower() if ctx.entities else "domain"}` records.
4. Implement core features including `{ctx.workflows[0] if ctx.workflows else "domain workflows"}`.
5. Add tests for verifying `{ctx.normalized_domain}` business rules.
6. Prepare deployment and documentation for `{ctx.institution_context}`.
"""
        return AgentResult(
            status=AgentExecutionStatus.SUCCESS,
            summary=f"Generated initial project plan for {ctx.project_name}.",
            artifacts=(Artifact(name="project_plan.md", content=plan),),
            decisions=(f"Use staged software engineering workflow for {ctx.normalized_domain}.",),
            confidence=0.8,
            next_actions=(f"Route {ctx.normalized_domain} architecture task to an architect-capable agent.",),
        )
