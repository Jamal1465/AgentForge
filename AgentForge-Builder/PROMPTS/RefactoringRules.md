# RefactoringRules.md

Purpose: Rules for safe refactoring.

---

# 1. Refactor Only With Passing Tests

Do not refactor while tests are failing unless the refactor directly fixes the failure.

---

# 2. Preserve Public Contracts

Public interfaces, schemas, CLI commands, and documented behaviors must remain stable unless a milestone explicitly changes them.

---

# 3. Refactor Goals

Allowed goals:

- reduce duplication,
- improve boundaries,
- simplify dependencies,
- improve testability,
- improve naming,
- remove dead code.

---

# 4. Required Validation

After refactoring, run:

```bash
uv run ruff check .
uv run pytest
```

Run type checks when signatures changed.

---

# 5. Refactoring Report

Explain:

- what changed,
- why it changed,
- which behavior stayed the same,
- which tests prove safety.
