"""ADK-backed capability agent for AgentForge.

``ADKCapabilityAgent`` bridges the Google ADK agent interface and the
AgentForge capability-routing system.  It exposes an ADK-compatible ``.run()``
method while delegating all domain logic to whatever ``AgentPlugin`` the
capability registry resolves at runtime.

This is the correct way to integrate an external agent framework into
AgentForge: wrap it as a capability-routed plugin, never hardcode a concrete
agent class.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.adk.adk_adapter import ADK_AVAILABLE, ADKRunResponse, _StubADKAgent
from agentforge.domain.entities import ProjectTask
from agentforge.domain.value_objects import Capability
from agentforge.runtime.plugins.contracts import AgentPlugin
from agentforge.runtime.registry.agent_registry import AgentRegistry


@dataclass(frozen=True, slots=True)
class ADKCapabilityResult:
    """Structured result produced by an ADK capability agent run."""

    capability: str
    summary: str
    response_text: str
    confidence: float
    adk_available: bool
    events: tuple[dict[str, str], ...]


class ADKCapabilityAgent(_StubADKAgent):
    """An ADK agent that delegates work to a capability-registered AgentForge plugin.

    Rather than containing domain logic itself, this agent asks the
    ``AgentRegistry`` to find the registered ``AgentPlugin`` that claims
    the requested capability, then invokes it.

    Example capabilities: ``requirements-analysis``,
    ``architecture-documentation``, ``risk-analysis``.
    """

    def __init__(
        self,
        capability: str,
        registry: AgentRegistry,
        description: str = "",
    ) -> None:
        super().__init__(
            name=f"adk-{capability}",
            model="gemini-2.0-flash",
            description=description or f"ADK agent for capability: {capability}",
            instruction=(
                f"You are a specialized agent responsible for the '{capability}' "
                "capability within the AgentForge platform. "
                "Analyze the project description and produce a structured output."
            ),
        )
        self._capability = capability
        self._registry = registry

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_capability(self, project_description: str) -> ADKCapabilityResult:
        """Route to the correct AgentForge plugin and return a unified result.

        This method:
        1. Resolves the plugin via capability registry (never by class name).
        2. Builds a ``ProjectTask`` with only the required capability tag.
        3. Invokes ``plugin.execute(task)``.
        4. Wraps the result in an ``ADKCapabilityResult``.
        """
        cap = Capability(self._capability)
        matches: tuple[AgentPlugin, ...] = self._registry.find_by_capability(cap)

        events: list[dict[str, str]] = [
            {"event_type": "adk.agent.started", "capability": self._capability},
        ]

        if not matches:
            events.append(
                {"event_type": "adk.agent.no_plugin", "capability": self._capability}
            )
            return ADKCapabilityResult(
                capability=self._capability,
                summary=f"No plugin registered for capability: {self._capability}",
                response_text="",
                confidence=0.0,
                adk_available=ADK_AVAILABLE,
                events=tuple(events),
            )

        # Use the first matching plugin (deterministic: alphabetical agent_id order)
        plugin: AgentPlugin = sorted(matches, key=lambda p: p.metadata.agent_id)[0]

        task = ProjectTask(
            title=f"ADK: {self._capability}",
            description=project_description,
            required_capabilities=(cap,),
        )

        agent_result = plugin.execute(task)

        events.append(
            {
                "event_type": "adk.agent.plugin_resolved",
                "capability": self._capability,
                "plugin_id": plugin.metadata.agent_id,
            }
        )
        events.append(
            {
                "event_type": "adk.agent.completed",
                "capability": self._capability,
                "status": agent_result.status.value,
            }
        )

        # Also call ADKAgentBase.run() to demonstrate the ADK interface
        adk_response: ADKRunResponse = self.run(
            f"[{self._capability}] {project_description[:120]}"
        )

        return ADKCapabilityResult(
            capability=self._capability,
            summary=agent_result.summary,
            response_text=str(adk_response),
            confidence=agent_result.confidence,
            adk_available=ADK_AVAILABLE,
            events=tuple(events),
        )
