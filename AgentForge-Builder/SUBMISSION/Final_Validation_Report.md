# Final Validation Report

Generated: 2026-06-28T00:44:17.515360+00:00

## Validation Commands

```bash
python -m pytest -q
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m agentforge.interfaces.cli.main health
PYTHONPATH=src python -m agentforge.interfaces.cli.main ready
PYTHONPATH=src python -m agentforge.interfaces.cli.main create "Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and technical documentation" --json
```

## Result

All validation commands passed.

## Details

### pytest

Return code: `0`

```text
........................................................................ [ 73%]
..........................                                               [100%]
98 passed in 0.27s
```
### compileall

Return code: `0`

```text

```
### health

Return code: `0`

```text
{
  "details": {
    "environment": "local"
  },
  "registered_plugins": 1,
  "service": "AgentForge",
  "status": "ok",
  "version": "0.1.0"
}
```
### ready

Return code: `0`

```text
{
  "details": {
    "planning_capability": "true"
  },
  "registered_plugins": 1,
  "service": "AgentForge",
  "status": "ready",
  "version": "0.1.0"
}
```
### create_demo

Return code: `0`

```text
{
  "error": null,
  "events": [
    {
      "event_type": "workflow.started",
      "message": "Workflow execution started.",
      "node_id": null
    },
    {
      "event_type": "node.started",
      "message": "Workflow node execution started.",
      "node_id": "plan"
    },
    {
      "event_type": "security.allow",
      "message": "Task passed security policy.",
      "node_id": "plan"
    },
    {
      "event_type": "node.agent_result",
      "message": "Generated initial deterministic project plan.",
      "node_id": "plan"
    },
    {
      "event_type": "evaluation.passed",
      "message": "Evaluation score=0.95; report=2b5f2bfb-eec8-407f-89be-05cbb81e9511",
      "node_id": "plan"
    },
    {
      "event_type": "node.completed",
      "message": "Workflow node completed successfully.",
      "node_id": "plan"
    },
    {
      "event_type": "workflow.completed",
      "message": "Workflow execution completed.",
      "node_id": null
    }
  ],
  "executed_node_ids": [
    "plan"
  ],
  "pending_approval_node_id": null,
  "status": "completed",
  "workflow_id": "9b4092b9-8cec-4629-8218-ce4978750fdf"
}
```
