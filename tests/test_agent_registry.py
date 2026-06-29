from __future__ import annotations

import pytest

from agentforge.agents.planner.plugin import PlannerAgentPlugin
from agentforge.domain.value_objects import Capability
from agentforge.runtime.registry.agent_registry import AgentRegistry, AgentRegistryError


def test_registry_registers_and_returns_agent() -> None:
    registry = AgentRegistry()
    planner = PlannerAgentPlugin()

    registry.register(planner)

    assert registry.get("builtin.planner") is planner


def test_registry_rejects_duplicate_agent_id() -> None:
    registry = AgentRegistry()
    planner = PlannerAgentPlugin()
    registry.register(planner)

    with pytest.raises(AgentRegistryError, match="Agent already registered"):
        registry.register(planner)


def test_registry_finds_agent_by_capability() -> None:
    registry = AgentRegistry()
    registry.register(PlannerAgentPlugin())

    matches = registry.find_by_capability(Capability("planning"))

    assert len(matches) == 1
    assert matches[0].metadata.agent_id == "builtin.planner"
