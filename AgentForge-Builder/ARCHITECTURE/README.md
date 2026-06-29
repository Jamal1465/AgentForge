# ARCHITECTURE Package Index

**Project:** AgentForge  
**Package:** Architecture Specification Package  
**Status:** Draft for Implementation  
**Last Updated:** June 2026  

This folder contains the implementation-facing architecture specifications for AgentForge.

## Files

| File | Purpose |
|---|---|
| `05_System_Architecture.md` | Master system architecture for AgentForge as an AI Software Engineering Operating System. |
| `06_Agent_Architecture.md` | Agent plugin contracts, specialist agents, routing, prompt boundaries, and permissions. |
| `07_Workflow_Architecture.md` | Workflow graph model, execution states, approval gates, retries, loops, and orchestration. |
| `08_Memory_Architecture.md` | Session memory, project memory, artifact store, decision log, and context pack strategy. |
| `09_MCP_Architecture.md` | MCP/tool gateway, tool policy, permission matrix, audit logging, and adapters. |
| `10_Security_Architecture.md` | Threat model, prompt-injection defense, secrets, tool safety, audit, and security gates. |
| `11_Evaluation_Architecture.md` | Evaluation gates, rubrics, test execution, quality reports, and refinement policy. |

## Implementation Rule

The coding assistant must read `05_System_Architecture.md` first, then read the specialized architecture document relevant to the current implementation task.

No source code should be generated unless it conforms to these architecture documents.
