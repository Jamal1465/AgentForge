# agent_builder_playbook.md

Project: AgentForge  
Purpose: Step-by-step operating manual for AI coding assistants

---

# 1. Playbook Purpose

This playbook tells an AI coding assistant how to build AgentForge safely and incrementally.

The assistant must not act like a free-form chatbot. It must act like a disciplined software engineer working from architecture documents, build rules, milestones, and tests.

---

# 2. Builder Operating Loop

For every development session, follow this loop:

```text
Read Context
  ↓
Identify Current Milestone
  ↓
Inspect Existing Files
  ↓
Plan Minimal Change
  ↓
Implement
  ↓
Test
  ↓
Review Against Architecture
  ↓
Document
  ↓
Stop or Continue
```

---

# 3. Mandatory Pre-Code Checklist

Before writing code, verify:

- Current milestone is known.
- Architecture package has been read.
- Existing files have been inspected.
- Required interfaces are identified.
- Tests to be added are known.
- No open test failures exist.

If any item fails, do not write feature code.

---

# 4. Phase 0 — Documentation Alignment

Objective: Understand the project before coding.

Required actions:

1. Read `00_READ_FIRST.md`.
2. Read `AI_CONTEXT.md`.
3. Read `BUILD_RULES.md`.
4. Read `CODING_STANDARDS.md`.
5. Read architecture documents.
6. Read current milestone.

Exit criteria:

- Builder can explain AgentForge in 5 lines.
- Builder can name the current architecture boundaries.
- Builder can identify forbidden shortcuts.

---

# 5. Phase 1 — Project Foundation

Objective: Create a runnable empty repository.

Deliverables:

- `pyproject.toml`
- `README.md`
- `.env.example`
- `.gitignore`
- source package directories
- tests directory
- quality tooling

Validation:

```bash
uv sync
uv run pytest
uv run ruff check .
```

---

# 6. Phase 2 — Core Contracts

Objective: Define stable contracts before concrete implementations.

Deliverables:

- domain entities,
- value objects,
- ports,
- plugin protocol,
- task/result schemas,
- workflow state model.

Do not implement complex agents yet.

---

# 7. Phase 3 — Registry and Routing

Objective: Allow agents to be discovered and selected by capability.

Deliverables:

- plugin loader,
- agent registry,
- capability router,
- routing decision record,
- tests for no match, one match, and multiple matches.

Rule:

The orchestrator must never hardcode agent class names.

---

# 8. Phase 4 — Workflow Engine

Objective: Execute explicit workflow graphs.

Deliverables:

- workflow definition,
- workflow state machine,
- node runner,
- retry policy,
- approval pause,
- persistence port.

Validation must include state transition tests.

---

# 9. Phase 5 — Memory System

Objective: Preserve structured context safely.

Deliverables:

- request memory,
- session memory,
- project memory,
- decision log,
- artifact store,
- context pack builder.

Rule:

Agents must receive scoped context packs, not raw global memory.

---

# 10. Phase 6 — Tool and MCP Gateway

Objective: Add governed tool execution.

Deliverables:

- tool registry,
- tool gateway,
- tool policy,
- audit log,
- MCP adapter,
- filesystem adapter,
- Git adapter.

Rule:

No direct shell/filesystem/Git access from agents.

---

# 11. Phase 7 — Built-In Agents

Objective: Add the first internal agent team.

Recommended sequence:

1. Planner Agent
2. Research Agent
3. Architect Agent
4. Backend Agent
5. Frontend Agent
6. Database Agent
7. DevOps Agent
8. Security Agent
9. Evaluation Agent
10. Documentation Agent

Each agent must have tests for metadata, capabilities, input validation, and structured result.

---

# 12. Phase 8 — Security Layer

Objective: Enforce safety before risky actions.

Deliverables:

- prompt injection scanner,
- tool permission checker,
- secret masker,
- workspace boundary checker,
- generated code security checks,
- human approval gate for high-risk actions.

---

# 13. Phase 9 — Evaluation Framework

Objective: Make quality measurable.

Deliverables:

- evaluation report model,
- quality gates,
- rubric evaluator,
- automated checks,
- refinement policy.

Every generated artifact should produce an evaluation report.

---

# 14. Phase 10 — Interfaces

Objective: Expose AgentForge through CLI and API.

Deliverables:

- Typer CLI,
- FastAPI API,
- request/response schemas,
- health endpoints,
- run status endpoint.

CLI must be implemented before web UI.

---

# 15. Phase 11 — Deployment

Objective: Make the app reproducible.

Deliverables:

- Dockerfile,
- docker-compose.yml,
- GitHub Actions,
- release scripts,
- local demo script.

---

# 16. Phase 12 — Submission Package

Objective: Prepare Kaggle/Google capstone submission.

Deliverables:

- final README,
- demo guide,
- architecture summary,
- presentation outline,
- evaluation results,
- demo video script,
- submission checklist.

---

# 17. Failure Handling

If tests fail:

1. Stop new feature work.
2. Identify failing boundary.
3. Fix root cause.
4. Re-run tests.
5. Update docs if behavior changed.

If architecture conflicts appear:

1. Stop.
2. Write an ADR draft.
3. Ask for human approval.
4. Continue only after approval.

---

# 18. Final Rule

Build AgentForge as a sequence of verified vertical slices. A small working system is better than a large broken codebase.
