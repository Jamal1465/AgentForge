# AgentForge

AgentForge is a capability-first AI Software Engineering Operating System.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q
agentforge create "Build a secure FastAPI task manager" --json
```

## Architecture

```text
User Request
   ↓
Planner
   ↓
Workflow Engine
   ↓
Capability Matcher
   ↓
Agent Registry
   ↓
Registered Plugins
   ↓
Security + Evaluation + Observability
```

## Core Principle

The orchestration core does not depend on concrete agent names. New engineering abilities are added as plugins that advertise capabilities.
