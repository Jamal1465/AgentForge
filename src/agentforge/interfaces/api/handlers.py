"""Framework-independent API handlers for AgentForge.

HTTP adapters and tests call these functions directly. The handlers return plain
Python dictionaries so the API boundary remains decoupled from FastAPI, Flask, or
stdlib HTTP servers.
"""

from __future__ import annotations

import os

from agentforge.application.platform import AgentForgePlatform
from agentforge.interfaces.api.schemas import ApprovalRequest, CreateProjectRequest


def health_handler(platform: AgentForgePlatform) -> dict[str, object]:
    """Return liveness payload."""
    return platform.health().to_dict()


def readiness_handler(platform: AgentForgePlatform) -> dict[str, object]:
    """Return readiness payload."""
    return platform.readiness().to_dict()


def create_project_handler(
    payload: dict[str, object],
    platform: AgentForgePlatform,
) -> dict[str, object]:
    """Create and execute a planning workflow from a JSON-like payload."""
    request = CreateProjectRequest.from_payload(payload)
    return platform.run_project_request(request.description).to_dict()


def approve_workflow_handler(
    payload: dict[str, object],
    platform: AgentForgePlatform,
) -> dict[str, object]:
    """Approve or reject a paused workflow node."""
    request = ApprovalRequest.from_payload(payload)
    return platform.approve_workflow(
        workflow_id=request.workflow_id,
        node_id=request.node_id,
        approved=request.approved,
    ).to_dict()


def get_project_handler(
    workflow_id: str,
    platform: AgentForgePlatform,
) -> dict[str, object]:
    """Retrieve details and generated files for a given workflow ID."""
    try:
        workflow = platform.workflow_store.get(workflow_id)
    except Exception as exc:
        from agentforge.interfaces.api.schemas import ApiValidationError
        raise ApiValidationError(f"Workflow not found: {workflow_id}") from exc

    output_dir = os.path.join("generated_projects", workflow_id)
    artifacts = []
    if os.path.isdir(output_dir):
        for name in sorted(os.listdir(output_dir)):
            if name.endswith(".md"):
                file_path = os.path.join(output_dir, name)
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                artifacts.append({"name": name, "content": content})

    events = [
        {
            "event_type": event.event_type,
            "message": event.message,
            "node_id": event.node_id,
        }
        for event in workflow.events
    ]

    eval_reports = []
    if (
        platform.evaluation_service is not None
        and platform.evaluation_service.store is not None
    ):
        try:
            reports = platform.evaluation_service.store.list_by_workflow(workflow_id)
            for r in reports:
                eval_reports.append({
                    "report_id": r.report_id,
                    "status": r.status.value,
                    "score": r.overall_score,
                    "findings": [
                        {
                            "criterion_id": f.criterion_id or "",
                            "message": f.message,
                            "severity": f.severity.value,
                        }
                        for f in r.findings
                    ],
                })
        except Exception:
            pass

    security_events = []
    if (
        platform.security_service is not None
        and platform.security_service.audit_store is not None
    ):
        try:
            events_list = platform.security_service.audit_store.list_events()
            for e in events_list:
                security_events.append({
                    "event_type": e.event_type,
                    "subject_id": e.subject_id,
                    "actor_id": e.actor_id,
                    "decision_status": e.decision_status.value,
                    "message": e.message,
                    "finding_ids": e.finding_ids,
                })
        except Exception:
            pass

    is_completed = any(e["event_type"] == "workflow.completed" for e in events)
    status = "completed" if is_completed else "running"

    return {
        "workflow_id": workflow_id,
        "status": status,
        "events": events,
        "artifacts": artifacts,
        "evaluations": eval_reports,
        "security_events": security_events,
        "output_path": f"generated_projects/{workflow_id}" if is_completed else None,
    }


def list_plugins_handler(platform: AgentForgePlatform) -> dict[str, object]:
    """Retrieve all registered plugins and capability routing map."""
    plugins = []
    capability_map: dict[str, list[str]] = {}
    for plugin in platform.registry.list_agents():
        plugin_info = {
            "agent_id": plugin.metadata.agent_id,
            "name": plugin.metadata.name,
            "version": plugin.metadata.version,
            "risk_level": plugin.metadata.risk_level.value,
            "capabilities": [c.name for c in plugin.metadata.capabilities],
        }
        plugins.append(plugin_info)
        for c in plugin.metadata.capabilities:
            if c.name not in capability_map:
                capability_map[c.name] = []
            capability_map[c.name].append(plugin.metadata.agent_id)

    return {
        "plugins": plugins,
        "capability_map": capability_map,
    }


def get_generated_files_handler(
    workflow_id: str,
    platform: AgentForgePlatform,
) -> dict[str, object]:
    """Retrieve list of all generated files for a given workflow ID."""
    try:
        platform.workflow_store.get(workflow_id)
    except Exception as exc:
        from agentforge.interfaces.api.schemas import ApiValidationError
        raise ApiValidationError(f"Workflow not found: {workflow_id}") from exc

    output_dir = os.path.join("generated_projects", workflow_id)
    files = []
    if os.path.isdir(output_dir):
        for root, _dirs, filenames in os.walk(output_dir):
            for name in filenames:
                file_path = os.path.join(root, name)
                rel_path = os.path.relpath(file_path, output_dir)
                rel_path_standard = rel_path.replace(os.sep, "/")
                files.append({
                    "name": name,
                    "path": rel_path_standard,
                    "size_bytes": os.path.getsize(file_path),
                })

    return {
        "workflow_id": workflow_id,
        "files": sorted(files, key=lambda x: str(x["path"])),
    }


