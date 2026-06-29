# Milestone 11 — Interfaces and Deployment

Project: AgentForge  
Version: 1.0.0  
Status: Completed  
Architecture Mode: Capability-first plugin platform

## 1. Objective

Milestone 11 exposes AgentForge through local interfaces and deployment assets while preserving the plugin-first, capability-based architecture.

The milestone does not introduce hardcoded agent roles. External users interact with the platform through a composition root, CLI commands, framework-independent API handlers, a dependency-light HTTP server, and container assets.

## 2. Core Principle

AgentForge interfaces must not know about concrete implementation agents such as Backend Agent, Frontend Agent, Database Agent, or DevOps Agent.

Interfaces submit project requests to the platform. The platform creates workflow tasks requiring capabilities. The registry and router select plugins that provide those capabilities.

```text
CLI / API / Docker
        │
        ▼
AgentForgePlatform
        │
        ▼
Workflow Engine
        │
        ▼
Capability Router
        │
        ▼
Agent Registry
        │
        ▼
Registered Plugins
```

## 3. Deliverables

```text
src/agentforge/application/platform.py
src/agentforge/infrastructure/config.py
src/agentforge/infrastructure/deployment/health.py
src/agentforge/interfaces/api/schemas.py
src/agentforge/interfaces/api/handlers.py
src/agentforge/interfaces/api/app.py
src/agentforge/interfaces/api/stdlib_server.py
src/agentforge/interfaces/cli/main.py
Dockerfile
docker-compose.yml
.dockerignore
.env.example
.github/workflows/ci.yml
scripts/smoke_test.py
deployment/cloud-run.md
docs/MILESTONE_11_INTERFACES_DEPLOYMENT_REPORT.md
```

## 4. Functional Scope

### 4.1 Platform Composition Root

The `AgentForgePlatform` object wires:

- settings,
- agent registry,
- capability router,
- workflow store,
- workflow runner,
- memory service,
- security service,
- evaluation service,
- observability service.

All interfaces depend on this object instead of rebuilding service wiring.

### 4.2 CLI

Commands:

```bash
agentforge health
agentforge ready
agentforge create "Build a FastAPI task manager" --json
agentforge serve --host 127.0.0.1 --port 8080
```

### 4.3 HTTP API

Framework-independent handlers support:

```text
GET  /health
GET  /ready
POST /projects
POST /workflows/approval
```

### 4.4 Optional FastAPI Adapter

`agentforge.interfaces.api.app:create_app` creates a FastAPI application only when optional API dependencies are installed.

The core package does not require FastAPI.

### 4.5 Stdlib HTTP Server

`agentforge.interfaces.api.stdlib_server` provides a dependency-light JSON HTTP server for local smoke testing and container execution.

### 4.6 Deployment Assets

Milestone 11 adds:

- Dockerfile,
- Docker Compose,
- Docker health check,
- environment example,
- CI workflow,
- Cloud Run deployment notes.

## 5. Configuration

Configuration is environment-driven:

```text
AGENTFORGE_ENV
AGENTFORGE_HOST
AGENTFORGE_PORT
AGENTFORGE_LOG_LEVEL
AGENTFORGE_ENABLE_DOCS
AGENTFORGE_DEBUG_ERRORS
AGENTFORGE_APP_NAME
```

## 6. Acceptance Criteria

- The CLI uses `AgentForgePlatform`.
- API handlers are framework-independent.
- Health and readiness endpoints are implemented.
- The stdlib server can serve JSON endpoints.
- Dockerfile and Docker Compose are present.
- CI workflow is present.
- Tests validate configuration, platform, handlers, and CLI.
- Core routing remains capability-based.

## 7. Validation

```bash
python -m pytest -q
# 95 passed

PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m agentforge.interfaces.cli.main health
PYTHONPATH=src python -m agentforge.interfaces.cli.main ready
PYTHONPATH=src python -m agentforge.interfaces.cli.main create "Build a FastAPI task manager" --json
```

## 8. Next Milestone

Milestone 12 — Submission Package.

Milestone 12 will produce the final capstone assets, README, demo guide, presentation outline, architecture summary, submission checklist, and final ZIP packaging.
