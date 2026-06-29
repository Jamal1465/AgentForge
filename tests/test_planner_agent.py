from __future__ import annotations

from agentforge.agents.planner.plugin import PlannerAgentPlugin
from agentforge.domain.entities import ProjectTask
from agentforge.domain.value_objects import Capability
from agentforge.runtime.plugins.contracts import AgentExecutionStatus


def test_planner_agent_returns_structured_result() -> None:
    planner = PlannerAgentPlugin()
    task = ProjectTask(
        title="Create plan",
        description="Build a FastAPI app",
        required_capabilities=(Capability("planning"),),
    )

    result = planner.execute(task)

    assert result.status == AgentExecutionStatus.SUCCESS
    assert result.artifacts
    assert result.artifacts[0].name == "project_plan.md"
    assert "Recommended Phases" in result.artifacts[0].content
