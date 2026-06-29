"""ADK demo workflow for AgentForge.

``ADKDemoWorkflow`` demonstrates how AgentForge's capability-first routing
can be exposed through a Google ADK-style agent orchestration layer.

Three capabilities are demonstrated:
- ``requirements-analysis``      — maps to ``RequirementsAgentPlugin``
- ``architecture-documentation`` — maps to ``ArchitectureAgentPlugin``
- ``risk-analysis``              — maps to ``OperationsAgentPlugin``

No agent classes are hardcoded.  The workflow only names *capabilities*.
The ``CapabilityRouter`` resolves the actual plugin at runtime.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.adk.adk_adapter import ADK_AVAILABLE, adk_status_line
from agentforge.adk.adk_capability_agent import ADKCapabilityAgent, ADKCapabilityResult
from agentforge.application.platform import AgentForgePlatform
from agentforge.infrastructure.config import load_settings

# Capabilities demonstrated in the ADK demo — no concrete class names here
_DEMO_CAPABILITIES: tuple[str, ...] = (
    "requirements-analysis",
    "architecture-documentation",
    "risk-analysis",
)


@dataclass(frozen=True, slots=True)
class ADKDemoResult:
    """Aggregated result from the full ADK demo workflow run."""

    description: str
    capability_results: tuple[ADKCapabilityResult, ...]
    adk_available: bool

    @property
    def all_events(self) -> list[dict[str, str]]:
        """Flatten events from all capability runs."""
        events: list[dict[str, str]] = [
            {"event_type": "adk.workflow.started", "capabilities": str(_DEMO_CAPABILITIES)},
        ]
        for cap_result in self.capability_results:
            events.extend(cap_result.events)
        events.append(
            {
                "event_type": "adk.workflow.completed",
                "total_capabilities": str(len(self.capability_results)),
            }
        )
        return events

    def summary_lines(self) -> list[str]:
        """Return human-readable summary lines for CLI output."""
        lines: list[str] = [
            "",
            "=" * 54,
            "     AgentForge  x  Google ADK  Demo",
            "=" * 54,
            "",
            f"  Project : {self.description[:72]}",
            f"  {adk_status_line()}",
            "",
        ]
        for cap_result in self.capability_results:
            status = "✓" if cap_result.confidence > 0 else "✗"
            lines.append(
                f"  {status} [{cap_result.capability}]"
                f"  confidence={cap_result.confidence:.2f}"
            )
            lines.append(f"    {cap_result.summary}")
            lines.append(f"    ADK response: {cap_result.response_text}")
            lines.append("")

        lines += [
            "  -- Events ------------------------------------------",
            "",
        ]
        for event in self.all_events:
            et = event.get("event_type", "")
            extra = {k: v for k, v in event.items() if k != "event_type"}
            extra_str = "  ".join(f"{k}={v}" for k, v in extra.items())
            lines.append(f"  [{et}]  {extra_str}")

        n = len(self.capability_results)
        lines += [
            "",
            f"  Demo complete. {n} capabilities executed via ADK adapter.",
            "",
        ]
        return lines


class ADKDemoWorkflow:
    """Orchestrates a demo workflow using ADK capability agents.

    Usage::

        workflow = ADKDemoWorkflow()
        result = workflow.run("Build a secure FastAPI task manager API")
        print("\\n".join(result.summary_lines()))
    """

    def __init__(self, platform: AgentForgePlatform | None = None) -> None:
        self._platform = platform or AgentForgePlatform.create_default(
            settings=load_settings()
        )

    def run(self, description: str) -> ADKDemoResult:
        """Execute all demo capabilities and return the aggregated result."""
        registry = self._platform.registry
        capability_results: list[ADKCapabilityResult] = []

        for capability in _DEMO_CAPABILITIES:
            agent = ADKCapabilityAgent(
                capability=capability,
                registry=registry,
            )
            result = agent.run_capability(description)
            capability_results.append(result)

        return ADKDemoResult(
            description=description,
            capability_results=tuple(capability_results),
            adk_available=ADK_AVAILABLE,
        )
