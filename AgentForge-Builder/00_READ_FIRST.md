# 00_READ_FIRST.md

Project: AgentForge  
Version: 1.0.0  
Status: Builder Kit Active  
Purpose: Single entry point for human developers and AI coding assistants

---

# 1. What This Project Is

AgentForge is an AI Software Engineering Operating System built on top of Google Agent Development Kit concepts. It coordinates specialized software-engineering agents that transform a natural-language project idea into a planned, implemented, tested, evaluated, documented, and exportable software project.

AgentForge is not a simple chatbot, single prompt, or one-file coding assistant. It is a plugin-first multi-agent platform with explicit workflows, shared memory, tool governance, human approval gates, evaluation loops, and production-oriented engineering standards.

---

# 2. How To Use This Builder Kit

This Builder Kit is the source of truth for building AgentForge. An AI coding assistant must read the documents in the required order before writing implementation code.

Required reading order:

1. `00_READ_FIRST.md`
2. `AI_CONTEXT.md`
3. `BUILD_RULES.md`
4. `CODING_STANDARDS.md`
5. `ARCHITECTURE/05_System_Architecture.md`
6. `ARCHITECTURE/06_Agent_Architecture.md`
7. `ARCHITECTURE/07_Workflow_Architecture.md`
8. `ARCHITECTURE/08_Memory_Architecture.md`
9. `ARCHITECTURE/09_MCP_Architecture.md`
10. `ARCHITECTURE/10_Security_Architecture.md`
11. `ARCHITECTURE/11_Evaluation_Architecture.md`
12. `agent_builder_playbook.md`
13. `IMPLEMENTATION/README.md`
14. The current milestone file only

Do not begin coding before this sequence is complete.

---

# 3. Non-Negotiable Architecture Decisions

The implementation must preserve these decisions:

- AgentForge uses a plugin-first agent architecture.
- The orchestrator must not hardcode individual agents.
- Agents must declare capabilities.
- Workflows must be explicit graph definitions.
- Human approval gates must exist for risky actions.
- Tool access must pass through a gateway and policy layer.
- Memory must be structured, scoped, and auditable.
- Evaluation is part of the runtime, not a final manual step.
- Security checks must happen before tool execution and before artifact export.
- Tests must be generated with every implementation milestone.

---

# 4. Build Philosophy

AgentForge must be built like a real production software platform.

The expected engineering order is:

1. Understand requirements.
2. Validate architecture.
3. Create a small runnable scaffold.
4. Implement one vertical slice.
5. Add tests.
6. Run checks.
7. Refactor only after tests pass.
8. Continue to the next milestone.

Never generate large disconnected code dumps.

---

# 5. Definition of Clean Build

A clean build means:

- The repository installs from a clean environment.
- Imports resolve.
- Type checks pass or have documented exceptions.
- Unit tests pass.
- Integration tests relevant to the milestone pass.
- No broken placeholder implementations exist.
- Public APIs are documented.
- Generated files match the architecture package.

---

# 6. What To Do First

For a new coding assistant session:

1. Read this file.
2. Summarize the project in 5 lines.
3. Identify the current milestone.
4. Inspect existing files.
5. Propose the smallest safe next change.
6. Implement only that change.
7. Run validation.
8. Report results.

---

# 7. Forbidden Behavior

Do not:

- Rewrite the architecture without explicit approval.
- Replace the plugin architecture with hardcoded if/else routing.
- Skip security gates.
- Skip evaluation gates.
- Create fake tests that do not assert behavior.
- Add TODO-only modules.
- Use `pass` as a final implementation.
- Hide errors.
- Continue building new features while tests are failing.
- Store secrets in source code.

---

# 8. Builder Kit Packages

Current package status:

| Package | Status |
|---|---|
| Architecture Package | Generated |
| Builder Pack | Generated |
| Implementation Milestones | Generated |
| Prompt Rules | Generated |
| Source Scaffold | Next |
| Submission Pack | Later |

---

# 9. Target Outcome

The final repository should allow a user to run a command similar to:

```bash
agentforge create "Build a FastAPI CRM with React and PostgreSQL"
agentforge plan --project crm
agentforge run --project crm
agentforge evaluate --project crm
agentforge export --project crm
```

The system should generate a secure, tested, documented, deployable project through multi-agent collaboration.
