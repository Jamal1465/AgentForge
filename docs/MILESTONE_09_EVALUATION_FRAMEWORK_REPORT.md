# Milestone 09 — Evaluation Framework Report

Project: AgentForge  
Status: Completed in source scaffold  
Validation Date: June 28, 2026

---

## 1. Objective

Implement a deterministic, capability-first evaluation framework for AgentForge.

The framework evaluates plugin outputs, workflow outputs, and generated artifacts without depending on hardcoded agent roles such as Backend Agent, Frontend Agent, Database Agent, or DevOps Agent.

---

## 2. Architecture Position

The evaluation framework sits after plugin execution and before workflow node completion.

```text
Workflow Node
      ↓
Capability Router
      ↓
Registered Plugin
      ↓
AgentResult
      ↓
EvaluationService
      ↓
QualityGate
      ↓
Continue / Fail Safely
```

This preserves the plugin-first architecture:

- the Planner requests capabilities,
- the Registry selects plugins,
- the Workflow Runner executes selected plugins,
- the Evaluation Framework scores returned outputs,
- the Quality Gate decides whether the workflow may continue.

---

## 3. Implemented Components

### Domain Layer

- `EvaluationSubject`
- `EvaluationSubjectType`
- `EvaluationCriterion`
- `EvaluationMetricCategory`
- `EvaluationScore`
- `EvaluationFinding`
- `EvaluationRubric`
- `EvaluationReport`
- `EvaluationStatus`
- `QualityGate`

### Application Layer

- `EvaluationStore` port
- `EvaluationService`
- default agent-result rubric
- default artifact rubric
- default workflow rubric
- quality gate checks

### Infrastructure Layer

- `InMemoryEvaluationStore`

### Workflow Integration

- `WorkflowRunner` now accepts an optional `EvaluationService`.
- Successful plugin results are evaluated before the node is marked completed.
- Failed quality gates fail the node safely.
- Evaluation events are written to workflow audit events.
- Evaluation outcomes are optionally written to memory when memory is configured.

---

## 4. Capability-First Behavior

The evaluation layer evaluates outputs by subject type and declared task capabilities.

Example:

```python
ProjectTask(
    title="Implement API",
    required_capabilities=(Capability("api-development"),),
)
```

The evaluation framework does not need to know whether the selected plugin is a FastAPI plugin, Django plugin, Node.js plugin, or another future implementation.

---

## 5. Quality Gates

The default quality gate enforces:

- minimum overall score,
- required criterion pass/fail,
- high or critical finding blocking.

A report passes only when:

```text
overall_score >= min_overall_score
AND no failed required criteria
AND no high/critical blocking findings
```

---

## 6. Tests Added

- `tests/test_evaluation_domain.py`
- `tests/test_evaluation_service.py`
- `tests/test_evaluation_store.py`
- `tests/test_workflow_evaluation_integration.py`

---

## 7. Validation

Command:

```bash
python -m pytest -q
```

Result:

```text
79 passed
```

Command:

```bash
python -m compileall -q src tests
```

Result: successful.

`ruff` and `mypy` are configured in `pyproject.toml`, but they were not installed in the current execution environment.

---

## 8. New Source Files

```text
src/agentforge/domain/evaluation.py
src/agentforge/application/evaluation/__init__.py
src/agentforge/application/evaluation/ports.py
src/agentforge/application/evaluation/service.py
src/agentforge/infrastructure/persistence/evaluation_store.py
tests/test_evaluation_domain.py
tests/test_evaluation_service.py
tests/test_evaluation_store.py
tests/test_workflow_evaluation_integration.py
```

---

## 9. Modified Source Files

```text
src/agentforge/application/workflows/runner.py
README.md
```

---

## 10. Exit Criteria

Milestone 09 is complete because:

- evaluation domain model exists,
- application service exists,
- persistence port exists,
- in-memory persistence adapter exists,
- workflow integration exists,
- quality gates are enforced,
- tests cover domain, service, persistence, and workflow integration,
- the implementation remains capability-first and plugin-first.
