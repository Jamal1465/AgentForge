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

        This implementation is intentionally deterministic so tests can validate
        the plugin system before live model calls are introduced.
        """
        plan = f"""# Project Plan

Task: {task.title}

## Recommended Phases

1. Clarify requirements.
2. Generate architecture.
3. Build repository scaffold.
4. Implement core features.
5. Add tests and evaluation.
6. Prepare deployment and documentation.
"""
        return AgentResult(
            status=AgentExecutionStatus.SUCCESS,
            summary="Generated initial deterministic project plan.",
            artifacts=(Artifact(name="project_plan.md", content=plan),),
            decisions=("Use staged software engineering workflow.",),
            confidence=0.8,
            next_actions=("Route architecture task to an architect-capable agent.",),
        )
