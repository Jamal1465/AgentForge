# AgentForge × Google ADK Integration

## Overview

This document describes how AgentForge integrates with the **Google Agent Development
Kit (ADK)** to demonstrate a production-ready AI agent orchestration pattern for the
Kaggle × Google AI Agents Hackathon capstone.

---

## Why Google ADK?

The Google Agent Development Kit provides a standardized framework for building,
composing, and deploying AI agents.  It defines:

- An **`Agent`** base class with a `.run(prompt)` interface
- A **`Runner`** that manages agent execution lifecycle
- Hooks for multi-agent orchestration and tool use

AgentForge uses ADK to demonstrate how an enterprise AI platform can expose its
**capability-routed agents** through a standard agent interface without sacrificing
the plugin-first architecture.

---

## Architecture: How AgentForge Maps Capabilities to ADK Agents

AgentForge's capability-first design means that **no agent class name is ever
hardcoded**.  Instead, the system routes work by *capability tags*.

```
agentforge adk-demo "Build a secure FastAPI task manager API"
       │
       ▼
 ADKDemoWorkflow (src/agentforge/adk/adk_demo_workflow.py)
       │  iterates over capability tags only:
       │  ["requirements-analysis", "architecture-documentation", "risk-analysis"]
       │
       ▼
 ADKCapabilityAgent (src/agentforge/adk/adk_capability_agent.py)
       │  wraps any AgentForge plugin as an ADK Agent
       │  delegates to CapabilityRouter — never to a hardcoded class
       │
       ▼
 CapabilityRouter → resolves the registered AgentPlugin at runtime
       │
       ▼
 AgentPlugin.execute(task) → returns AgentResult
       │
       ▼
 ADKCapabilityResult (unified response with ADK lifecycle events)
```

### ADK Adapter Pattern

The `ADKAdapter` (`src/agentforge/adk/adk_adapter.py`) tries to import the real
`google.adk` package.  If not installed, it falls back to a local stub that mirrors
the same interface.  This means:

- Tests pass without installing `google-adk`
- The real SDK can be dropped in without changing any other code
- The boundary is enforced in **one file only**

```python
# src/agentforge/adk/adk_adapter.py
try:
    from google.adk.agents import Agent as ADKAgentBase  # real SDK
    ADK_AVAILABLE = True
except ImportError:
    class ADKAgentBase: ...          # local stub
    ADK_AVAILABLE = False
```

---

## Demonstrated Capabilities

| Capability Tag              | Routed To                    | ADK Agent Name                   |
|-----------------------------|------------------------------|----------------------------------|
| `requirements-analysis`     | `RequirementsAgentPlugin`    | `adk-requirements-analysis`      |
| `architecture-documentation`| `ArchitectureAgentPlugin`    | `adk-architecture-documentation` |
| `risk-analysis`             | `OperationsAgentPlugin`      | `adk-risk-analysis`              |

The ADK agent names are derived from capability tags — never from class names like
`BackendAgent` or `DatabaseAgent`.  This preserves the capability-first architecture
required by the course.

---

## Course Concept Alignment

This integration demonstrates the following concepts from the Google AI Agents course:

| Course Concept           | AgentForge Implementation                                      |
|--------------------------|----------------------------------------------------------------|
| Agent lifecycle          | `ADKCapabilityAgent.run_capability()` emits start/complete events |
| Multi-agent orchestration| `ADKDemoWorkflow` sequences 3 ADK agents by capability tag     |
| Tool use                 | `AgentPlugin.execute()` is the tool called by each ADK agent   |
| Agent composition        | Adapter pattern wraps any plugin as an ADK `Agent` subclass    |
| Capability routing       | `CapabilityRouter` resolves plugins dynamically at runtime     |

---

## Installation

### Without `google-adk` (stub mode — all features work)

```bash
# No extra install needed — the stub runs automatically
pip install -e ".[dev]"
```

### With `google-adk` (real SDK mode)

```bash
pip install -e ".[dev,adk]"
# or directly:
pip install google-adk
```

When `google-adk` is installed, `ADK_AVAILABLE` becomes `True` and the real
`google.adk.agents.Agent` class is used as the base for all ADK agents.

---

## Commands

### Run the ADK demo (primary demo command)

```bash
# With installed entry point:
agentforge adk-demo "Build a secure FastAPI task manager API"

# Or via Python module:
python -m agentforge adk-demo "Build a secure FastAPI task manager API"

# With PYTHONPATH set (development):
PYTHONPATH=src python -m agentforge adk-demo "Build a secure FastAPI task manager API"
```

### Check ADK availability

```python
from agentforge.adk import ADK_AVAILABLE, adk_status_line
print(adk_status_line())
# google-adk: NOT INSTALLED (using local stub — install with: pip install google-adk)
# or:
# google-adk: AVAILABLE (real SDK active)
```

### Run programmatically

```python
from agentforge.adk import ADKDemoWorkflow

result = ADKDemoWorkflow().run("Build a secure FastAPI task manager API")
print("\n".join(result.summary_lines()))

# Inspect events
for event in result.all_events:
    print(event["event_type"])
```

### Expected Output

```
╔══════════════════════════════════════════════════════╗
║          AgentForge  ×  Google ADK  Demo             ║
╚══════════════════════════════════════════════════════╝

  Project : Build a secure FastAPI task manager API
  google-adk: NOT INSTALLED (using local stub)

  ✓ [requirements-analysis]  confidence=0.90
    Generated requirements artifact: 02_Functional_Requirements.md.
    ADK response: [stub][adk-requirements-analysis] processed: ...

  ✓ [architecture-documentation]  confidence=0.90
    Generated architecture artifact: 05_System_Architecture.md.
    ADK response: [stub][adk-architecture-documentation] processed: ...

  ✓ [risk-analysis]  confidence=0.90
    Generated operations artifact: 10_Risk_Assessment.md.
    ADK response: [stub][adk-risk-analysis] processed: ...

  ── Events ──────────────────────────────────────────

  [adk.workflow.started]  capabilities=...
  [adk.agent.started]  capability=requirements-analysis
  [adk.agent.plugin_resolved]  capability=requirements-analysis  plugin_id=builtin.requirements
  [adk.agent.completed]  capability=requirements-analysis  status=success
  ...
  [adk.workflow.completed]  total_capabilities=3

  Demo complete. 3 capabilities executed via ADK adapter.
```

---

## Running Tests

```bash
python -m pytest tests/test_adk_integration.py -v
```

All 15 ADK tests pass whether or not `google-adk` is installed.

---

## Limitations

| Limitation | Reason | Mitigation |
|---|---|---|
| No real LLM calls | `google-adk` is not publicly available on PyPI as a standard package | Stub produces deterministic outputs; swap in real SDK when available |
| No streaming | ADK streaming API varies across versions | `run()` returns complete `ADKRunResponse` objects |
| No multi-turn | Demo is single-turn per capability | Extend `ADKDemoWorkflow` with session management for multi-turn |
| Gemini model not called | Requires Google Cloud credentials | Set `GOOGLE_API_KEY` env var when real SDK is installed |

---

## File Structure

```
src/agentforge/adk/
├── __init__.py                # Public package API
├── adk_adapter.py             # Import boundary (real SDK or stub)
├── adk_capability_agent.py    # ADK agent wrapping capability router
└── adk_demo_workflow.py       # Demo orchestration of 3 capabilities

tests/
└── test_adk_integration.py    # 15 tests covering all ADK integration aspects

docs/
└── ADK_INTEGRATION.md         # This document
```
