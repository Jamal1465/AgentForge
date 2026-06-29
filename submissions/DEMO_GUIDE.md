# Demo Guide — AgentForge

## Goal

Demonstrate that AgentForge can accept a natural language software request and execute a governed, observable, capability-first workflow.

## Prerequisites

- Python 3.11+
- A terminal
- No API key is required for the deterministic local demo

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run Tests

```bash
python -m pytest -q
```

## Health Check

```bash
agentforge health
```

Expected output:

```json
{"status": "ok"}
```

## Readiness Check

```bash
agentforge ready
```

Expected output:

```json
{"status": "ready"}
```

## Main Demo

```bash
agentforge create "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and technical documentation" --json
```

Without package installation:

```bash
PYTHONPATH=src python -m agentforge.interfaces.cli.main create "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and technical documentation" --json
```

## What to Point Out During the Demo

1. The request is natural language.
2. The platform creates a workflow.
3. Security checks run before plugin execution.
4. The selected plugin is resolved through capability routing.
5. Evaluation runs after execution.
6. Observability emits structured events.
7. The response is machine-readable JSON.

## Optional HTTP Demo

Start server:

```bash
agentforge serve --host 127.0.0.1 --port 8080
```

Call API:

```bash
curl -X POST http://localhost:8080/projects   -H "Content-Type: application/json"   -d '{"description":"Build a secure FastAPI task manager"}'
```

## Docker Demo

```bash
docker build -t agentforge:local .
docker run --rm -p 8080:8080 agentforge:local
```

## Demo Evidence

A recorded sample output is stored in:

```text
examples/capstone_demo_project/demo_run.json
```
