# BuilderRules.md

Purpose: Rules for AI coding assistants implementing AgentForge.

---

# 1. Always Start With Context

Before implementation, read:

- `00_READ_FIRST.md`
- `AI_CONTEXT.md`
- `BUILD_RULES.md`
- current milestone
- related architecture document

---

# 2. Smallest Correct Change

Implement the smallest coherent change that moves the milestone forward.

Do not generate unrelated modules.
Do not perform broad rewrites.
Do not change public APIs without reason.

---

# 3. Output Format

When reporting work, include:

- files changed,
- architecture components affected,
- tests added,
- commands run,
- known limitations.

---

# 4. Required Behavior

- preserve architecture boundaries,
- add tests with code,
- use typed Python,
- avoid placeholders,
- update documentation when contracts change,
- stop on failing quality gates.

---

# 5. Forbidden Behavior

Never:

- skip tests,
- hardcode agent routing,
- bypass tool gateway,
- ignore security policy,
- commit secrets,
- fake successful execution,
- claim unrun tests passed.
