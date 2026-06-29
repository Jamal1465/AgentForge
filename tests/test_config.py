from __future__ import annotations

import pytest

from agentforge.infrastructure.config import RuntimeEnvironment, SettingsError, load_settings


def test_load_settings_from_mapping() -> None:
    settings = load_settings(
        {
            "AGENTFORGE_ENV": "test",
            "AGENTFORGE_HOST": "127.0.0.1",
            "AGENTFORGE_PORT": "9000",
            "AGENTFORGE_LOG_LEVEL": "debug",
            "AGENTFORGE_ENABLE_DOCS": "false",
        }
    )

    assert settings.environment == RuntimeEnvironment.TEST
    assert settings.host == "127.0.0.1"
    assert settings.port == 9000
    assert settings.log_level == "DEBUG"
    assert not settings.enable_docs


def test_load_settings_rejects_invalid_port() -> None:
    with pytest.raises(SettingsError):
        load_settings({"AGENTFORGE_PORT": "not-a-number"})
