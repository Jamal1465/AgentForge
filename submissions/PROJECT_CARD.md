# Project Card — AgentForge

## Project Name

AgentForge

## One-Line Summary

AgentForge is a capability-first AI Software Engineering Operating System that orchestrates plugin agents to plan, govern, evaluate, and package software engineering workflows.

## Problem

Most AI coding assistants work well for isolated prompts but struggle with full software engineering workflows. They often lack explicit planning, durable context, security review, evaluation, observability, and extension boundaries.

## Solution

AgentForge provides a platform runtime where engineering capabilities are added as plugins. The Planner does not know concrete agent names. It asks for capabilities such as `api-development`, `data-modeling`, `security-analysis`, `quality-assurance`, or `technical-documentation`. The Agent Registry and Capability Router select the best compatible plugin at runtime.

## Key Differentiator

AgentForge is not a fixed multi-agent demo. It is a plugin-based AI engineering platform. The orchestration core remains stable while new engineering capabilities can be added independently.

## Implemented Milestones

| Milestone | Status |
|---|---|
| 01 Project Foundation | Complete |
| 02 Repository Scaffold | Complete |
| 03 Core Domain Models | Complete |
| 04 Plugin Registry | Complete |
| 05 Workflow Engine | Complete |
| 06 Memory System | Complete |
| 07 MCP Tool Integration Boundary | Complete |
| 08 Security Layer | Complete |
| 09 Evaluation Framework | Complete |
| 10 Observability and Telemetry | Complete |
| 11 Interfaces and Deployment | Complete |
| 12 Submission Package | Complete |

## Current Technical Scope

The current implementation is a clean, tested vertical slice. It focuses on platform architecture and runtime governance rather than pretending to generate a full production app in one command.

## Validation Evidence

- `pytest`: passing
- Python compilation: passing
- CLI health command: passing
- CLI readiness command: passing
- CLI project creation demo: passing

## Future Expansion

Future plugins can implement capabilities such as:

- `api-development`,
- `ui-development`,
- `mobile-development`,
- `data-modeling`,
- `infrastructure`,
- `security-analysis`,
- `quality-assurance`,
- `technical-documentation`,
- `research`,
- `code-review`.
