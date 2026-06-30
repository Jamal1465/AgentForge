# AgentForge Build, Run, Test, and GitHub Guide

## 1. Correct Package to Use

Use the final source package for development:

```text
AgentForge-Source-Milestone-12.zip
```

Use the complete package if you also want the full Builder Kit documentation:

```text
AgentForge-Complete-Milestone-12.zip
```

## 2. Project Architecture

AgentForge is a capability-first, plugin-based AI Software Engineering Platform.

The core does not depend on hardcoded agent roles such as Backend Agent, Frontend Agent, or Database Agent.

The execution model is:

```text
User Request
    ↓
CLI / API Interface
    ↓
AgentForgePlatform Composition Root
    ↓
Workflow Engine
    ↓
Capability Router
    ↓
Agent Registry
    ↓
Registered Plugin Agents
    ↓
Security Layer
    ↓
Evaluation Framework
    ↓
Observability + Memory
    ↓
Submission / Export Artifacts
```

## 3. Source File Structure

```text
agentforge-source-scaffold/
├── .github/
│   └── workflows/
│       └── ci.yml
├── deployment/
│   └── cloud-run.md
├── docs/
│   ├── MILESTONE_05_WORKFLOW_ENGINE_REPORT.md
│   ├── MILESTONE_06_MEMORY_SYSTEM_REPORT.md
│   ├── MILESTONE_07_MCP_TOOL_INTEGRATION_REPORT.md
│   ├── MILESTONE_08_SECURITY_LAYER_REPORT.md
│   ├── MILESTONE_09_EVALUATION_FRAMEWORK_REPORT.md
│   ├── MILESTONE_10_OBSERVABILITY_TELEMETRY_REPORT.md
│   ├── MILESTONE_11_INTERFACES_DEPLOYMENT_REPORT.md
│   ├── MILESTONE_12_SUBMISSION_PACKAGE_REPORT.md
│   └── README.md
├── examples/
│   └── capstone_demo_project/
│       ├── demo_run.json
│       ├── expected_workflow.md
│       └── project_request.md
├── scripts/
│   └── smoke_test.py
├── src/
│   └── agentforge/
│       ├── agents/
│       │   └── planner/
│       │       └── plugin.py
│       ├── application/
│       │   ├── evaluation/
│       │   ├── memory/
│       │   ├── observability/
│       │   ├── security/
│       │   ├── tools/
│       │   ├── workflows/
│       │   └── platform.py
│       ├── domain/
│       │   ├── entities.py
│       │   ├── evaluation.py
│       │   ├── memory.py
│       │   ├── observability.py
│       │   ├── security.py
│       │   ├── tools.py
│       │   ├── value_objects.py
│       │   └── workflow.py
│       ├── domain_analysis/
│       │   ├── domain_context.py
│       │   ├── domain_packs.py
│       │   ├── domain_analyzer.py
│       │   └── new_packs.py
│       ├── infrastructure/
│       │   ├── config.py
│       │   ├── deployment/
│       │   ├── persistence/
│       │   └── tools/
│       ├── interfaces/
│       │   ├── api/
│       │   └── cli/
│       └── runtime/
│           ├── plugins/
│           ├── registry/
│           ├── routing/
│           └── tools/
├── submissions/
│   ├── ARTIFACT_MANIFEST.md
│   ├── CAPSTONE_CHECKLIST.md
│   ├── DEMO_GUIDE.md
│   ├── EVALUATION_EVIDENCE.md
│   ├── FINAL_VALIDATION_REPORT.md
│   ├── JUDGE_WALKTHROUGH.md
│   ├── KAGGLE_SUBMISSION.md
│   ├── PRESENTATION_OUTLINE.md
│   ├── PROJECT_CARD.md
│   ├── README.md
│   ├── TECHNICAL_ARCHITECTURE_SUMMARY.md
│   └── VIDEO_STORYBOARD.md
├── tests/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── Makefile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## 4. Local Setup Commands

### Windows PowerShell

```powershell
cd path\to\agentforge-source-scaffold
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev,api]"
```

### Linux / macOS / Git Bash

```bash
cd path/to/agentforge-source-scaffold
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev,api]"
```

## 5. Run the Project

### Health check

```bash
agentforge health
```

Alternative without installing editable package:

```bash
PYTHONPATH=src python -m agentforge.interfaces.cli.main health
```

### Readiness check

```bash
agentforge ready
```

Alternative:

```bash
PYTHONPATH=src python -m agentforge.interfaces.cli.main ready
```

### Create a workflow from a project idea

```bash
agentforge create "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and documentation" --json
```

Alternative:

```bash
PYTHONPATH=src python -m agentforge.interfaces.cli.main create "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and documentation" --json
```

### Run smoke test

```bash
PYTHONPATH=src python scripts/smoke_test.py
```

## 6. Test and Quality Commands

```bash
python -m pytest -q
PYTHONPATH=src python -m compileall -q src tests
ruff check .
mypy src
```

Full check:

```bash
make check
```

If `ruff` or `mypy` are missing, install development dependencies:

```bash
pip install -e ".[dev,api]"
```

## 7. Docker Run

```bash
docker build -t agentforge:local .
docker run --rm -p 8080:8080 agentforge:local
```

Docker Compose:

```bash
docker compose up --build
```
