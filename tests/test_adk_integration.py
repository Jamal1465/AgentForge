"""Tests for the AgentForge Google ADK integration layer.

Covers:
- ADK adapter import boundary (real SDK or stub, never crashes)
- ADKCapabilityAgent wraps a plugin and routes by capability (not by class name)
- ADKDemoWorkflow runs end-to-end with all three capabilities
- CLI adk-demo command produces valid output
- Capability-first architecture is preserved (no hardcoded agent names in routing)
"""

from __future__ import annotations

import subprocess
import sys

import pytest

from agentforge.adk.adk_adapter import (
    ADK_AVAILABLE,
    ADKAgentBase,
    ADKRunResponse,
    adk_status_line,
)
from agentforge.adk.adk_capability_agent import ADKCapabilityAgent, ADKCapabilityResult
from agentforge.adk.adk_demo_workflow import _DEMO_CAPABILITIES, ADKDemoWorkflow
from agentforge.application.platform import AgentForgePlatform
from agentforge.infrastructure.config import AgentForgeSettings, RuntimeEnvironment
from agentforge.interfaces.cli.main import run_adk_demo

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def platform() -> AgentForgePlatform:
    settings = AgentForgeSettings(environment=RuntimeEnvironment.TEST)
    return AgentForgePlatform.create_default(settings=settings)


# ---------------------------------------------------------------------------
# ADK adapter boundary tests
# ---------------------------------------------------------------------------


def test_adk_available_is_bool() -> None:
    """ADK_AVAILABLE must be a bool regardless of whether SDK is installed."""
    assert isinstance(ADK_AVAILABLE, bool)


def test_adk_status_line_is_str() -> None:
    """adk_status_line() must return a non-empty string."""
    line = adk_status_line()
    assert isinstance(line, str)
    assert len(line) > 0


def test_adk_agent_base_instantiates() -> None:
    """ADKAgentBase (real or stub) must be instantiable with name only."""
    agent = ADKAgentBase(name="test-agent")
    assert agent.name == "test-agent"


def test_adk_agent_base_run_returns_response() -> None:
    """ADKAgentBase.run() must return an ADKRunResponse."""
    agent = ADKAgentBase(name="test-agent", description="unit test")
    response = agent.run("Hello, ADK!")
    assert isinstance(response, ADKRunResponse)
    assert response.agent_name == "test-agent"
    assert "Hello, ADK!" in response.prompt or len(response.text) > 0


def test_adk_run_response_str() -> None:
    """ADKRunResponse.__str__ must include agent name and a label."""
    resp = ADKRunResponse(
        agent_name="my-agent",
        prompt="test prompt",
        text="result text",
        is_stub=True,
    )
    out = str(resp)
    assert "my-agent" in out
    assert "stub" in out


# ---------------------------------------------------------------------------
# ADKCapabilityAgent tests — capability-first, not class-name-first
# ---------------------------------------------------------------------------


def test_adk_capability_agent_routes_requirements(platform: AgentForgePlatform) -> None:
    """ADKCapabilityAgent for requirements-analysis routes to the correct plugin."""
    agent = ADKCapabilityAgent(
        capability="requirements-analysis",
        registry=platform.registry,
    )
    result = agent.run_capability("Build a secure FastAPI task manager API")

    assert isinstance(result, ADKCapabilityResult)
    assert result.capability == "requirements-analysis"
    assert result.confidence > 0.0
    assert result.adk_available == ADK_AVAILABLE
    # Events must prove the ADK lifecycle
    event_types = [e.get("event_type") for e in result.events]
    assert "adk.agent.started" in event_types
    assert "adk.agent.completed" in event_types


def test_adk_capability_agent_routes_architecture(platform: AgentForgePlatform) -> None:
    """ADKCapabilityAgent for architecture-documentation routes to correct plugin."""
    agent = ADKCapabilityAgent(
        capability="architecture-documentation",
        registry=platform.registry,
    )
    result = agent.run_capability("Build a microservices platform")
    assert result.capability == "architecture-documentation"
    assert result.confidence > 0.0


def test_adk_capability_agent_routes_risk(platform: AgentForgePlatform) -> None:
    """ADKCapabilityAgent for risk-analysis routes to correct plugin."""
    agent = ADKCapabilityAgent(
        capability="risk-analysis",
        registry=platform.registry,
    )
    result = agent.run_capability("Build a payment processing system")
    assert result.capability == "risk-analysis"
    assert result.confidence > 0.0


def test_adk_capability_agent_no_hardcoded_class_names(
    platform: AgentForgePlatform,
) -> None:
    """ADKCapabilityAgent must use capability routing, not hardcoded class names.

    The agent's name is derived from the capability tag, not a class name.
    This verifies the capability-first architecture is preserved.
    """
    for cap in _DEMO_CAPABILITIES:
        agent = ADKCapabilityAgent(capability=cap, registry=platform.registry)
        # Agent name is capability-derived, not a class name like 'BackendAgent'
        assert cap in agent.name
        assert "BackendAgent" not in agent.name
        assert "FrontendAgent" not in agent.name
        assert "DatabaseAgent" not in agent.name


