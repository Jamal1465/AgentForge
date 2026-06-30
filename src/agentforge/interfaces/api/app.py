"""Optional FastAPI adapter for AgentForge.

FastAPI is intentionally optional. The core package, tests, and CLI do not import
FastAPI at module import time. Deployments that want ASGI can install the `api`
extra and call `create_app()`.
"""

from __future__ import annotations

from typing import Any

from agentforge.application.platform import AgentForgePlatform
from agentforge.interfaces.api.handlers import (
    approve_workflow_handler,
    create_project_handler,
    get_generated_file_content_handler,
    get_generated_files_handler,
    get_project_handler,
    health_handler,
    list_capabilities_handler,
    list_events_handler,
    list_plugins_handler,
    list_projects_handler,
    readiness_handler,
)
from agentforge.interfaces.api.schemas import ApiValidationError


def create_app(platform: AgentForgePlatform | None = None) -> Any:
    """Create an optional FastAPI application."""
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
    except ImportError as exc:  # pragma: no cover - optional dependency path.
        raise RuntimeError("Install agentforge[api] to use the FastAPI adapter.") from exc

    active_platform = platform or AgentForgePlatform.create_default()
    app = FastAPI(
        title=active_platform.settings.app_name,
        version="0.1.0",
        docs_url="/docs" if active_platform.settings.enable_docs else None,
        redoc_url="/redoc" if active_platform.settings.enable_docs else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, object]:
        return health_handler(active_platform)

    @app.get("/ready")
    def ready() -> dict[str, object]:
        return readiness_handler(active_platform)

    # Legacy routes for compatibility with existing frontend
    @app.post("/projects")
    def create_project(payload: dict[str, object]) -> dict[str, object]:
        try:
            return create_project_handler(payload, active_platform)
        except ApiValidationError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/workflows/approval")
    def approve_workflow(payload: dict[str, object]) -> dict[str, object]:
        try:
            return approve_workflow_handler(payload, active_platform)
        except ApiValidationError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.get("/projects/{workflow_id}")
    def get_project(workflow_id: str) -> dict[str, object]:
        try:
            return get_project_handler(workflow_id, active_platform)
        except ApiValidationError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/plugins")
    def list_plugins() -> dict[str, object]:
        return list_plugins_handler(active_platform)

    # New API endpoints requested by user
    @app.post("/api/workflows/create")
    def api_create_workflow(payload: dict[str, object]) -> dict[str, object]:
        try:
            return create_project_handler(payload, active_platform)
        except ApiValidationError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.get("/api/workflows/{workflow_id}")
    def api_get_workflow(workflow_id: str) -> dict[str, object]:
        try:
            return get_project_handler(workflow_id, active_platform)
        except ApiValidationError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/generated-projects/{workflow_id}/files")
    def api_get_files(workflow_id: str) -> dict[str, object]:
        try:
            return get_generated_files_handler(workflow_id, active_platform)
        except ApiValidationError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/generated-projects/{workflow_id}/files/{filename:path}")
    def api_get_file_content(workflow_id: str, filename: str) -> dict[str, object]:
        try:
            return get_generated_file_content_handler(workflow_id, filename, active_platform)
        except ApiValidationError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/plugins")
    def api_list_plugins() -> dict[str, object]:
        return list_plugins_handler(active_platform)

    @app.get("/api/capabilities")
    def api_list_capabilities() -> dict[str, object]:
        return list_capabilities_handler(active_platform)

    @app.get("/api/events")
    def api_list_events(workflow_id: str | None = None) -> dict[str, object]:
        return list_events_handler(active_platform, workflow_id=workflow_id)

    @app.get("/projects")
    def list_projects() -> dict[str, object]:
        return list_projects_handler(active_platform)

    @app.get("/api/workflows")
    def api_list_workflows() -> dict[str, object]:
        return list_projects_handler(active_platform)

    return app


app = create_app()
