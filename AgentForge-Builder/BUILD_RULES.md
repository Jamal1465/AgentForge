# BUILD_RULES.md

Project: AgentForge  
Status: Mandatory implementation rules

---

# 1. Purpose

This document defines non-negotiable implementation rules for AgentForge. It exists to prevent an AI coding assistant from producing a loosely connected demo instead of a clean multi-agent software architecture.

---

# 2. Build Rule Categories

| Category | Purpose |
|---|---|
| BR-A | Architecture integrity |
| BR-B | Agent implementation |
| BR-C | Workflow implementation |
| BR-D | Memory implementation |
| BR-E | Tool and MCP implementation |
| BR-F | Security implementation |
| BR-G | Evaluation implementation |
| BR-H | Testing and quality |
| BR-I | Documentation |

---

# 3. Architecture Integrity Rules

## BR-A001 — Preserve Layer Boundaries

Domain modules must not import application, runtime, infrastructure, interfaces, or governance modules.

Allowed dependency direction:

```text
interfaces -> application -> domain
runtime -> application -> domain
infrastructure -> application ports -> domain
governance -> application/domain contracts
```

## BR-A002 — No Framework Leakage Into Domain

Domain entities must not import:

- FastAPI
- Typer
- Google ADK
- SQLAlchemy
- Pydantic settings
- Docker SDK
- MCP SDK

## BR-A003 — Ports Before Adapters

Any external dependency must be represented by an application port before an infrastructure adapter is written.

Examples:

- `MemoryStorePort` before `LocalMemoryStore`
- `ToolExecutorPort` before `MCPToolExecutor`
- `ModelClientPort` before `GeminiModelClient`

## BR-A004 — Configuration Over Hardcoding

Models, tools, plugins, workspace paths, retry policies, logging levels, and security policies must be externally configurable.

---

# 4. Agent Rules

## BR-B001 — Every Agent Must Be a Plugin

Agents must implement the common agent plugin contract.

Each agent must declare:

- ID
- name
- version
- capabilities
- required tools
- input schema
- output schema
- risk level

## BR-B002 — No Hardcoded Agent Routing

The orchestrator must route tasks through capabilities, not direct class names.

Wrong:

```python
if task.type == "backend":
    return BackendAgent()
```

Correct:

```python
router.select_agent(task.required_capabilities)
```

## BR-B003 — Agents Return Structured Results

Agents must return a structured result containing:

- status
- artifacts
- decisions
- confidence
- warnings
- errors
- evaluation hints

## BR-B004 — Agents Must Not Access Tools Directly

Agents request tools through the Tool Gateway only.

---

# 5. Workflow Rules

## BR-C001 — Workflows Are Explicit Graphs

Workflows must be represented as graph definitions with nodes, edges, conditions, state transitions, and exit criteria.

## BR-C002 — Human Approval Must Be Modeled As a State

Human approval is not a comment or optional pause. It must be a workflow state with resumable execution.

## BR-C003 — Retry Policies Must Be Explicit

Retries must define:

- max attempts,
- backoff strategy,
- retryable error classes,
- non-retryable error classes,
- audit behavior.

---

# 6. Memory Rules

## BR-D001 — Memory Must Be Scoped

Memory must distinguish:

- request memory,
- session memory,
- project memory,
- knowledge memory.

## BR-D002 — Decisions Must Be Persisted

Architecture decisions, security decisions, routing decisions, and human approval decisions must be recorded.

## BR-D003 — Memory Retrieval Must Be Intentional

Agents must not receive unlimited memory. They receive context packs selected for the task.

---

# 7. Tool and MCP Rules

## BR-E001 — All Tool Calls Pass Through Tool Gateway

No direct filesystem, shell, Git, or network operation may bypass the Tool Gateway.

## BR-E002 — Risky Tools Require Permission Policies

Risky operations include:

- file deletion,
- shell execution,
- Git push,
- dependency installation,
- secret access,
- deployment,
- external API calls.

## BR-E003 — Tool Calls Must Be Audited

Every tool call must record:

- caller,
- task ID,
- tool name,
- arguments hash,
- timestamp,
- result status,
- duration,
- security decision.

---

# 8. Security Rules

## BR-F001 — Prompt Injection Guard Required

User input and retrieved external content must be inspected before being used in prompts or tool calls.

## BR-F002 — Secrets Must Never Be Printed

Secrets must be masked in logs, exceptions, reports, and generated documentation.

## BR-F003 — Generated Code Must Be Security Reviewed

Security agent review is required before export.

---

# 9. Evaluation Rules

## BR-G001 — Evaluation Is Mandatory

Every generated artifact must pass an evaluation gate appropriate to its type.

## BR-G002 — Failed Evaluation Triggers Refinement

Failed evaluation must produce a refinement task, not a silent warning.

## BR-G003 — Evaluation Reports Must Be Persisted

Reports must be stored under project evaluation history.

---

# 10. Testing Rules

## BR-H001 — Tests Are Part of Every Milestone

A milestone is not complete without tests.

## BR-H002 — No Fake Tests

Tests must assert behavior, not only import modules.

## BR-H003 — Minimum Test Types

Required test categories:

- unit,
- integration,
- workflow,
- security,
- evaluation.

---

# 11. Documentation Rules

## BR-I001 — Public Components Need Documentation

Every public component must document:

- purpose,
- inputs,
- outputs,
- errors,
- examples.

## BR-I002 — Architecture Changes Require ADRs

Any deviation from the architecture package requires an Architecture Decision Record.

---

# 12. Stop Conditions

Stop implementation when:

- tests fail,
- architecture boundary is unclear,
- security policy denies an action,
- required context is missing,
- user approval is required,
- implementation would require changing a major architecture decision.