def test_adk_capability_agent_unknown_capability(platform: AgentForgePlatform) -> None:
    """ADKCapabilityAgent for an unregistered capability returns graceful failure."""
    agent = ADKCapabilityAgent(
        capability="nonexistent-capability-xyz",
        registry=platform.registry,
    )
    result = agent.run_capability("Some project")
    assert result.confidence == 0.0
    event_types = [e.get("event_type") for e in result.events]
    assert "adk.agent.no_plugin" in event_types


# ---------------------------------------------------------------------------
# ADKDemoWorkflow tests
# ---------------------------------------------------------------------------


def test_adk_demo_workflow_runs_all_capabilities(platform: AgentForgePlatform) -> None:
    """ADKDemoWorkflow must run all three demo capabilities successfully."""
    workflow = ADKDemoWorkflow(platform=platform)
    result = workflow.run("Build a secure FastAPI task manager API")

    assert len(result.capability_results) == len(_DEMO_CAPABILITIES)
    for cap_result in result.capability_results:
        assert cap_result.capability in _DEMO_CAPABILITIES
        assert cap_result.confidence > 0.0


def test_adk_demo_workflow_events_prove_integration(platform: AgentForgePlatform) -> None:
    """ADKDemoWorkflow events must include start/complete lifecycle markers."""
    workflow = ADKDemoWorkflow(platform=platform)
    result = workflow.run("Build a task management system")

    all_event_types = [e.get("event_type") for e in result.all_events]
    assert "adk.workflow.started" in all_event_types
    assert "adk.workflow.completed" in all_event_types
    assert "adk.agent.started" in all_event_types
    assert "adk.agent.completed" in all_event_types


def test_adk_demo_workflow_summary_lines(platform: AgentForgePlatform) -> None:
    """summary_lines() must produce non-empty list with key markers."""
    workflow = ADKDemoWorkflow(platform=platform)
    result = workflow.run("Build an e-commerce API")
    lines = result.summary_lines()

    full_output = "\n".join(lines)
    assert "AgentForge" in full_output
    assert "ADK" in full_output
    assert "requirements-analysis" in full_output
    assert "architecture-documentation" in full_output
    assert "risk-analysis" in full_output
    assert "Demo complete" in full_output


def test_adk_demo_workflow_adk_available_flag(platform: AgentForgePlatform) -> None:
    """result.adk_available must match the adapter's ADK_AVAILABLE flag."""
    workflow = ADKDemoWorkflow(platform=platform)
    result = workflow.run("Test project")
    assert result.adk_available == ADK_AVAILABLE


# ---------------------------------------------------------------------------
# CLI integration test
# ---------------------------------------------------------------------------


def test_run_adk_demo_cli_function() -> None:
    """run_adk_demo() must return a non-empty string with expected markers."""
    output = run_adk_demo("Build a secure FastAPI task manager API")
    assert isinstance(output, str)
    assert "AgentForge" in output
    assert "ADK" in output
    assert "requirements-analysis" in output
    assert "Demo complete" in output


def test_adk_demo_cli_subprocess() -> None:
    """agentforge adk-demo must work as a CLI subprocess."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "agentforge",
            "adk-demo",
            "Build a secure FastAPI task manager API",
        ],
        capture_output=True,
        text=True,
        timeout=60,
        env={
            **__import__("os").environ,
            "PYTHONPATH": "src",
            "PYTHONUTF8": "1",
        },
        cwd=(
            r"c:\Users\abbas\Desktop\Multi Agent Project"
            r"\AgentForge-Final-Verified\agentforge-source-scaffold"
        ),
    )
    assert result.returncode == 0, f"CLI failed:\n{result.stderr}"
    assert "Demo complete" in result.stdout


# ---------------------------------------------------------------------------
# Architecture preservation tests
# ---------------------------------------------------------------------------


def test_demo_capabilities_are_strings_not_class_names() -> None:
    """_DEMO_CAPABILITIES must contain capability tag strings, never class names."""
    forbidden = {"BackendAgent", "FrontendAgent", "DatabaseAgent", "WorkerAgent"}
    for cap in _DEMO_CAPABILITIES:
        assert cap not in forbidden
        # capability tags are lowercase-kebab-case
        assert cap == cap.lower()
        assert "_" not in cap  # no underscores — use hyphens


def test_adk_package_public_api() -> None:
    """The adk package must export the documented public symbols."""
    import agentforge.adk as adk_pkg

    required = {
        "ADK_AVAILABLE",
        "ADKAgentBase",
        "ADKCapabilityAgent",
        "ADKCapabilityResult",
        "ADKDemoResult",
        "ADKDemoWorkflow",
        "ADKRunResponse",
        "adk_status_line",
    }
    for symbol in required:
        assert hasattr(adk_pkg, symbol), f"Missing public symbol: {symbol}"
