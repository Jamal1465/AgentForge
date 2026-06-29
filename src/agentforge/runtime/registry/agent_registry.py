"""Agent registry implementation."""

from __future__ import annotations

from dataclasses import dataclass, field

from agentforge.domain.value_objects import Capability
from agentforge.runtime.plugins.contracts import AgentPlugin


class AgentRegistryError(RuntimeError):
    """Raised when registry operations are invalid."""


@dataclass(slots=True)
class AgentRegistry:
    """Stores and discovers agent plugins.

    The registry preserves plugin-first architecture by allowing agents to be
    discovered by metadata and capability rather than by hardcoded names.
    """

    _agents: dict[str, AgentPlugin] = field(default_factory=dict)

    def register(self, plugin: AgentPlugin) -> None:
        """Register a plugin by its agent ID."""
        agent_id = plugin.metadata.agent_id
        if agent_id in self._agents:
            raise AgentRegistryError(f"Agent already registered: {agent_id}")
        self._agents[agent_id] = plugin

    def get(self, agent_id: str) -> AgentPlugin:
        """Return a registered agent by ID."""
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise AgentRegistryError(f"Unknown agent: {agent_id}") from exc

    def list_agents(self) -> tuple[AgentPlugin, ...]:
        """Return all registered plugins."""
        return tuple(self._agents.values())

    def find_by_capability(self, capability: Capability) -> tuple[AgentPlugin, ...]:
        """Return plugins that provide the requested capability."""
        return tuple(
            agent for agent in self._agents.values() if capability in agent.metadata.capabilities
        )
