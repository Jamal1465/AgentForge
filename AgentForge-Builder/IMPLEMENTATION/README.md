# IMPLEMENTATION Package

Project: AgentForge  
Purpose: Milestone-by-milestone implementation guide

---

# 1. How To Use This Package

Each milestone is a focused engineering specification. Implement only one milestone at a time.

Do not skip ahead. Later milestones depend on contracts created in earlier milestones.

AgentForge is capability-first and plugin-first. Avoid hardcoded core references to fixed engineering roles such as Backend Agent, Frontend Agent, or Database Agent. The core platform should reason about capabilities and plugin metadata.

---

# 2. Milestone Order

1. Project Foundation
2. Repository Scaffold
3. Core Domain Models
4. Plugin Registry and Capability Router
5. Workflow Engine
6. Memory System
7. Tool and MCP Gateway
8. Security Layer
9. Evaluation Framework
10. Observability and Telemetry
11. Interfaces and Deployment
12. Submission Package

---

# 3. Milestone Completion Rules

A milestone is complete only when:

- implementation is present,
- tests are present,
- quality checks pass,
- documentation is updated,
- architecture boundaries remain valid,
- no placeholder implementation remains,
- the orchestration core remains independent of concrete agent implementations.

---

# 4. Validation Commands

Default validation commands:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

If a command is not yet available during early milestones, document why and add it as soon as tooling exists.
