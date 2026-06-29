# Milestone 10 — Observability and Telemetry

Project: AgentForge  
Version: 1.0.0  
Status: Completed  
Depends On: Milestone 09 — Evaluation Framework

---

## 1. Objective

Implement an observability layer that makes AgentForge workflow execution transparent, inspectable, and auditable without coupling the core runtime to a specific monitoring vendor.

The milestone must support structured telemetry events, metrics, and trace spans for workflows, nodes, routing decisions, plugin execution, security decisions, evaluation results, and tool calls.

---

## 2. Architectural Rule

AgentForge remains capability-first and plugin-first.

The observability layer must not emit telemetry based on hardcoded agent roles such as:

- Backend Agent,
- Frontend Agent,
- Database Agent,
- DevOps Agent.

Instead, it must observe:

- workflow IDs,
- node IDs,
- task IDs,
- required capabilities,
- selected plugin IDs,
- tool IDs,
- security decisions,
- evaluation reports,
- execution status.

---

## 3. Functional Requirements Covered

This milestone supports:

- workflow traceability,
- event logging,
- plugin execution visibility,
- routing decision visibility,
- security audit visibility,
- evaluation result visibility,
- tool execution visibility,
- future monitoring adapter support.

---

## 4. Non-Functional Requirements Covered

This milestone supports:

- observability,
- testability,
- maintainability,
- extensibility,
- auditability,
- operational transparency.

---

## 5. Required Components

### 5.1 Domain Layer

Implement:

```text
src/agentforge/domain/observability.py
```

Required objects:

- `TraceContext`
- `TelemetryEvent`
- `MetricPoint`
- `SpanRecord`
- `TelemetrySeverity`
- `TelemetryEventType`
- `MetricType`
- `SpanStatus`

### 5.2 Application Layer

Implement:

```text
src/agentforge/application/observability/ports.py
src/agentforge/application/observability/service.py
```

Required interfaces:

- `ObservabilityStore`

Required service:

- `ObservabilityService`

### 5.3 Infrastructure Layer

Implement:

```text
src/agentforge/infrastructure/persistence/observability_store.py
```

Required adapter:

- `InMemoryObservabilityStore`

### 5.4 Runtime Layer

Implement:

```text
src/agentforge/runtime/tools/observable_executor.py
```

Required wrapper:

- `ObservableToolExecutor`

---

## 6. Workflow Integration

The workflow runner shall emit telemetry for:

- `workflow.started`
- `workflow.completed`
- `workflow.failed`
- `workflow.deadlocked`
- `approval.required`
- `approval.granted`
- `approval.rejected`
- `node.started`
- `node.completed`
- `node.failed`
- `routing.routed`
- `routing.failed`
- `plugin.execution.success`
- `plugin.execution.failed`
- `security.allow`
- `security.requires_approval`
- `security.block`
- `evaluation.passed`
- `evaluation.warning`
- `evaluation.failed`
- `evaluation.quality_gate_failed`

---

## 7. Metrics

At minimum, the platform shall record metrics for:

```text
workflow.started_total
workflow.finished_total
workflow.node.started_total
workflow.node.finished_total
workflow.approval_required_total
routing.finished_total
plugin.execution.finished_total
security.decision_total
evaluation.finished_total
tool.execution.started_total
tool.execution.finished_total
span.duration_ms
```

---

## 8. Trace Strategy

The initial implementation shall use the workflow ID as the trace ID.

This keeps trace correlation deterministic during local testing and avoids requiring external tracing infrastructure.

Future versions may replace this with OpenTelemetry-compatible trace IDs without changing the domain or workflow contracts.

---

## 9. Testing Requirements

Add tests for:

- observability domain validation,
- event creation,
- metric creation,
- span lifecycle,
- in-memory store filtering,
- observable tool executor,
- workflow runner telemetry integration.

---

## 10. Acceptance Criteria

Milestone 10 is complete when:

- observability domain objects exist,
- observability service exists,
- observability store port exists,
- in-memory observability store exists,
- workflow runner emits telemetry when service is provided,
- tool execution can be wrapped with telemetry,
- tests cover the main behavior,
- all existing tests pass,
- no hardcoded engineering agent roles are introduced.

---

## 11. Validation Commands

```bash
python -m pytest -q
python -m compileall -q src tests
```

Expected result after implementation:

```text
87 passed
```

---

## 12. Next Milestone

Milestone 11 should implement:

- interfaces,
- composition root,
- FastAPI entrypoint,
- CLI improvements,
- deployment assets,
- Docker support,
- health checks.
