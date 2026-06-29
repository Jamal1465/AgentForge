from __future__ import annotations

import pytest

from agentforge.domain.entities import ProjectRequest, ProjectTask
from agentforge.domain.value_objects import Capability


def test_capability_normalizes_name() -> None:
    capability = Capability(" Planning ")

    assert capability.name == "planning"


def test_capability_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="Capability name cannot be empty"):
        Capability("  ")


def test_project_request_rejects_empty_description() -> None:
    with pytest.raises(ValueError, match="Project description cannot be empty"):
        ProjectRequest("  ")


def test_project_task_requires_capability() -> None:
    with pytest.raises(ValueError, match="Task must require at least one capability"):
        ProjectTask(title="Plan project", required_capabilities=())