def get_generated_file_content_handler(
    workflow_id: str,
    filename: str,
    platform: AgentForgePlatform,
) -> dict[str, object]:
    """Retrieve content of a specific generated file."""
    try:
        platform.workflow_store.get(workflow_id)
    except Exception as exc:
        from agentforge.interfaces.api.schemas import ApiValidationError
        raise ApiValidationError(f"Workflow not found: {workflow_id}") from exc

    output_dir = os.path.abspath(os.path.join("generated_projects", workflow_id))
    target_path = os.path.abspath(os.path.join(output_dir, filename))
    if not target_path.startswith(output_dir):
        from agentforge.interfaces.api.schemas import ApiValidationError
        raise ApiValidationError("Access denied: Invalid filename path.")

    if not os.path.isfile(target_path):
        from agentforge.interfaces.api.schemas import ApiValidationError
        raise ApiValidationError(f"File not found: {filename}")

    try:
        with open(target_path, encoding="utf-8") as f:
            content = f.read()
    except Exception as exc:
        from agentforge.interfaces.api.schemas import ApiValidationError
        raise ApiValidationError(f"Could not read file: {filename}") from exc

    return {
        "workflow_id": workflow_id,
        "filename": filename,
        "content": content,
    }


def list_capabilities_handler(platform: AgentForgePlatform) -> dict[str, object]:
    """Retrieve all unique capabilities registered in the agent registry."""
    capabilities = set()
    for plugin in platform.registry.list_agents():
        for cap in plugin.metadata.capabilities:
            capabilities.add(cap.name)
    return {
        "capabilities": sorted(list(capabilities)),
    }


def list_events_handler(
    platform: AgentForgePlatform,
    workflow_id: str | None = None,
) -> dict[str, object]:
    """Retrieve telemetry events, optionally filtered by workflow/trace ID."""
    events = platform.observability_service.store.list_events(trace_id=workflow_id)
    serialized = []
    for e in events:
        serialized.append({
            "event_id": e.event_id,
            "name": e.name,
            "event_type": e.event_type.value,
            "severity": e.severity.value,
            "message": e.message,
            "trace_id": e.trace_id,
            "workflow_id": e.workflow_id,
            "node_id": e.node_id,
            "agent_id": e.agent_id,
            "tool_id": e.tool_id,
            "metadata": e.metadata,
            "timestamp": e.timestamp.isoformat(),
        })
    return {
        "events": serialized,
    }


def list_projects_handler(platform: AgentForgePlatform) -> dict[str, object]:
    """List all generated projects/workflows."""
    import os
    import re
    from datetime import UTC, datetime
    from typing import Any

    projects: list[dict[str, Any]] = []
    seen_ids = set()

    # 1. Scan the generated_projects folder on disk
    output_base_dir = "generated_projects"
    if os.path.isdir(output_base_dir):
        for workflow_id in os.listdir(output_base_dir):
            output_dir = os.path.join(output_base_dir, workflow_id)
            if not os.path.isdir(output_dir):
                continue

            seen_ids.add(workflow_id)
            project_name = "Generated Project"
            mtime_float = os.path.getmtime(output_dir)

            # Try to read the actual project name from 01_Project_Brief.md
            brief_path = os.path.join(output_dir, "01_Project_Brief.md")
            if os.path.isfile(brief_path):
                try:
                    mtime_float = os.path.getmtime(brief_path)
                    with open(brief_path, encoding="utf-8") as f:
                        for line in f:
                            if "project name:" in line.lower():
                                parts = line.split(":", 1)
                                if len(parts) > 1:
                                    project_name = parts[1].strip()
                                    project_name = re.sub(r'[*`#_]', '', project_name)
                                    break
                except Exception:
                    pass

            # Gather generated files
            files = []
            for name in sorted(os.listdir(output_dir)):
                if name.endswith(".md"):
                    file_path = os.path.join(output_dir, name)
                    files.append({
                        "name": name,
                        "size_bytes": os.path.getsize(file_path),
                    })

            # Check if workflow exists in memory to get correct status
            status = "completed"
            try:
                workflow = platform.workflow_store.get(workflow_id)
                events = workflow.events
                is_completed = any(e.event_type == "workflow.completed" for e in events)
                status = "completed" if is_completed else "running"
            except Exception:
                pass

            iso_timestamp = datetime.fromtimestamp(mtime_float, tz=UTC).isoformat()
            projects.append({
                "workflow_id": workflow_id,
                "project_name": project_name,
                "status": status,
                "files": files,
                "timestamp": iso_timestamp,
            })

    # 2. Also check any running workflows in memory that might not have files yet
    if hasattr(platform.workflow_store, "_workflows"):
        for workflow_id, workflow in platform.workflow_store._workflows.items():
            if workflow_id in seen_ids:
                continue

            project_name = "Generated Project"
            events = workflow.events
            is_completed = any(e.event_type == "workflow.completed" for e in events)
            status = "completed" if is_completed else "running"
            now_iso = datetime.now(tz=UTC).isoformat()

            projects.append({
                "workflow_id": workflow_id,
                "project_name": project_name,
                "status": status,
                "files": [],
                "timestamp": now_iso,
            })

    projects.sort(key=lambda x: str(x["timestamp"]), reverse=True)
    return {"projects": projects}



