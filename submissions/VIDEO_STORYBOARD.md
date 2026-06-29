# Demo Video Storyboard

## Target Length

2–3 minutes.

## Scene 1 — Introduction

Say:

> AgentForge is a capability-first AI Software Engineering Operating System. It is not a fixed set of hardcoded agents. It routes software engineering tasks to plugins based on declared capabilities.

Show:

- repository root,
- README,
- submissions folder.

## Scene 2 — Architecture

Show the architecture summary.

Say:

> The Planner requests capabilities. The Workflow Engine manages execution. The Agent Registry selects registered plugins. Security, evaluation, and observability run around every important execution step.

## Scene 3 — Tests

Run:

```bash
python -m pytest -q
```

Say:

> The project includes automated tests across workflow, memory, tools, security, evaluation, observability, CLI, and API boundaries.

## Scene 4 — Health and Readiness

Run:

```bash
agentforge health
agentforge ready
```

## Scene 5 — Main Demo

Run:

```bash
agentforge create "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and technical documentation" --json
```

Point out:

- workflow id,
- security event,
- evaluation event,
- workflow completion.

## Scene 6 — Closing

Say:

> The core value of AgentForge is extensibility. New engineering plugins can be added without rewriting the planner or workflow engine.
