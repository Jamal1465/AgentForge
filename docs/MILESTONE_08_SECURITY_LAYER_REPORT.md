# Milestone 08 — Security Layer Report

Project: AgentForge  
Status: Completed  
Package: Source Scaffold  

---

## 1. Objective

Milestone 08 adds a capability-first security layer to AgentForge.

The implementation protects workflow execution, plugin metadata, and tool execution without hardcoding agent roles such as backend, frontend, database, or DevOps. Security policy is expressed in terms of capabilities, risk levels, plugin metadata, tool metadata, text scanning, and approval decisions.

---

## 2. Architectural Decision

AgentForge now treats security as an application service placed between orchestration and execution boundaries.

The core security model uses:

- capabilities,
- risk levels,
- plugin metadata,
- tool definitions,
- text scanning,
- audit events,
- approval decisions.

The Planner, Workflow Engine, Agent Registry, and Capability Matcher do not need to know concrete agent class names. A task asking for `deployment` or `infrastructure` can be paused, blocked, or allowed by policy regardless of which plugin provides that capability.

---

## 3. Added Source Files

```text
src/agentforge/domain/security.py
src/agentforge/application/security/__init__.py
src/agentforge/application/security/ports.py
src/agentforge/application/security/service.py
src/agentforge/infrastructure/persistence/security_audit_store.py
src/agentforge/runtime/tools/secure_executor.py
```

---

## 4. Updated Source Files

```text
src/agentforge/domain/value_objects.py
src/agentforge/application/workflows/runner.py
README.md
```

---

## 5. Added Tests

```text
tests/test_security_domain.py
tests/test_security_service.py
tests/test_secure_tool_executor.py
tests/test_workflow_security_integration.py
```

---

## 6. Implemented Capabilities

### Security Domain

- `SecurityFinding`
- `SecurityDecision`
- `SecurityPolicy`
- `SecurityAuditEvent`
- `SecurityFindingType`
- `SecurityDecisionStatus`

### Guardrails

- prompt-injection detection,
- secret-like value detection,
- basic PII detection,
- blocked capability enforcement,
- approval-required capability enforcement,
- high-risk task approval enforcement,
- untrusted plugin blocking,
- destructive tool blocking,
- security audit recording.

### Workflow Integration

The `WorkflowRunner` can now receive an optional `SecurityService`.

Before routing a task to a plugin, the runner assesses the task against security policy.

Outcomes:

- `ALLOW` → route and execute normally,
- `REQUIRES_APPROVAL` → pause workflow,
- `BLOCK` → fail the node and workflow safely.

### Tool Integration

`SecureToolExecutor` wraps `SafeToolExecutor`.

It performs security assessment before the underlying tool adapter executes and redacts secret-like output values after execution.

---

## 7. Capability-First Policy Examples

```python
SecurityPolicy(
    blocked_capabilities=(Capability("infrastructure"),),
    approval_required_capabilities=(Capability("deployment"),),
)
```

This blocks any task requiring `infrastructure` and pauses any task requiring `deployment`, regardless of which plugin provides that capability.

---

## 8. Validation

Commands executed:

```bash
python -m pytest -q
python -m compileall -q src tests
```

Result:

```text
68 passed
```

`ruff` and `mypy` are configured in `pyproject.toml`, but were not installed in the current execution environment.

---

## 9. Exit Criteria

- [x] Security domain model exists.
- [x] Capability-first policy exists.
- [x] Prompt-injection scanner exists.
- [x] Secret redaction exists.
- [x] Security audit store exists.
- [x] Tool execution security wrapper exists.
- [x] Workflow execution security integration exists.
- [x] Tests pass.
- [x] No hardcoded engineering role routing was added.

---

## 10. Next Milestone

The next recommended milestone is **Milestone 09 — Evaluation Framework**.

That milestone should evaluate generated artifacts, agent outputs, workflow quality, security results, and documentation completeness.
