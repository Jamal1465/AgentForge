# Expected Demo Workflow

The current milestone implements a deterministic planning vertical slice. The expected execution flow is:

```text
User Request
   ↓
CLI/API Handler
   ↓
AgentForgePlatform Composition Root
   ↓
Workflow Engine
   ↓
Security Service
   ↓
Capability Router
   ↓
Agent Registry
   ↓
Registered Planner Plugin
   ↓
Evaluation Service
   ↓
Observability Service
   ↓
Final Workflow Response
```

## Expected Result

The workflow should complete successfully and return:

- a workflow id,
- a completed status,
- executed node ids,
- structured telemetry events,
- security decision events,
- evaluation pass events.

## What This Proves

This demo proves that AgentForge has a working capability-first orchestration spine:

- the interface layer does not call plugin implementations directly,
- the workflow engine owns execution state,
- security checks happen before plugin execution,
- plugin selection is routed through the registry and matcher,
- evaluation runs after plugin execution,
- observability records the execution path.
