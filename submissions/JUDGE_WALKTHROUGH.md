# Judge Walkthrough

## Fast Path Review

1. Open `README.md`.
2. Review the capability-first architecture diagram.
3. Run `python -m pytest -q`.
4. Run the main CLI demo.
5. Inspect `submissions/KAGGLE_SUBMISSION.md`.
6. Inspect `src/agentforge/runtime/registry/agent_registry.py`.
7. Inspect `src/agentforge/runtime/routing/capability_router.py`.
8. Inspect `src/agentforge/application/workflows/runner.py`.
9. Inspect `src/agentforge/application/security/service.py`.
10. Inspect `src/agentforge/application/evaluation/service.py`.

## What to Look For

AgentForge is intentionally architected as a platform foundation. The important technical merit is not a hardcoded demo chain, but the separation of:

- planning,
- routing,
- plugin registration,
- workflow execution,
- security,
- evaluation,
- observability,
- interface/deployment.
