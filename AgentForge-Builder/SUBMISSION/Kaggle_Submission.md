# Kaggle Capstone Submission — AgentForge

## Title

AgentForge — A Capability-First AI Software Engineering Operating System

## Short Description

AgentForge is a plugin-first multi-agent platform for AI-assisted software engineering. It turns a natural language software request into a governed workflow by routing tasks through capabilities, registered plugins, shared memory, secure tools, evaluation gates, and telemetry.

## Long Description

AgentForge was built for the Kaggle × Google AI Agents Intensive Vibe Coding course as a production-oriented capstone project. Rather than implementing a fixed hardcoded chain of agents, AgentForge provides an extensible runtime for agentic software engineering.

The platform follows this core architecture:

```text
User Request
   ↓
Project Intake / CLI / API
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
   ↓
Exportable Results
```

The Planner never assumes that a specific agent exists. It requests a capability. The registry decides which plugin can execute that capability.

## Why This Matters

A fixed multi-agent demo is easy to build but difficult to extend. AgentForge instead models a real platform boundary:

- The core owns orchestration.
- Plugins own specialized execution.
- Tools are invoked through safe adapters.
- Security policies apply to capabilities and tool risk.
- Evaluation checks outputs before they are accepted.
- Observability records how work moved through the system.

## Key Features

- capability-based task routing,
- plugin registry and plugin contract,
- workflow graph execution,
- persistent workflow state abstraction,
- shared memory service,
- MCP-ready tool adapter boundary,
- safe and secure tool execution,
- prompt-injection and secret-redaction checks,
- deterministic evaluation service and quality gates,
- structured telemetry, metrics, and traces,
- CLI/API interface layer,
- Docker and deployment assets,
- submission and demo package.

## Demo Command

```bash
PYTHONPATH=src python -m agentforge.interfaces.cli.main create   "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and technical documentation"   --json
```

## Expected Demo Outcome

The demo returns a completed workflow with:

- `workflow.started`,
- `security.allow`,
- plugin execution result,
- `evaluation.passed`,
- `workflow.completed`.

## Architecture Claim

AgentForge should be evaluated as a platform foundation for agentic software engineering, not as a single-purpose code generator.

## Current Limitations

The current submission includes deterministic local plugins and adapter boundaries. Live Gemini/ADK/MCP provider calls are intentionally isolated behind interfaces so the platform remains testable and does not require external credentials for review.

## Future Work

- Add live Google ADK agent adapters.
- Add Gemini-backed planning plugins.
- Add real MCP filesystem, Git, search, and Python execution adapters.
- Add plugin packaging and version compatibility checks.
- Add cloud execution workers.
- Add visual workflow viewer.
- Add marketplace-ready plugin metadata.
