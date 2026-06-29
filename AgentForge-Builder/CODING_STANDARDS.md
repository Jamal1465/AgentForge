# CODING_STANDARDS.md

Project: AgentForge  
Status: Required engineering standard

---

# 1. Purpose

This document defines the coding standard for AgentForge. The goal is to keep the repository readable, testable, extensible, and safe for AI-assisted development.

---

# 2. Python Version

Use Python 3.11 or newer.

Reason:

- modern typing support,
- improved performance,
- compatibility with current AI/agent tooling,
- stable ecosystem support.

---

# 3. Formatting and Linting

Use:

- Ruff for linting,
- Ruff formatter or Black-compatible formatting,
- MyPy or Pyright for static typing,
- Pytest for tests.

Mandatory checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

---

# 4. Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Packages | snake_case | `workflow_engine` |
| Classes | PascalCase | `WorkflowRunner` |
| Functions | snake_case | `load_plugins` |
| Variables | snake_case | `task_id` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_TIMEOUT_SECONDS` |
| Protocols | PascalCase + Port/Protocol | `MemoryStorePort` |
| Exceptions | PascalCase + Error | `WorkflowStateError` |

---

# 5. Type Standards

All public functions must have type annotations.

Prefer:

```python
from __future__ import annotations
```

Use typed models for boundary data.

Allowed:

- dataclasses for domain entities,
- Pydantic for interface/API/config schemas,
- Protocol for ports.

Avoid:

- untyped dictionaries as public contracts,
- `Any` unless unavoidable,
- dynamic attribute mutation.

---

# 6. Domain Layer Standards

Domain code must be pure Python.

Allowed:

- dataclasses,
- enums,
- value objects,
- domain exceptions,
- pure validation logic.

Not allowed:

- FastAPI imports,
- ADK imports,
- database imports,
- filesystem writes,
- network calls,
- environment variable reads.

---

# 7. Application Layer Standards

Application services coordinate domain logic and ports.

Application services may:

- call domain entities,
- call ports,
- manage use cases,
- enforce workflow policies.

Application services must not:

- import concrete infrastructure adapters,
- directly call external APIs,
- perform ungoverned filesystem access.

---

# 8. Infrastructure Standards

Infrastructure implements ports.

Infrastructure modules may contain:

- database adapters,
- local file storage,
- MCP adapters,
- model clients,
- Git integration,
- Docker integration.

Every infrastructure adapter must have tests.

---

# 9. Agent Standards

Every agent plugin must expose:

- metadata,
- capabilities,
- required tools,
- input schema,
- output schema,
- execution method.

Agent code must not:

- directly access secrets,
- directly invoke shell commands,
- directly write files outside approved artifact APIs,
- bypass security checks.

---

# 10. Error Handling

Use domain-specific exceptions.

Examples:

- `WorkflowStateError`
- `PluginLoadError`
- `ToolPermissionDeniedError`
- `EvaluationGateFailedError`
- `MemoryScopeError`

Do not swallow exceptions silently.

Every caught exception must either:

- be converted into a structured result,
- be logged and re-raised,
- trigger a retry policy,
- trigger a workflow failure state.

---

# 11. Logging Standards

Use structured logs.

Required fields when available:

- `workflow_id`,
- `run_id`,
- `task_id`,
- `agent_id`,
- `tool_name`,
- `duration_ms`,
- `status`,
- `risk_level`.

Do not log:

- raw API keys,
- personal secrets,
- full prompt payloads containing sensitive data,
- unmasked environment variables.

---

# 12. Testing Standards

Every test must assert behavior.

Minimum test rules:

- one unit test per domain policy,
- one unit test per application service,
- one integration test per infrastructure adapter,
- one workflow test per workflow type,
- one security test per denied action,
- one evaluation test per quality gate.

Preferred test naming:

```text
test_<unit_under_test>_<condition>_<expected_behavior>.py
```

Example:

```python
def test_router_no_matching_capability_returns_no_route():
    ...
```

---

# 13. Configuration Standards

Configuration must use environment variables or config files.

Required `.env.example` values:

```env
GOOGLE_API_KEY=
AGENTFORGE_ENV=local
AGENTFORGE_WORKSPACE=.agentforge
AGENTFORGE_LOG_LEVEL=INFO
AGENTFORGE_DEFAULT_MODEL=gemini-2.5-flash
```

Never commit real secrets.

---

# 14. Documentation Standards

Every public module should include a short module docstring.

Every public class should document:

- responsibility,
- key collaborators,
- failure modes.

Every architecture-significant change should update documentation or add an ADR.

---

# 15. Commit Discipline

Each milestone should produce small commits grouped by purpose:

```text
feat(runtime): add plugin registry contract
feat(workflow): add workflow state machine
feat(security): add tool permission policy
fix(memory): prevent cross-project context leakage
test(workflow): cover approval pause state
docs(architecture): add ADR for local storage adapter
```
