# Milestone 05 — Workflow Engine

Project: AgentForge  
Status: Completed in source scaffold  
Architecture References: `ARCHITECTURE/05_System_Architecture.md`

---

# 1. Objective

Implement explicit workflow graphs, workflow state machine, workflow runner, retry policy, and human approval pause.

---

# 2. Why This Milestone Exists

This milestone creates a controlled step in the AgentForge build process. It prevents the codebase from becoming a set of disconnected AI-generated files and ensures each layer is built in the correct order.

---

# 3. Required Inputs

Before starting this milestone, read:

- `00_READ_FIRST.md`
- `AI_CONTEXT.md`
- `BUILD_RULES.md`
- `CODING_STANDARDS.md`
- `ARCHITECTURE/05_System_Architecture.md`
- the architecture document most closely related to this milestone

---

# 4. Deliverables

- `application/workflows/`
- `domain/workflow.py`
- `infrastructure/persistence/workflow_store.py`

---

# 5. Implementation Rules

- Preserve Clean Architecture boundaries.
- Add tests with implementation.
- Avoid final placeholder implementations.
- Keep public contracts typed and documented.
- Do not bypass plugin, workflow, memory, tool, security, or evaluation boundaries.
- Do not introduce direct framework dependencies into the domain layer.

---

# 6. Suggested Implementation Steps

1. Inspect the current repository state.
2. Identify affected architecture components.
3. Create or update only the files required by this milestone.
4. Add unit tests first where practical.
5. Implement behavior incrementally.
6. Run validation commands.
7. Update documentation if contracts changed.
8. Record unresolved issues clearly.

---

# 7. Testing Requirements

Minimum checks:

- [x] state transitions validated
- [x] approval pause resumable
- [x] retry tests pass

Recommended commands once tooling exists:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

---

# 8. Exit Criteria

This milestone is complete when:

- all deliverables exist,
- relevant tests pass,
- no unrelated files were rewritten,
- architecture boundaries remain valid,
- documentation is updated where necessary,
- there are no silent failures or fake success messages.

---

# 9. Common Pitfalls

Avoid:

- implementing future milestones too early,
- creating hardcoded shortcuts,
- skipping tests because the milestone seems simple,
- placing infrastructure code inside domain,
- hiding incomplete behavior behind comments,
- changing architecture documents without approval.

---

# 10. Review Questions

Before marking this milestone complete, answer:

1. Which architecture document did this milestone implement?
2. Which tests prove the behavior?
3. Which public contracts were created or changed?
4. Which risks remain?
5. What is the next milestone?

---

# 11. Implementation Completion Notes

Milestone 05 has been implemented in the source scaffold.

Implemented files:

```text
src/agentforge/domain/workflow.py
src/agentforge/application/workflows/ports.py
src/agentforge/application/workflows/runner.py
src/agentforge/infrastructure/persistence/workflow_store.py
tests/test_workflow_domain.py
tests/test_workflow_runner.py
```

Validation result:

```bash
python -m pytest -q
# 18 passed
```

Remaining future work:

- parallel workflow execution,
- durable workflow persistence,
- structured telemetry export,
- ADK-backed runtime adapter.
