"""Command-line interface for AgentForge."""

from __future__ import annotations

import argparse
import json

from agentforge.application.platform import AgentForgePlatform
from agentforge.infrastructure.config import load_settings


def build_parser() -> argparse.ArgumentParser:
    """Create CLI parser."""
    parser = argparse.ArgumentParser(prog="agentforge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a project plan from an idea")
    create_parser.add_argument("description", help="Natural-language project description")
    create_parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    subparsers.add_parser("health", help="Print liveness status")
    subparsers.add_parser("ready", help="Print readiness status")

    serve_parser = subparsers.add_parser(
        "serve",
        help="Run the stdlib server or FastAPI server if installed",
    )
    serve_parser.add_argument("--host", help="Override AGENTFORGE_HOST")
    serve_parser.add_argument("--port", type=int, help="Override AGENTFORGE_PORT")

    serve_api_parser = subparsers.add_parser("serve-api", help="Run the FastAPI HTTP server")
    serve_api_parser.add_argument("--host", help="Override AGENTFORGE_HOST")
    serve_api_parser.add_argument("--port", type=int, help="Override AGENTFORGE_PORT")

    return parser


def run_create(description: str, *, as_json: bool = False) -> str:
    """Create and execute a project planning workflow."""
    platform = AgentForgePlatform.create_default(settings=load_settings())
    summary = platform.run_project_request(description)
    payload = summary.to_dict()
    if as_json:
        return json.dumps(payload, indent=2, sort_keys=True)

    events = payload.get("events", [])
    event_lines = []
    if isinstance(events, list):
        event_lines = [
            f"- {event.get('event_type')}: {event.get('message')}"
            for event in events
            if isinstance(event, dict)
        ]
    event_text = "\n".join(event_lines[-6:])
    output_path = payload.get("output_path") or "none"
    return (
        f"Workflow: {summary.workflow_id}\n"
        f"Status: {summary.status}\n"
        f"Executed nodes: {', '.join(summary.executed_node_ids) or 'none'}\n"
        f"Pending approval: {summary.pending_approval_node_id or 'none'}\n"
        f"Error: {summary.error or 'none'}\n"
        f"Output path: {output_path}\n\n"
        f"Recent events:\n{event_text}"
    )


def run_health(*, readiness: bool = False) -> str:
    """Return health or readiness as JSON."""
    platform = AgentForgePlatform.create_default(settings=load_settings())
    payload = platform.readiness().to_dict() if readiness else platform.health().to_dict()
    return json.dumps(payload, indent=2, sort_keys=True)


def run_server(host: str | None = None, port: int | None = None) -> None:
    """Run the server (uses FastAPI if installed, else stdlib)."""
    fastapi_installed = False
    try:
        import fastapi  # noqa: F401
        import uvicorn  # noqa: F401
        fastapi_installed = True
    except ImportError:
        pass

    if fastapi_installed:
        run_server_api(host=host, port=port)
        return

    from agentforge.interfaces.api.stdlib_server import create_server

    base = load_settings()
    settings = base
    if host is not None or port is not None:
        from agentforge.infrastructure.config import AgentForgeSettings

        settings = AgentForgeSettings(
            environment=base.environment,
            host=host or base.host,
            port=port or base.port,
            log_level=base.log_level,
            enable_docs=base.enable_docs,
            enable_debug_errors=base.enable_debug_errors,
            app_name=base.app_name,
        )
    platform = AgentForgePlatform.create_default(settings=settings)
    server = create_server(platform)
    print(f"AgentForge (stdlib) listening on http://{settings.host}:{settings.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


def run_server_api(host: str | None = None, port: int | None = None) -> None:
    """Run the FastAPI server using uvicorn."""
    try:
        import uvicorn

        from agentforge.interfaces.api.app import create_app
    except ImportError as exc:
        msg = "Install agentforge[api] (fastapi and uvicorn) to run the FastAPI server."
        raise RuntimeError(msg) from exc

    base = load_settings()
    settings = base
    if host is not None or port is not None:
        from agentforge.infrastructure.config import AgentForgeSettings

        settings = AgentForgeSettings(
            environment=base.environment,
            host=host or base.host,
            port=port or base.port,
            log_level=base.log_level,
            enable_docs=base.enable_docs,
            enable_debug_errors=base.enable_debug_errors,
            app_name=base.app_name,
        )

    platform = AgentForgePlatform.create_default(settings=settings)
    app = create_app(platform)
    print(f"AgentForge FastAPI listening on http://{settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port, log_level=settings.log_level.lower())


def main() -> None:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "create":
        print(run_create(args.description, as_json=args.json))
        return
    if args.command == "health":
        print(run_health())
        return
    if args.command == "ready":
        print(run_health(readiness=True))
        return
    if args.command == "serve":
        run_server(host=args.host, port=args.port)
        return
    if args.command == "serve-api":
        run_server_api(host=args.host, port=args.port)
        return


if __name__ == "__main__":
    main()
