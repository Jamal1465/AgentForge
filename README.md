# AgentForge: Capability-First AI Software Engineering Platform

AgentForge is a modular, plugin-based AI Software Engineering Platform designed using Clean and Hexagonal Architecture principles. 

Unlike conventional platforms that hardcode developer persona agents (e.g., `BackendAgent`, `FrontendAgent`, `DatabaseAgent`), AgentForge is **capability-first**. Orchestration components only deal with abstract `Capability` demands. Agent registries dynamically match capabilities to registered plugins at runtime, enabling secure, observable, and policy-governed execution.

---

## 📖 Key Architectural Concepts

- **Capability-First Routing**: Agent plugins register by declaring capability tags. The platform routes tasks dynamically without coupling to concrete agent class types.
- **Clean/Hexagonal Layering**: Domain core contains pure dataclasses and business logic. Application service interfaces manage orchestrations. Infrastructure implements adapters (persistence, memory, tools). Interfaces serve CLI and HTTP API requests.
- **Governed Tool execution**: A secure tool wrapper intercepts execution, evaluates boundary policies, redacts credentials/secrets, and audits actions.
- **Multi-Scope Memory**: Scopes data across Request, Session, Project, and Knowledge boundaries.
- **Closed-Loop Evaluation**: Validates outputs against quality criteria rubrics and enforces quality gates.

---

## 🛠️ Prerequisites

- **Python**: version 3.11+
- **Node.js**: version 18+ (for UI frontend)
- **Docker & Docker Compose**: optional (for containerized deployment)

---

## 🚀 Quick Start Guide

### 1. Installation

Clone the repository and configure the virtual environment:

```bash
# Setup Python Virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package with all development and API dependencies
pip install -e ".[dev,api]"
```

For the frontend dashboard:

```bash
cd frontend
npm install
cd ..
```

---

## 💻 Local Execution Commands

### A. Command Line Interface (CLI)

Use the CLI to run health checks, readiness reports, or synthesize a project blueprint:

```bash
# Verify health and readiness
agentforge health
agentforge ready

# Synthesize a project blueprint (returns JSON)
agentforge create "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and documentation" --json
```

Or run without global CLI installation:

```bash
PYTHONPATH=src python -m agentforge.interfaces.cli.main health
PYTHONPATH=src python -m agentforge.interfaces.cli.main ready
PYTHONPATH=src python -m agentforge.interfaces.cli.main create "Build a secure FastAPI task manager" --json
```

### B. Backend API Servers

#### 1. FastAPI ASGI Server (Recommended)
Exposes complete API endpoints and serves interactive documentation at `/docs`:

```bash
# Start FastAPI server on localhost:8080 (auto-detects and runs FastAPI)
agentforge serve --host 127.0.0.1 --port 8080

# Or explicitly start FastAPI server
agentforge serve-api --host 127.0.0.1 --port 8080
```

#### 2. Standard Library JSON Server (Fallback)
If `fastapi` and `uvicorn` are not installed, the platform falls back to a minimal standard library HTTP server:

```bash
# Runs the lightweight fallback server on localhost:8080
agentforge serve --host 127.0.0.1 --port 8080
```

### C. Frontend Dashboard

Run the Vite-based development server to interact with the visual dashboard:

```bash
cd frontend
# Launch development server on http://localhost:5173
npm run dev
```

---

## 🐳 Docker Deployment

To build and package the application as a container:

### 1. Run single container

```bash
# Build the Docker image
docker build -t agentforge:local .

# Run the container (binds API to port 8080)
docker run --rm -p 8080:8080 agentforge:local
```

### 2. Run with Docker Compose (Backend + Frontend)

Start the full platform ecosystem using Docker Compose:

```bash
# Build and spin up containers
docker compose up --build
```

---

## 🧪 Verification & Development Commands

Run the full validation suite to verify code formatting, type safety, and unit test behaviors:

```bash
# Run pytest unit tests
python -m pytest -q

# Run Ruff linter and style check
python -m ruff check .

# Run MyPy strict type checker
python -m mypy src

# Compile source to verify syntax
PYTHONPATH=src python -m compileall -q src tests

# Execute runtime smoke test
PYTHONPATH=src python scripts/smoke_test.py
```

For the frontend workspace:

```bash
cd frontend
# Check for lint errors
npm run lint

# Compile and build production assets
npm run build
```

---

## 📂 API Endpoint Documentation

When serving via FastAPI (`agentforge serve-api`), view the Swagger UI at `http://localhost:8080/docs`.

### Primary Endpoints
* **`GET /health`**: Platform health check status.
* **`GET /ready`**: Capability readiness check.
* **`POST /api/workflows/create`**: Trigger a project synthesis workflow.
* **`GET /api/workflows/{workflow_id}`**: Retrieve full details of a specific workflow run.
* **`GET /api/generated-projects/{workflow_id}/files`**: List files produced by the workflow.
* **`GET /api/generated-projects/{workflow_id}/files/{filename}`**: Read specific file contents.
* **`GET /api/plugins`**: List all registered plugins and their capabilities.
* **`GET /api/capabilities`**: Retrieve all matched capability tags in the system.
* **`GET /api/events`**: Stream observability telemetry events.
