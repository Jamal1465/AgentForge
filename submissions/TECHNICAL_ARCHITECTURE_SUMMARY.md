# Technical Architecture Summary

## Architecture Style

AgentForge uses Clean Architecture with plugin-first runtime boundaries.

```text
Domain Layer
   ↑
Application Layer
   ↑
Runtime Layer
   ↑
Infrastructure Layer
   ↑
Interface Layer
```

## Core Runtime

| Component | Responsibility |
|---|---|
| AgentForgePlatform | Composition root |
| Workflow Engine | Executes workflow graphs |
| Agent Registry | Stores registered plugins |
| Capability Router | Matches tasks to plugin capabilities |
| Memory Service | Stores and retrieves project/workflow/agent memory |
| Tool Registry | Stores safe tool adapters |
| Security Service | Applies policies before risky execution |
| Evaluation Service | Scores outputs and applies quality gates |
| Observability Service | Emits events, metrics, and trace spans |

## Capability-First Rule

The core platform must not depend on concrete agent names.

Allowed:

```text
capability = api-development
capability = security-analysis
capability = technical-documentation
```

Avoid in core orchestration:

```text
BackendAgent
FrontendAgent
DatabaseAgent
DevOpsAgent
```

## Plugin Contract

A plugin advertises metadata and capabilities. The registry stores the plugin. The router matches a workflow task to a compatible plugin.

```text
Plugin Metadata
   ↓
Capabilities
   ↓
Registry
   ↓
Router
   ↓
Workflow Execution
```

## Security Boundary

Security policies are attached to:

- prompt content,
- required capability,
- plugin trust metadata,
- tool risk metadata,
- destructive operation flags.

## Evaluation Boundary

Evaluation is independent of fixed agent roles. It evaluates subjects such as:

- workflow result,
- plugin result,
- generated artifact,
- tool result.

## Observability Boundary

Telemetry records platform events such as:

- workflow started,
- node started,
- security allowed/blocked,
- routing decision,
- plugin execution success/failure,
- evaluation passed/failed,
- workflow completed.
