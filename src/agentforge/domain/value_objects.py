"""Domain value objects for AgentForge.

This module is pure Python and must not import infrastructure frameworks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum


class RiskLevel(StrEnum):
    """Risk classification used by agents, tasks, and tool execution."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class Capability:
    """Represents one ability an agent can provide.

    Examples include `planning`, `api-development`, `security-analysis`,
    `quality-assurance`, and `technical-documentation`.
    """

    name: str

    def __post_init__(self) -> None:
        normalized = re.sub(r"[\s_]+", "-", self.name.strip().lower())
        if not normalized:
            raise ValueError("Capability name cannot be empty.")
        object.__setattr__(self, "name", normalized)
