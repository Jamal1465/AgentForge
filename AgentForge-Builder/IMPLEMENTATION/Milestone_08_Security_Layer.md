# Milestone 08 — Security Layer

Project: AgentForge  
Status: Completed in source scaffold  
Architecture References: `ARCHITECTURE/10_Security_Architecture.md`, `ARCHITECTURE/05_System_Architecture.md`

---

# 1. Objective

Implement a capability-first security layer that protects workflow execution, plugin metadata, tool invocation, and generated content.

The security layer must not depend on hardcoded engineering agent names. It must enforce policy using capabilities, risk levels, plugin metadata, tool metadata, and content findings.

---

# 2. Deliverables

- security domain model,
- security application service,
- security audit store port,
- in-memory security audit store,
- prompt-injection checks,
- secret redaction,
- capability block/approval rules,
- plugin trust policy,
- secure tool executor,
- workflow security integration,
- tests.

---

# 3. Capability-First Policy

Security policy shall reference capabilities rather than concrete agents.

Example:

```python
SecurityPolicy(
    blocked_capabilities=(Capability("infrastructure"),),
    approval_required_capabilities=(Capability("deployment"),),
)
```

This blocks infrastructure tasks and pauses deployment tasks regardless of which plugin provides those capabilities.

---

# 4. Required Files

```text
src/agentforge/domain/security.py
src/agentforge/application/security/ports.py
src/agentforge/application/security/service.py
src/agentforge/infrastructure/persistence/security_audit_store.py
src/agentforge/runtime/tools/secure_executor.py
```

---

# 5. Required Tests

```text
tests/test_security_domain.py
tests/test_security_service.py
tests/test_secure_tool_executor.py
tests/test_workflow_security_integration.py
```

---

# 6. Exit Criteria

- [x] Prompt-injection attempts can be detected and blocked.
- [x] Secret-like output values can be redacted.
- [x] High-risk capabilities can require approval.
- [x] Blocked capabilities fail safely.
- [x] Plugin trust policy can block untrusted plugins.
- [x] Destructive tools can be blocked by policy.
- [x] Security decisions are auditable.
- [x] Workflow execution pauses on approval-required security decisions.
- [x] Tests pass.

---

# 7. Validation

```bash
python -m pytest -q
python -m compileall -q src tests
```

Result:

```text
68 passed
```
