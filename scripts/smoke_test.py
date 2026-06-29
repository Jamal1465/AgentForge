"""Local smoke test for AgentForge milestone 11."""

from __future__ import annotations

import json

from agentforge.application.platform import AgentForgePlatform


def main() -> None:
    platform = AgentForgePlatform.create_default()
    health = platform.health().to_dict()
    ready = platform.readiness().to_dict()
    run = platform.run_project_request("Build a task manager API").to_dict()
    print(json.dumps({"health": health, "ready": ready, "run": run}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
