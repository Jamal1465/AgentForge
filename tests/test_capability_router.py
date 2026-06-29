from __future__ import annotations

from agentforge.agents.planner.plugin import PlannerAgentPlugin
from agentforge.domain.entities import ProjectTask
from agentforge.domain.value_objects import Capability
from agentforge.runtime.registry.agent_registry import AgentRegistry
from agentforge.runtime.routing.capability_router import CapabilityRouter, RoutingStatus


def test_router_routes_task_to_matching_agent() -> None:
    registry = AgentRegistry()
    registry.register(PlannerAgentPlugin())
    router = CapabilityRouter(registry)
    task = ProjectTask(
        title="Plan project",
        required_capabilities=(Capability("planning"),),
    )

    decision = router.route(task)

    assert decision.status == RoutingStatus.ROUTED
    assert decision.selected_agent_id == "builtin.planner"


def test_router_returns_no_match_when_no_agent_has_capability() -> None:
    router = CapabilityRouter(AgentRegistry())
    task = ProjectTask(
        title="Design backend",
        required_capabilities=(Capability("backend"),),
    )

    decision = router.route(task)

    assert decision.status == RoutingStatus.NO_MATCH
    assert decision.selected_agent_id is None
