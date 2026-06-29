# Milestone 09 — Evaluation Framework

Project: AgentForge  
Status: Completed in source scaffold  
Architecture References: `ARCHITECTURE/11_Evaluation_Architecture.md`, `ARCHITECTURE/05_System_Architecture.md`

---

# 1. Objective

Implement a capability-first evaluation framework that scores plugin results, generated artifacts, workflow health, and future tool outputs without depending on hardcoded agent roles.

The evaluation framework must support deterministic quality checks first and remain extensible for future LLM-as-judge, benchmark, regression, and human review evaluators.

---

# 2. Design Rule

The evaluation layer must not know concrete engineering agent names.

Do not evaluate using assumptions such as:

- Backend Agent,
- Frontend Agent,
- Database Agent,
- DevOps Agent.

Evaluate using:

- subject type,
- declared capabilities,
- rubric criteria,
- findings,
- quality gates,
- workflow context.

Example:

```text
required capability: api-development
selected plugin: any compatible registered plugin
subject evaluated: agent result
rubric applied: default agent result rubric
quality gate: default-quality-gate
```

---

# 3. Deliverables

This milestone shall produce:

- evaluation domain model,
- evaluation store port,
- evaluation service,
- deterministic rubrics,
- quality gate logic,
- in-memory evaluation store,
- workflow runner integration,
- evaluation audit events,
- tests for domain, service, store, and workflow integration.

---

# 4. Required Source Files

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

# 5. Domain Model

The domain layer shall define:

- `EvaluationSubject`,
- `EvaluationSubjectType`,
- `EvaluationCriterion`,
- `EvaluationMetricCategory`,
- `EvaluationScore`,
- `EvaluationFinding`,
- `EvaluationRubric`,
- `EvaluationReport`,
- `EvaluationStatus`,
- `QualityGate`.

All domain models must be framework-free.

---

# 6. Application Service

The `EvaluationService` shall provide:

- `evaluate_agent_result`,
- `evaluate_artifact`,
- `evaluate_workflow`,
- `passes_quality_gate`.

The service shall be deterministic in this milestone.

Future LLM-as-judge evaluators may be added behind the same application boundary.

---

# 7. Quality Gate Rules

A report passes the default gate only when:

```text
overall_score >= min_overall_score
AND no failed required criteria
AND no high/critical findings
```

Failed quality gates must prevent unsafe or low-quality workflow continuation.

---

# 8. Workflow Integration

The `WorkflowRunner` shall accept an optional `EvaluationService`.

When configured:

1. agent plugin executes task,
2. plugin returns `AgentResult`,
3. evaluation service scores the result,
4. report is persisted,
5. workflow event is recorded,
6. node completes only if the quality gate passes.

---

# 9. Acceptance Criteria

Milestone 09 is complete when:

- evaluation reports can be created,
- quality gates can pass or fail reports,
- reports can be persisted and queried,
- workflow nodes fail safely when evaluation fails,
- evaluation works by capabilities and subject types,
- tests pass.

---

# 10. Validation Evidence

Current source scaffold validation:

```text
79 passed
```

Python compilation:

```text
python -m compileall -q src tests
```

completed successfully.
