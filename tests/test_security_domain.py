from __future__ import annotations

import pytest

from agentforge.domain.security import (
    SecurityDecision,
    SecurityDecisionStatus,
    SecurityDomainError,
    SecurityFinding,
    SecurityFindingType,
    SecurityPolicy,
)
from agentforge.domain.value_objects import Capability, RiskLevel


def test_security_policy_deduplicates_capabilities() -> None:
    policy = SecurityPolicy(
        blocked_capabilities=(Capability("api-development"), Capability("API Development")),
    )

    assert policy.blocked_capabilities == (Capability("api-development"),)


def test_security_finding_rejects_empty_message() -> None:
    with pytest.raises(SecurityDomainError, match="message"):
        SecurityFinding(
            finding_type=SecurityFindingType.PROMPT_INJECTION,
            severity=RiskLevel.HIGH,
            message=" ",
            subject_id="task-1",
        )


def test_security_decision_allows_only_allow_status() -> None:
    decision = SecurityDecision(
        status=SecurityDecisionStatus.ALLOW,
        subject_id="task-1",
        reason="Passed",
    )

    assert decision.is_allowed is True
