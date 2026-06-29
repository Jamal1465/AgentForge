# TestingRules.md

Purpose: Rules for generating tests in AgentForge.

---

# 1. Tests Must Assert Behavior

Do not create tests that only import modules.

Bad:

```python
def test_imports():
    import agentforge
```

Good:

```python
def test_router_returns_no_route_when_no_agent_matches():
    result = router.route(task)
    assert result.status == "no_route"
```

---

# 2. Required Test Categories

- unit tests for domain and policies,
- integration tests for adapters,
- workflow tests for state transitions,
- security tests for denied actions,
- evaluation tests for quality gates.

---

# 3. No Live API Calls In Unit Tests

Unit tests must not call live Gemini, MCP, GitHub, or network APIs.

Use fake ports and deterministic fixtures.

---

# 4. Test Naming

Use descriptive names:

```text
test_<component>_<condition>_<expected_behavior>
```

---

# 5. Coverage Priority

Prioritize:

1. workflow state transitions,
2. plugin routing,
3. security permission decisions,
4. memory scope isolation,
5. evaluation gate failures.
