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

## 8. Recommended Antigravity Build Order

Give Antigravity the following order:

1. Open `AgentForge-Complete-Milestone-12`.
2. Read the Builder Kit first:
   - `00_READ_FIRST.md`
   - `AI_CONTEXT.md`
   - `BUILD_RULES.md`
   - `CODING_STANDARDS.md`
   - `GETTING_STARTED.md`
   - `agent_builder_playbook.md`
3. Read architecture documents:
   - `ARCHITECTURE/05_System_Architecture.md`
   - `ARCHITECTURE/06_Agent_Architecture.md`
   - `ARCHITECTURE/07_Workflow_Architecture.md`
   - `ARCHITECTURE/08_Memory_Architecture.md`
   - `ARCHITECTURE/09_MCP_Architecture.md`
   - `ARCHITECTURE/10_Security_Architecture.md`
   - `ARCHITECTURE/11_Evaluation_Architecture.md`
4. Read the implementation milestone files.
5. Open `agentforge-source-scaffold` as the implementation workspace.
6. Run the baseline test suite before making any change.
7. Preserve the capability-first plugin architecture.
8. Do not hardcode Backend Agent, Frontend Agent, Database Agent, or DevOps Agent into the core.
9. Add new engineering skills only as registered plugin capabilities.
10. After every change, run tests and quality checks.
11. Only push to GitHub after all checks pass.

## 9. Antigravity Prompt

```text
You are working inside the AgentForge repository.

Your job is to build and validate AgentForge as a capability-first, plugin-based AI Software Engineering Platform.

Before editing code, read these files in order:

1. 00_READ_FIRST.md
2. AI_CONTEXT.md
3. BUILD_RULES.md
4. CODING_STANDARDS.md
5. GETTING_STARTED.md
6. agent_builder_playbook.md
7. ARCHITECTURE/05_System_Architecture.md
8. ARCHITECTURE/06_Agent_Architecture.md
9. ARCHITECTURE/07_Workflow_Architecture.md
10. ARCHITECTURE/08_Memory_Architecture.md
11. ARCHITECTURE/09_MCP_Architecture.md
12. ARCHITECTURE/10_Security_Architecture.md
13. ARCHITECTURE/11_Evaluation_Architecture.md
14. IMPLEMENTATION/README.md
15. All milestone files inside IMPLEMENTATION/

Important architecture rule:
AgentForge must remain capability-first and plugin-first.
Do not hardcode agents such as BackendAgent, FrontendAgent, DatabaseAgent, DevOpsAgent, or DocumentationAgent into the orchestration core.
The Planner requests capabilities.
The Workflow Engine routes tasks by capability.
The Agent Registry selects registered plugins.
Plugins advertise capabilities such as api-development, ui-development, data-modeling, infrastructure, security-analysis, quality-assurance, and technical-documentation.

Implementation rules:
- Preserve Clean Architecture boundaries.
- Keep domain models free of infrastructure dependencies.
- Keep orchestration independent of concrete plugin implementations.
- Use typed Python.
- Do not introduce placeholder implementations.
- Do not remove tests.
- Do not skip failing tests.
- Do not push secrets.

First task:
Run the baseline validation:

python -m pytest -q
PYTHONPATH=src python -m compileall -q src tests
ruff check .
mypy src
PYTHONPATH=src python scripts/smoke_test.py

If any command fails, fix the failure before adding new features.

Second task:
Review the current source against the architecture and create a short gap analysis.

Third task:
Implement improvements one milestone at a time, starting only after baseline tests pass.

Fourth task:
After each implementation step, run the full validation suite again.

Final task:
Prepare the repository for GitHub by ensuring README, docs, tests, Docker files, CI workflow, and submission assets are complete and clean.
```

## 10. GitHub Push Commands

### First-time GitHub push

```bash
git init
git add .
git commit -m "Initial AgentForge capability-first platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agentforge.git
git push -u origin main
```

### If remote already exists

```bash
git remote -v
git remote set-url origin https://github.com/YOUR_USERNAME/agentforge.git
git add .
git commit -m "Complete AgentForge milestone 12 package"
git push origin main
```

### Before every push

```bash
python -m pytest -q
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python scripts/smoke_test.py
git status
```

## 11. Final Verification Completed Here

The generated package was checked with:

```bash
python -m pytest -q
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m agentforge.interfaces.cli.main health
PYTHONPATH=src python -m agentforge.interfaces.cli.main ready
PYTHONPATH=src python -m agentforge.interfaces.cli.main create "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and documentation" --json
PYTHONPATH=src python scripts/smoke_test.py
unzip -t AgentForge-Complete-Milestone-12.zip
unzip -t AgentForge-Source-Milestone-12.zip
unzip -t AgentForge-Submission-Package.zip
```

Result:

```text
98 tests passed.
Python compilation passed.
CLI health passed.
CLI readiness passed.
CLI workflow creation passed.
Smoke test passed.
ZIP integrity checks passed.
```
