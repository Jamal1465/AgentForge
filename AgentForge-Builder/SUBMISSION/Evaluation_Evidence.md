# Evaluation Evidence

## Validation Commands

```bash
python -m pytest -q
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m agentforge.interfaces.cli.main health
PYTHONPATH=src python -m agentforge.interfaces.cli.main ready
PYTHONPATH=src python -m agentforge.interfaces.cli.main create "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and technical documentation" --json
```

## What the Tests Cover

| Area | Evidence |
|---|---|
| Domain models | value objects, entities, workflow states |
| Plugin runtime | registry, capability router, planner plugin |
| Workflow engine | execution, dependencies, retry, approval pause |
| Memory system | scoped records, querying, context rendering |
| Tool gateway | registry, safe executor, MCP adapter boundary |
| Security | prompt injection, secret redaction, capability policy |
| Evaluation | rubrics, scores, reports, quality gates |
| Observability | events, metrics, traces, observable wrappers |
| Interfaces | CLI, API handlers, platform health/readiness |
| Deployment | Dockerfile, Compose, CI, smoke test script |

## Current Test Count

Final Milestone 12 validation reports 98 passing tests, including submission-package checks.

## Demo Evidence

The demo output file proves end-to-end platform orchestration for the deterministic local vertical slice:

```text
examples/capstone_demo_project/demo_run.json
```

## Evaluation Philosophy

AgentForge does not claim that every generated artifact is correct without review. Instead, it implements a safer architecture:

1. route by capability,
2. apply security policy,
3. execute compatible plugin,
4. evaluate output,
5. record telemetry,
6. export evidence.
