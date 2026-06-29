from __future__ import annotations

from agentforge.application.platform import AgentForgePlatform
from agentforge.infrastructure.config import AgentForgeSettings, RuntimeEnvironment


def test_default_platform_is_healthy_and_ready() -> None:
    platform = AgentForgePlatform.create_default(
        settings=AgentForgeSettings(environment=RuntimeEnvironment.TEST)
    )

    assert platform.health().status == "ok"
    assert platform.readiness().status == "ready"
    assert platform.health().registered_plugins >= 1


def test_platform_runs_project_request_through_workflow() -> None:
    platform = AgentForgePlatform.create_default(
        settings=AgentForgeSettings(environment=RuntimeEnvironment.TEST)
    )

    summary = platform.run_project_request("Build a FastAPI task manager")

    assert summary.status == "completed"
    assert "plan" in summary.executed_node_ids
    assert "01_project_brief" in summary.executed_node_ids
    assert len(summary.executed_node_ids) == 11
    assert summary.workflow_id
    assert any(event["event_type"] == "workflow.completed" for event in summary.events)
