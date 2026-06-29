from __future__ import annotations

import pytest

from agentforge.application.platform import AgentForgePlatform
from agentforge.infrastructure.config import AgentForgeSettings, RuntimeEnvironment
from agentforge.interfaces.api.handlers import (
    create_project_handler,
    get_project_handler,
    health_handler,
    list_plugins_handler,
    readiness_handler,
)
from agentforge.interfaces.api.schemas import ApiValidationError


def build_platform() -> AgentForgePlatform:
    return AgentForgePlatform.create_default(
        settings=AgentForgeSettings(environment=RuntimeEnvironment.TEST)
    )


def test_health_and_readiness_handlers_return_plain_dicts() -> None:
    platform = build_platform()

    assert health_handler(platform)["status"] == "ok"
    assert readiness_handler(platform)["status"] == "ready"


def test_create_project_handler_runs_workflow() -> None:
    platform = build_platform()
    result = create_project_handler({"description": "Build an LMS"}, platform)

    assert result["status"] == "completed"
    assert "plan" in result["executed_node_ids"]
    assert "01_project_brief" in result["executed_node_ids"]
    assert len(result["executed_node_ids"]) == 11

    # Test get_project_handler
    workflow_id = result["workflow_id"]
    proj_details = get_project_handler(workflow_id, platform)
    assert proj_details["workflow_id"] == workflow_id
    assert proj_details["status"] == "completed"
    assert len(proj_details["artifacts"]) > 0
    assert len(proj_details["events"]) > 0

    # Test list_plugins_handler
    plugins_data = list_plugins_handler(platform)
    assert "plugins" in plugins_data
    assert "capability_map" in plugins_data
    assert len(plugins_data["plugins"]) > 0


def test_create_project_handler_validates_payload() -> None:
    with pytest.raises(ApiValidationError):
        create_project_handler({"description": ""}, build_platform())


def test_get_project_handler_not_found() -> None:
    with pytest.raises(ApiValidationError):
        get_project_handler("non-existent-id", build_platform())
