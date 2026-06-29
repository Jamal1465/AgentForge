# AI_CONTEXT.md

Project: AgentForge  
Audience: AI coding assistants, Antigravity IDE, Gemini/Codex-style builders  
Status: Mandatory context file

---

# 1. Core Identity

AgentForge is a production-grade multi-agent AI software engineering platform. It behaves like an AI Software Engineering Operating System.

Architecture metaphor:

| AgentForge Component | Operating System Analogy |
|---|---|
| Workflow Engine | Scheduler |
| Agent Registry | Process manager |
| Agent Plugins | Executable programs |
| Memory Layer | File system and working memory |
| MCP/Tool Gateway | Device driver layer |
| Security Guard | Kernel permission boundary |
| Evaluation Engine | Quality gate and diagnostics |
| Human Approval | Privileged user confirmation |

This metaphor should guide naming, responsibilities, and boundaries.

---

# 2. Primary Goal

Build a system where specialized agents collaborate to create software projects from natural-language ideas.

The system must support:

- project intake,
- planning,
- architecture generation,
- task decomposition,
- agent routing,
- tool execution,
- memory persistence,
- human approval,
- code generation,
- security validation,
- evaluation,
- documentation,
- export.

---

# 3. Implementation Stack

Default stack:

- Language: Python 3.11+
- Package manager: `uv`
- Agent framework: Google ADK-compatible design
- API: FastAPI
- CLI: Typer
- Data validation: Pydantic
- Testing: Pytest
- Type checking: MyPy or Pyright
- Linting/formatting: Ruff
- Containers: Docker
- CI: GitHub Actions
- Docs: Markdown and Mermaid diagrams

Do not introduce a different default stack unless the user explicitly changes the architecture.

---

# 4. Architectural Rules

The implementation must follow:

- Clean Architecture
- Hexagonal Architecture
- Ports and Adapters
- Dependency Inversion
- Plugin-first extensibility
- Explicit workflow graphs
- Structured state management
- Secure tool gateway
- Evaluation-driven development

Domain code must never depend on infrastructure frameworks.

---

# 5. AgentForge Core Components

Required components:

1. Domain Layer
   - entities
   - value objects
   - domain events
   - policies

2. Application Layer
   - commands
   - queries
   - services
   - workflows
   - ports

3. Runtime Layer
   - orchestrator
   - agent registry
   - plugin loader
   - capability router
   - ADK adapter

4. Agents Layer
   - planner
   - research
   - architect
   - backend
   - frontend
   - database
   - devops
   - security
   - evaluation
   - documentation

5. Infrastructure Layer
   - persistence
   - memory
   - artifacts
   - tools
   - MCP
   - Git
   - Docker
   - model clients

6. Governance Layer
   - security
   - evaluation
   - observability
   - audit

7. Interfaces Layer
   - CLI
   - API
   - schemas

---

# 6. Behavior Expected From AI Builder

When implementing:

- Read the current milestone.
- Inspect existing code before editing.
- Make minimal coherent changes.
- Preserve public interfaces.
- Add tests with implementation.
- Run tests before moving forward.
- Explain changes using architecture terms.
- Stop when a quality gate fails.

---

# 7. Output Quality

Generated code must include:

- type hints,
- docstrings for public APIs,
- structured errors,
- logging where execution crosses boundaries,
- configuration externalization,
- tests,
- examples where useful.

Generated documentation must include:

- purpose,
- responsibilities,
- inputs,
- outputs,
- failure cases,
- extension notes.

---

# 8. Forbidden Shortcuts

Never satisfy a milestone by writing only comments or placeholders.

Forbidden patterns:

```python
pass
raise NotImplementedError
# TODO: implement later
return {}
```

These are allowed only in abstract interfaces or explicitly marked future extension files.

---

# 9. Review Checklist Before Responding

Before presenting any generated implementation, verify:

- Does it follow the architecture package?
- Does it avoid hardcoded agent routing?
- Does it preserve plugin contracts?
- Does it include tests?
- Does it avoid secrets?
- Does it remain runnable?
- Does it avoid fake success messages?
