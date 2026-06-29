# GETTING_STARTED.md

Project: AgentForge  
Purpose: Setup and first build guide

---

# 1. Overview

This guide explains how to prepare a local development environment for AgentForge and how to begin implementation safely.

AgentForge is built as a Python-based, Google ADK-aligned, plugin-first multi-agent software engineering platform.

---

# 2. Prerequisites

Install the following:

- Python 3.11+
- Git
- Docker Desktop or Docker Engine
- `uv` package manager
- Google AI Studio API key or compatible Gemini access
- VS Code, Antigravity IDE, or another AI-assisted editor

Recommended:

- Make
- Node.js only if frontend demo generation is added later
- GitHub CLI for repository operations

---

# 3. Environment Variables

Create `.env` from `.env.example`.

Required variables:

```env
GOOGLE_API_KEY=your_key_here
AGENTFORGE_ENV=local
AGENTFORGE_WORKSPACE=.agentforge
AGENTFORGE_LOG_LEVEL=INFO
AGENTFORGE_DEFAULT_MODEL=gemini-2.5-flash
AGENTFORGE_REQUIRE_APPROVAL_FOR_HIGH_RISK=true
```

Never commit `.env`.

---

# 4. Recommended Repository Setup

When the source scaffold is generated, the project root should look like this:

```text
agentforge/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── docs/
├── src/
├── tests/
├── examples/
├── scripts/
└── submissions/
```

---

# 5. Install Dependencies

Expected command after scaffold generation:

```bash
uv sync
```

If `uv` is not installed:

```bash
pip install uv
```

---

# 6. Run Quality Checks

Expected commands:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

A milestone is not complete until these checks pass or documented exceptions are approved.

---

# 7. First Development Flow

Do not start by building every agent.

Start with the smallest vertical slice:

1. Domain models for project, task, agent capability, workflow state.
2. Plugin contract.
3. Agent registry.
4. Capability router.
5. Simple planner stub that returns structured tasks.
6. Workflow runner that executes one task through one agent.
7. Evaluation report for the task.
8. CLI command to run the demo.

This proves the architecture before adding complexity.

---

# 8. Development Order

Recommended implementation order:

1. Milestone 1 — Project Foundation
2. Milestone 2 — Repository Scaffold
3. Milestone 3 — Core Domain Models
4. Milestone 4 — Plugin Registry
5. Milestone 5 — Workflow Engine
6. Milestone 6 — Memory System
7. Milestone 7 — Tool and MCP Gateway
8. Milestone 8 — Built-in Agents
9. Milestone 9 — Security Layer
10. Milestone 10 — Evaluation Framework
11. Milestone 11 — Interfaces and Deployment
12. Milestone 12 — Submission Package

---

# 9. Local Demo Target

The first complete demo should execute this flow:

```bash
agentforge create "Build a simple FastAPI task manager with SQLite"
agentforge plan --project task-manager
agentforge run --project task-manager
agentforge evaluate --project task-manager
agentforge export --project task-manager
```

Expected output:

- project specification,
- task plan,
- generated artifacts,
- evaluation report,
- security report,
- README,
- exportable project directory.

---

# 10. Troubleshooting

## Import Errors

Run:

```bash
uv sync
uv run python -m pip list
```

Check that `src/` package discovery is configured correctly in `pyproject.toml`.

## Missing API Key

Verify:

```bash
echo $GOOGLE_API_KEY
```

On Windows PowerShell:

```powershell
$env:GOOGLE_API_KEY
```

## Tests Failing

Do not add new features. Fix failing tests first.

## Architecture Confusion

Return to:

- `ARCHITECTURE/05_System_Architecture.md`
- `BUILD_RULES.md`
- current milestone file

---

# 11. Completion Signal

Environment setup is complete when:

- dependencies install,
- CLI imports,
- tests run,
- quality checks execute,
- a sample project plan can be generated.
