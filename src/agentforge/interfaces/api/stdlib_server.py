"""Small stdlib HTTP server for local and container smoke testing."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from agentforge.application.platform import AgentForgePlatform
from agentforge.infrastructure.config import load_settings
from agentforge.interfaces.api.handlers import (
    approve_workflow_handler,
    create_project_handler,
    get_project_handler,
    health_handler,
    list_plugins_handler,
    readiness_handler,
)
from agentforge.interfaces.api.schemas import ApiValidationError


class AgentForgeHttpHandler(BaseHTTPRequestHandler):
    """Minimal JSON HTTP handler for AgentForge."""

    platform: AgentForgePlatform

    def do_OPTIONS(self) -> None:  # noqa: N802
        """Handle CORS pre-flight requests."""
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API.
        """Handle liveness, readiness, project details, and plugins endpoints."""
        if self.path == "/health":
            self._write_json(HTTPStatus.OK, health_handler(self.platform))
            return
        if self.path == "/ready":
            status = readiness_handler(self.platform)
            http_status = (
                HTTPStatus.OK
                if status.get("status") == "ready"
                else HTTPStatus.SERVICE_UNAVAILABLE
            )
            self._write_json(http_status, status)
            return
        if self.path.startswith("/projects/"):
            workflow_id = self.path.split("/")[-1]
            try:
                data = get_project_handler(workflow_id, self.platform)
                self._write_json(HTTPStatus.OK, data)
            except Exception as exc:
                self._write_json(HTTPStatus.NOT_FOUND, {"error": str(exc)})
            return
        if self.path == "/plugins":
            self._write_json(HTTPStatus.OK, list_plugins_handler(self.platform))
            return
        self._write_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API.
        """Handle JSON workflow endpoints."""
        try:
            payload = self._read_json()
            if self.path == "/projects":
                self._write_json(HTTPStatus.CREATED, create_project_handler(payload, self.platform))
                return
            if self.path == "/workflows/approval":
                self._write_json(HTTPStatus.OK, approve_workflow_handler(payload, self.platform))
                return
            self._write_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
        except ApiValidationError as exc:
            self._write_json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": str(exc)})
        except json.JSONDecodeError:
            self._write_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid JSON payload."})

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - stdlib signature.
        """Silence default access logs for deterministic tests and local output."""
        del format, args

    def _read_json(self) -> dict[str, object]:
        length_header = self.headers.get("Content-Length", "0")
        length = int(length_header)
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ApiValidationError("JSON payload must be an object.")
        return payload

    def _write_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        # Add CORS response headers
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()
        self.wfile.write(body)


def create_server(platform: AgentForgePlatform | None = None) -> ThreadingHTTPServer:
    """Create a configured stdlib HTTP server."""
    active_platform = platform or AgentForgePlatform.create_default()
    handler = type(
        "ConfiguredAgentForgeHttpHandler",
        (AgentForgeHttpHandler,),
        {"platform": active_platform},
    )
    return ThreadingHTTPServer(
        (active_platform.settings.host, active_platform.settings.port), handler
    )


def main() -> None:
    """Run the stdlib AgentForge HTTP server."""
    settings = load_settings()
    platform = AgentForgePlatform.create_default(settings=settings)
    server = create_server(platform)
    print(f"AgentForge listening on http://{settings.host}:{settings.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    main()
