# GEMINI_PROJECT_GUIDE.md

Project: AgentForge  
Purpose: Gemini and ADK-aligned implementation guidance

---

# 1. Purpose

This guide explains how AgentForge should use Gemini and Google ADK-aligned concepts without coupling the entire codebase directly to one framework API.

The implementation should use an adapter layer so AgentForge remains portable and testable.

---

# 2. Model Usage Principles

Use Gemini models through a model client port.

Required abstraction:

```text
Application Service
  ↓
ModelClientPort
  ↓
GeminiModelClient Adapter
```

Do not call Gemini directly from domain entities, workflow nodes, or agent business logic.

---

# 3. Recommended Model Routing

Use model selection by task type.

| Task Type | Recommended Model Class |
|---|---|
| planning | reasoning-capable model |
| architecture | reasoning-capable model |
| code generation | strong coding model |
| summarization | fast model |
| classification | fast model |
| evaluation | reasoning-capable model |
| security review | reasoning-capable model |

Model names should be configurable.

---

# 4. ADK-Aligned Concepts

AgentForge should align with these concepts:

- agents as autonomous task units,
- tools as callable capabilities,
- sessions/state for conversational and workflow context,
- memory for long-term knowledge,
- callbacks/policies for governance,
- evaluation for quality validation,
- deployment-ready agent services.

---

# 5. Agent Adapter Rule

Built-in AgentForge agents may be wrapped by ADK agents, but internal business logic must remain framework-independent where possible.

Recommended shape:

```text
AgentForge Agent Plugin
  ↓
Agent Runtime Adapter
  ↓
ADK Agent / Runner / Tooling
```

This avoids rewriting core architecture if framework APIs change.

---

# 6. Prompt Construction

Prompts must be generated from structured context packs.

Prompt inputs:

- system role,
- task objective,
- constraints,
- relevant architecture decisions,
- required output schema,
- available tools,
- memory excerpts,
- evaluation rubric.

Do not insert raw untrusted external content without security inspection.

---

# 7. Structured Output

Whenever possible, agents should return structured outputs using schemas.

Required fields:

- `status`,
- `summary`,
- `artifacts`,
- `decisions`,
- `warnings`,
- `errors`,
- `confidence`,
- `next_actions`.

---

# 8. Tool Usage

Tools must be exposed through AgentForge's Tool Gateway.

Tool usage flow:

```text
Agent Request
  ↓
Tool Gateway
  ↓
Security Policy
  ↓
Tool Adapter or MCP Adapter
  ↓
Audit Log
  ↓
Structured Tool Result
```

---

# 9. Memory Usage

Memory should be mapped to ADK concepts where useful, but AgentForge owns its memory architecture.

Use:

- session state for active workflow context,
- project memory for persistent project decisions,
- knowledge memory for reusable engineering patterns,
- artifact store for generated outputs.

---

# 10. Evaluation

AgentForge must support evaluation at multiple levels:

- agent output evaluation,
- workflow evaluation,
- generated code evaluation,
- security evaluation,
- final submission evaluation.

Evaluation reports should be saved and used for refinement.

---

# 11. Local Development Modes

Recommended modes:

| Mode | Purpose |
|---|---|
| `mock` | tests without live model calls |
| `local` | local development with live API |
| `demo` | controlled capstone demo |
| `ci` | no external calls unless explicitly allowed |
| `production` | strict approval and security rules |

---

# 12. API Key Handling

Rules:

- read keys from environment,
- mask keys in logs,
- never write keys to generated artifacts,
- never include keys in prompts,
- never commit `.env`.

---

# 13. Capstone Demonstration Guidance

The demo should clearly show:

1. Natural-language project intake.
2. Planner decomposing work.
3. Multiple agents collaborating.
4. Tool use through MCP/gateway.
5. Memory preserving decisions.
6. Human approval gate.
7. Security review.
8. Evaluation report.
9. Final generated project export.

This is stronger than showing only code generation.
