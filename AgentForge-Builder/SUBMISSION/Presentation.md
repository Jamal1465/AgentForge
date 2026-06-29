# Presentation Outline — AgentForge

## Slide 1 — Title

AgentForge: A Capability-First AI Software Engineering Operating System

## Slide 2 — Problem

AI coding assistants are useful, but full software engineering requires planning, architecture, security, testing, documentation, deployment, and evaluation.

## Slide 3 — Core Idea

Do not hardcode a fixed list of agents. Build a platform that routes tasks by capability.

## Slide 4 — Old vs New Architecture

Old:

```text
Planner → Backend Agent → Frontend Agent → Database Agent
```

New:

```text
Planner → Workflow Engine → Capability Matcher → Agent Registry → Plugins
```

## Slide 5 — Platform Components

- workflow engine,
- plugin registry,
- capability router,
- memory,
- tools/MCP gateway,
- security,
- evaluation,
- observability,
- CLI/API/deployment.

## Slide 6 — Demo Flow

Show the CLI command and JSON output.

## Slide 7 — Security and Governance

Security policy is based on capabilities, plugin trust, prompt risk, and tool risk.

## Slide 8 — Evaluation

Outputs are checked using rubrics and quality gates before acceptance.

## Slide 9 — Observability

Telemetry proves what happened during the workflow.

## Slide 10 — Results

- tested source scaffold,
- deterministic local demo,
- Docker-ready deployment,
- submission package,
- extensible plugin architecture.

## Slide 11 — Limitations

- current plugins are deterministic local examples,
- live Gemini/ADK/MCP providers are adapter-ready but not required for local review,
- visual workflow UI is future work.

## Slide 12 — Future Work

- real ADK agent adapters,
- plugin marketplace,
- multi-LLM routing,
- distributed execution,
- visual workflow composer.
