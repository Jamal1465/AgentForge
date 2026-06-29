# ReviewRules.md

Purpose: Rules for reviewing AgentForge changes.

---

# 1. Review Order

Review every change in this order:

1. architecture boundary,
2. correctness,
3. security,
4. tests,
5. maintainability,
6. documentation.

---

# 2. Architecture Review

Check:

- domain purity,
- dependency direction,
- port/adapter separation,
- plugin-first design,
- workflow explicitness.

---

# 3. Security Review

Check:

- no hardcoded secrets,
- risky tools behind policy,
- workspace boundaries enforced,
- prompt injection handled,
- logs mask sensitive data.

---

# 4. Test Review

Check:

- tests assert behavior,
- failure cases covered,
- no live API calls in unit tests,
- no fake success.

---

# 5. Review Output

Report:

- approved items,
- blocking issues,
- non-blocking improvements,
- required fixes before merge.
