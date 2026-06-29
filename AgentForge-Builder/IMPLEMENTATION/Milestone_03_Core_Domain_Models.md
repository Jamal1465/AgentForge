# Milestone 03 — Core Domain Models

Project: AgentForge  
Status: Completed  
Architecture References: `ARCHITECTURE/05_System_Architecture.md`

---

# 1. Objective

Implement pure domain models for projects, tasks, agents, workflows, artifacts, decisions, and tool requests.

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

- `domain/entities/`
- `domain/value_objects/`
- `domain/events/`
- `domain/policies/`

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

- [ ] domain has no framework imports
- [ ] entity validation tests pass
- [ ] value object tests pass

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

Milestone 03 has been fully completed.

Completed features:
- Implemented pure framework-free domain models:
  - `entities.py` (Project, ProjectTask, Artifact, TaskStatus)
  - `value_objects.py` (Capability, RiskLevel)
  - `workflow.py` (WorkflowGraph, WorkflowNode, WorkflowStatus, WorkflowNodeStatus)
  - `memory.py` (MemoryScope, MemoryKind, MemoryRecord, MemoryQuery)
  - `tools.py` (ToolKind, ToolExecutionStatus, ToolDefinition, ToolInvocation, ToolResult, ToolExecutionPolicy)
  - `security.py` (SecurityFindingType, SecurityFinding, SecurityDecisionStatus, SecurityDecision, SecurityPolicy)
  - `evaluation.py` (EvaluationSubjectType, EvaluationStatus, EvaluationMetricCategory, EvaluationSubject, EvaluationCriterion, EvaluationScore, EvaluationFinding, EvaluationRubric, EvaluationReport, QualityGate)
  - `observability.py` (TelemetrySeverity, TelemetryEventType, MetricType, SpanStatus, TraceContext, TelemetryEvent, MetricPoint, SpanRecord)
- Verified all models through comprehensive domain unit tests in `tests/`.
