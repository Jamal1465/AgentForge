"""Deployment health-check helpers."""

from __future__ import annotations

from agentforge.application.platform import AgentForgePlatform


def assert_platform_ready(platform: AgentForgePlatform) -> None:
    """Raise RuntimeError when the platform cannot serve traffic."""
    readiness = platform.readiness()
    if readiness.status != "ready":
        raise RuntimeError(f"AgentForge is not ready: {readiness.details}")
