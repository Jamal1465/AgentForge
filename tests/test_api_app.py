from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from agentforge.application.platform import AgentForgePlatform
from agentforge.infrastructure.config import AgentForgeSettings, RuntimeEnvironment
from agentforge.interfaces.api.app import create_app


@pytest.fixture
def test_client() -> TestClient:
    settings = AgentForgeSettings(environment=RuntimeEnvironment.TEST)
    platform = AgentForgePlatform.create_default(settings=settings)
    app = create_app(platform)
    return TestClient(app)


def test_fastapi_health_ready(test_client: TestClient) -> None:
    # Test health
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    # Test readiness
    response = test_client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_fastapi_workflows_lifecycle(test_client: TestClient) -> None:
    # Test workflows create
    response = test_client.post(
        "/api/workflows/create",
        json={"description": "Build a secure FastAPI task manager"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "workflow_id" in data
    assert data["status"] == "completed"

    workflow_id = data["workflow_id"]

    # Test workflow details
    response = test_client.get(f"/api/workflows/{workflow_id}")
    assert response.status_code == 200
    workflow_data = response.json()
    assert workflow_data["workflow_id"] == workflow_id
    assert workflow_data["status"] == "completed"
    assert "events" in workflow_data

    # Test files listing
    response = test_client.get(f"/api/generated-projects/{workflow_id}/files")
    assert response.status_code == 200
    files_data = response.json()
    assert files_data["workflow_id"] == workflow_id
    assert "files" in files_data
    assert len(files_data["files"]) > 0

    # Test specific file content retrieve
    first_file = files_data["files"][0]["path"]
    response = test_client.get(f"/api/generated-projects/{workflow_id}/files/{first_file}")
    assert response.status_code == 200
    content_data = response.json()
    assert content_data["filename"] == first_file
    assert "content" in content_data

    # Test file path traversal denial
    response = test_client.get(f"/api/generated-projects/{workflow_id}/files/../../invalid.txt")
    assert response.status_code == 404


def test_fastapi_plugins_capabilities_events(test_client: TestClient) -> None:
    # Test plugins
    response = test_client.get("/api/plugins")
    assert response.status_code == 200
    plugins_data = response.json()
    assert "plugins" in plugins_data
    assert "capability_map" in plugins_data

    # Test capabilities
    response = test_client.get("/api/capabilities")
    assert response.status_code == 200
    cap_data = response.json()
    assert "capabilities" in cap_data
    assert "planning" in cap_data["capabilities"]

    # Test events list
    response = test_client.get("/api/events")
    assert response.status_code == 200
    events_data = response.json()
    assert "events" in events_data


def test_fastapi_list_workflows(test_client: TestClient) -> None:
    # First, generate a project to ensure we have a workflow in memory/disk
    response_create = test_client.post(
        "/api/workflows/create",
        json={"description": "Build a secure FastAPI task manager"},
    )
    assert response_create.status_code == 200
    created_data = response_create.json()
    workflow_id = created_data["workflow_id"]

    # Test GET /projects
    response_list1 = test_client.get("/projects")
    assert response_list1.status_code == 200
    list1_data = response_list1.json()
    assert "projects" in list1_data
    assert len(list1_data["projects"]) > 0
    assert any(p["workflow_id"] == workflow_id for p in list1_data["projects"])

    # Test GET /api/workflows
    response_list2 = test_client.get("/api/workflows")
    assert response_list2.status_code == 200
    list2_data = response_list2.json()
    assert "projects" in list2_data
    assert len(list2_data["projects"]) > 0
    assert any(p["workflow_id"] == workflow_id for p in list2_data["projects"])

