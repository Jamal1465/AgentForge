"""AgentForge ADK integration package.

Provides a Google ADK adapter layer that can operate with the real
``google-adk`` SDK when installed, or a local stub otherwise.

Public API::

    from agentforge.adk import ADK_AVAILABLE, adk_status_line
    from agentforge.adk import ADKCapabilityAgent, ADKDemoWorkflow

Example::

    from agentforge.adk import ADKDemoWorkflow
    result = ADKDemoWorkflow().run("Build a secure FastAPI task manager API")
    print("\\n".join(result.summary_lines()))
"""

from agentforge.adk.adk_adapter import (
    ADK_AVAILABLE,
    ADKRunResponse,
    adk_status_line,
)
from agentforge.adk.adk_adapter import (
    _StubADKAgent as ADKAgentBase,
)
from agentforge.adk.adk_capability_agent import ADKCapabilityAgent, ADKCapabilityResult
from agentforge.adk.adk_demo_workflow import ADKDemoResult, ADKDemoWorkflow

__all__ = [
    "ADK_AVAILABLE",
    "ADKAgentBase",
    "ADKCapabilityAgent",
    "ADKCapabilityResult",
    "ADKDemoResult",
    "ADKDemoWorkflow",
    "ADKRunResponse",
    "adk_status_line",
]
