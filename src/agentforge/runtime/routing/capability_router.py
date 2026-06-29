"""Capability-based task router."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from agentforge.domain.entities import ProjectTask
from agentforge.runtime.plugins.contracts import AgentPlugin
from agentforge.runtime.registry.agent_registry import AgentRegistry


class RoutingStatus(StrEnum):
    """Routing outcome."""

    ROUTED = "routed"
    NO_MATCH = "no_match"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    """Explains how a task was routed."""

    status: RoutingStatus
    task_id: str
    selected_agent_id: str | None
    reason: str
    candidate_agent_ids: tuple[str, ...]


@dataclass(slots=True)
class CapabilityRouter:
    """Routes tasks to agents using declared capabilities."""

    registry: AgentRegistry

    def route(self, task: ProjectTask) -> RoutingDecision:
        """Select the best agent for a task.

        Version 1 routing requires one agent to satisfy all requested capabilities.
        Later milestones can replace scoring without changing the public contract.
        """
        candidates: list[AgentPlugin] = []
        required = set(task.required_capabilities)

        for agent in self.registry.list_agents():
            provided = set(agent.metadata.capabilities)
            if required.issubset(provided):
                candidates.append(agent)

        candidate_ids = tuple(agent.metadata.agent_id for agent in candidates)

        if not candidates:
            return RoutingDecision(
                status=RoutingStatus.NO_MATCH,
                task_id=task.task_id,
                selected_agent_id=None,
                reason="No registered agent satisfies all required capabilities.",
                candidate_agent_ids=(),
            )

        if len(candidates) > 1:
            selected = sorted(candidates, key=lambda agent: agent.metadata.agent_id)[0]
            return RoutingDecision(
                status=RoutingStatus.AMBIGUOUS,
                task_id=task.task_id,
                selected_agent_id=selected.metadata.agent_id,
                reason="Multiple agents matched; selected deterministic first agent ID.",
                candidate_agent_ids=candidate_ids,
            )

        selected = candidates[0]
        return RoutingDecision(
            status=RoutingStatus.ROUTED,
            task_id=task.task_id,
            selected_agent_id=selected.metadata.agent_id,
            reason="Exactly one agent matched required capabilities.",
            candidate_agent_ids=candidate_ids,
        )
