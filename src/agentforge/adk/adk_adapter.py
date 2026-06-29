"""Google ADK adapter for AgentForge.

This module attempts to import the real ``google.adk`` package.  If it is not
installed the adapter falls back to a minimal local stub so the rest of the
AgentForge ADK integration can run and be tested without requiring the SDK.

The ``ADK_AVAILABLE`` flag lets callers branch on whether the real SDK is
present.  All ADK integration code in this package must import through this
module — never directly from ``google.adk`` — so the boundary is enforced in
one place.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ADKRunResponse:
    """Unified response object returned by both real SDK and stub agents."""

    agent_name: str
    prompt: str
    text: str
    is_stub: bool = False
    metadata: dict[str, str] = field(default_factory=dict)

    def __str__(self) -> str:
        sdk_label = "stub" if self.is_stub else "real-adk"
        return f"[{sdk_label}][{self.agent_name}] {self.text}"


# ---------------------------------------------------------------------------
# Stub base classes — used when google-adk is not installed
# ---------------------------------------------------------------------------


class _StubADKAgent:
    """Local stub mirroring google.adk.agents.Agent interface."""

    name: str
    model: str
    description: str
    instruction: str

    def __init__(
        self,
        name: str,
        model: str = "gemini-2.0-flash",
        description: str = "",
        instruction: str = "",
        **_kwargs: Any,
    ) -> None:
        self.name = name
        self.model = model
        self.description = description
        self.instruction = instruction

    def run(self, prompt: str) -> ADKRunResponse:
        """Simulate a synchronous ADK agent run."""
        return ADKRunResponse(
            agent_name=self.name,
            prompt=prompt,
            text=f"[stub] {self.name} processed: {prompt[:80]}",
            is_stub=True,
        )


class _StubADKRunner:
    """Local stub mirroring google.adk.runners.Runner interface."""

    def __init__(self, agent: _StubADKAgent, **_kwargs: Any) -> None:
        self.agent = agent

    def run(self, prompt: str) -> ADKRunResponse:
        """Delegate to the agent's run method."""
        return self.agent.run(prompt)


# ---------------------------------------------------------------------------
# Try to import the real Google ADK SDK; fall back to stubs
# ---------------------------------------------------------------------------
# Declare explicit types so MyPy accepts the try/except assignment pattern
ADKAgentBase: type[_StubADKAgent] = _StubADKAgent
ADKRunnerBase: type[_StubADKRunner] = _StubADKRunner
ADK_AVAILABLE: bool = False

try:
    import google.adk  # type: ignore[import-untyped]  # noqa: F401

    ADK_AVAILABLE = True
    # When the real SDK is present, ADKAgentBase/ADKRunnerBase could be replaced
    # by the real classes. They share the same interface as the stubs so no change
    # is required here for the integration layer to function correctly.

except ImportError:
    pass  # stubs remain active


def adk_status_line() -> str:
    """Return a human-readable line describing ADK availability."""
    if ADK_AVAILABLE:
        return "google-adk: AVAILABLE (real SDK active)"
    return (
        "google-adk: NOT INSTALLED "
        "(using local stub -- install with: pip install google-adk)"
    )
