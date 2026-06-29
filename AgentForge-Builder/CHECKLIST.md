# CHECKLIST.md

Project: AgentForge  
Purpose: Master build and submission checklist

---

# 1. Documentation Checklist

- [ ] `00_READ_FIRST.md` reviewed
- [ ] `AI_CONTEXT.md` reviewed
- [ ] `BUILD_RULES.md` reviewed
- [ ] `CODING_STANDARDS.md` reviewed
- [ ] Architecture package reviewed
- [ ] Current milestone reviewed
- [ ] README updated
- [ ] Demo guide prepared
- [ ] Submission writeup prepared

---

# 2. Architecture Checklist

- [ ] Clean Architecture boundaries enforced
- [ ] Domain has no framework imports
- [ ] Ports exist before adapters
- [ ] Plugin architecture implemented
- [ ] Agent registry implemented
- [ ] Capability routing implemented
- [ ] Explicit workflow graph implemented
- [ ] Memory scopes implemented
- [ ] Tool gateway implemented
- [ ] Security policy implemented
- [ ] Evaluation gates implemented

---

# 3. Agent Checklist

For every agent:

- [ ] Metadata defined
- [ ] Capabilities declared
- [ ] Required tools declared
- [ ] Input schema defined
- [ ] Output schema defined
- [ ] Execution result structured
- [ ] Tests written
- [ ] Logging included
- [ ] Tool access goes through gateway
- [ ] Evaluation hints included

---

# 4. Workflow Checklist

- [ ] Workflow definitions are explicit
- [ ] State transitions validated
- [ ] Retry policy implemented
- [ ] Human approval state implemented
- [ ] Failure state implemented
- [ ] Persistence implemented
- [ ] Audit events generated
- [ ] Workflow tests pass

---

# 5. Memory Checklist

- [ ] Request memory implemented
- [ ] Session memory implemented
- [ ] Project memory implemented
- [ ] Decision log implemented
- [ ] Artifact store implemented
- [ ] Context pack builder implemented
- [ ] Memory safety tests pass

---

# 6. Tool and MCP Checklist

- [ ] Tool registry implemented
- [ ] Tool gateway implemented
- [ ] Tool policy implemented
- [ ] MCP adapter implemented
- [ ] Filesystem tool implemented
- [ ] Git tool implemented
- [ ] Python execution tool implemented
- [ ] Audit log implemented
- [ ] Permission tests pass

---

# 7. Security Checklist

- [ ] Prompt injection scanner implemented
- [ ] Secret masking implemented
- [ ] Workspace boundary checks implemented
- [ ] High-risk approval gate implemented
- [ ] Generated code security review implemented
- [ ] Security tests pass

---

# 8. Evaluation Checklist

- [ ] Evaluation report model implemented
- [ ] Architecture gate implemented
- [ ] Code gate implemented
- [ ] Security gate implemented
- [ ] Documentation gate implemented
- [ ] Submission gate implemented
- [ ] Failed evaluations trigger refinement

---

# 9. Quality Checklist

- [ ] `uv sync` works
- [ ] `ruff check` passes
- [ ] formatter check passes
- [ ] type check passes
- [ ] unit tests pass
- [ ] integration tests pass
- [ ] workflow tests pass
- [ ] security tests pass
- [ ] evaluation tests pass

---

# 10. Submission Checklist

- [ ] GitHub repository clean
- [ ] README polished
- [ ] Demo script ready
- [ ] Demo video recorded
- [ ] Architecture diagrams included
- [ ] Evaluation results included
- [ ] Security explanation included
- [ ] Capstone writeup complete
- [ ] Final ZIP/package created
