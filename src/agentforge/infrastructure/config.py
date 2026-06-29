"""Configuration loading for AgentForge interfaces and deployment.

Settings are intentionally small and environment-driven so the same package can
run from the CLI, a local HTTP server, Docker, or a future ADK/Cloud Run entry
point without changing source code.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum


class RuntimeEnvironment(StrEnum):
    """Supported runtime environment labels."""

    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class SettingsError(ValueError):
    """Raised when configuration is invalid."""


@dataclass(frozen=True, slots=True)
class AgentForgeSettings:
    """Runtime settings used by interfaces and deployment adapters."""

    environment: RuntimeEnvironment = RuntimeEnvironment.LOCAL
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "INFO"
    enable_docs: bool = True
    enable_debug_errors: bool = False
    app_name: str = "AgentForge"

    def __post_init__(self) -> None:
        if not self.host.strip():
            raise SettingsError("AGENTFORGE_HOST cannot be empty.")
        if not 1 <= self.port <= 65535:
            raise SettingsError("AGENTFORGE_PORT must be between 1 and 65535.")
        normalized_level = self.log_level.strip().upper()
        if normalized_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise SettingsError("AGENTFORGE_LOG_LEVEL is invalid.")
        object.__setattr__(self, "log_level", normalized_level)

    @property
    def is_production(self) -> bool:
        """Return True when running in production mode."""
        return self.environment == RuntimeEnvironment.PRODUCTION


def load_settings(env: Mapping[str, str] | None = None) -> AgentForgeSettings:
    """Load AgentForge settings from environment variables."""
    source = env if env is not None else os.environ
    environment_value = source.get("AGENTFORGE_ENV", RuntimeEnvironment.LOCAL.value).strip().lower()
    try:
        environment = RuntimeEnvironment(environment_value)
    except ValueError as exc:
        valid = ", ".join(item.value for item in RuntimeEnvironment)
        raise SettingsError(f"AGENTFORGE_ENV must be one of: {valid}.") from exc

    return AgentForgeSettings(
        environment=environment,
        host=source.get("AGENTFORGE_HOST", "0.0.0.0"),
        port=_parse_int(source.get("AGENTFORGE_PORT", "8080"), "AGENTFORGE_PORT"),
        log_level=source.get("AGENTFORGE_LOG_LEVEL", "INFO"),
        enable_docs=_parse_bool(source.get("AGENTFORGE_ENABLE_DOCS", "true")),
        enable_debug_errors=_parse_bool(source.get("AGENTFORGE_DEBUG_ERRORS", "false")),
        app_name=source.get("AGENTFORGE_APP_NAME", "AgentForge"),
    )


def _parse_int(value: str, name: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise SettingsError(f"{name} must be an integer.") from exc


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise SettingsError(f"Invalid boolean value: {value}.")
