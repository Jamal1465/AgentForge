"""Security service for capability-first AgentForge guardrails."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from agentforge.application.security.ports import SecurityAuditStore
from agentforge.domain.entities import ProjectTask
from agentforge.domain.security import (
    SecurityAuditEvent,
    SecurityDecision,
    SecurityDecisionStatus,
    SecurityFinding,
    SecurityFindingType,
    SecurityPolicy,
)
from agentforge.domain.tools import ToolDefinition, ToolInvocation
from agentforge.domain.value_objects import RiskLevel
from agentforge.runtime.plugins.contracts import AgentMetadata


@dataclass(slots=True)
class SecurityService:
    """Applies text, capability, plugin, and tool guardrails.

    The service is intentionally independent of concrete agent implementations.
    It reasons about task capabilities, plugin metadata, and tool definitions.
    """

    policy: SecurityPolicy = SecurityPolicy()
    audit_store: SecurityAuditStore | None = None
    prompt_injection_patterns: tuple[re.Pattern[str], ...] = field(
        default_factory=lambda: tuple(
            re.compile(pattern, re.IGNORECASE)
            for pattern in (
                r"ignore\s+(all\s+)?previous\s+instructions",
                r"disregard\s+(all\s+)?(previous|system)\s+instructions",
                r"reveal\s+(the\s+)?(system|developer)\s+prompt",
                r"print\s+(the\s+)?(system|developer)\s+prompt",
                r"bypass\s+(security|guardrails|policy)",
                r"disable\s+(security|guardrails|safety)",
                r"act\s+as\s+(dan|developer\s+mode)",
            )
        )
    )
    secret_patterns: tuple[re.Pattern[str], ...] = field(
        default_factory=lambda: tuple(
            re.compile(pattern, re.IGNORECASE)
            for pattern in (
                r"AIza[0-9A-Za-z_\-]{20,}",
                r"sk-[0-9A-Za-z]{20,}",
                r"github_pat_[0-9A-Za-z_]{20,}",
                r"ghp_[0-9A-Za-z]{20,}",
                r"AKIA[0-9A-Z]{16}",
                r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[^\s'\"]{8,}",
            )
        )
    )
    pii_patterns: tuple[re.Pattern[str], ...] = field(
        default_factory=lambda: tuple(
            re.compile(pattern, re.IGNORECASE)
            for pattern in (
                r"\b\d{3}-\d{2}-\d{4}\b",
                r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
            )
        )
    )

    def scan_text(self, subject_id: str, text: str) -> tuple[SecurityFinding, ...]:
        """Scan text for prompt injection, secrets, and basic PII indicators."""
        findings: list[SecurityFinding] = []
        findings.extend(
            self._scan_patterns(
                subject_id=subject_id,
                text=text,
                patterns=self.prompt_injection_patterns,
                finding_type=SecurityFindingType.PROMPT_INJECTION,
                severity=RiskLevel.HIGH,
                message="Potential prompt injection instruction detected.",
            )
        )
        findings.extend(
            self._scan_patterns(
                subject_id=subject_id,
                text=text,
                patterns=self.secret_patterns,
                finding_type=SecurityFindingType.SECRET_EXPOSURE,
                severity=RiskLevel.HIGH,
                message="Potential secret or credential detected.",
            )
        )
        findings.extend(
            self._scan_patterns(
                subject_id=subject_id,
                text=text,
                patterns=self.pii_patterns,
                finding_type=SecurityFindingType.PII_EXPOSURE,
                severity=RiskLevel.MEDIUM,
                message="Potential personally identifiable information detected.",
            )
        )
        return tuple(findings)

    def redact_secrets(self, text: str) -> str:
        """Redact known secret-like patterns from text."""
        redacted = text
        for pattern in self.secret_patterns:
            redacted = pattern.sub("[REDACTED_SECRET]", redacted)
        return redacted

    def assess_task(
        self,
        task: ProjectTask,
        *,
        actor_id: str,
        approval_granted: bool = False,
    ) -> SecurityDecision:
        """Assess whether a capability-routed task may execute."""
        findings: list[SecurityFinding] = []
        findings.extend(self.scan_text(task.task_id, "\n".join((task.title, task.description))))

        for capability in task.required_capabilities:
            if self.policy.is_capability_blocked(capability):
                findings.append(
                    SecurityFinding(
                        finding_type=SecurityFindingType.BLOCKED_CAPABILITY,
                        severity=RiskLevel.CRITICAL,
                        subject_id=task.task_id,
                        message=f"Capability is blocked by policy: {capability.name}.",
                        evidence=capability.name,
                    )
                )
            elif self.policy.does_capability_require_approval(capability):
                findings.append(
                    SecurityFinding(
                        finding_type=SecurityFindingType.HIGH_RISK_CAPABILITY,
                        severity=RiskLevel.HIGH,
                        subject_id=task.task_id,
                        message=f"Capability requires approval: {capability.name}.",
                        evidence=capability.name,
                    )
                )

        if task.risk_level in self.policy.approval_required_risk_levels:
            findings.append(
                SecurityFinding(
                    finding_type=SecurityFindingType.HIGH_RISK_CAPABILITY,
                    severity=task.risk_level,
                    subject_id=task.task_id,
                    message=f"Task risk level requires approval: {task.risk_level.value}.",
                    evidence=task.risk_level.value,
                )
            )

        decision = self._decision_from_findings(
            subject_id=task.task_id,
            actor_id=actor_id,
            findings=tuple(findings),
            approval_granted=approval_granted,
            reason_when_allowed="Task passed security policy.",
        )
        self._audit("security.task_assessed", actor_id, decision)
        return decision

    def assess_plugin(self, metadata: AgentMetadata, *, actor_id: str) -> SecurityDecision:
        """Assess plugin metadata before registration or execution."""
        findings: list[SecurityFinding] = []
        if (
            self.policy.require_trusted_plugins
            and metadata.agent_id not in self.policy.trusted_plugin_ids
        ):
            findings.append(
                SecurityFinding(
                    finding_type=SecurityFindingType.UNTRUSTED_PLUGIN,
                    severity=RiskLevel.HIGH,
                    subject_id=metadata.agent_id,
                    message="Plugin is not present in the trusted plugin allowlist.",
                    evidence=metadata.agent_id,
                )
            )

        for capability in metadata.capabilities:
            if self.policy.is_capability_blocked(capability):
                findings.append(
                    SecurityFinding(
                        finding_type=SecurityFindingType.BLOCKED_CAPABILITY,
                        severity=RiskLevel.CRITICAL,
                        subject_id=metadata.agent_id,
                        message=f"Plugin declares blocked capability: {capability.name}.",
                        evidence=capability.name,
                    )
                )

        decision = self._decision_from_findings(
            subject_id=metadata.agent_id,
            actor_id=actor_id,
            findings=tuple(findings),
            approval_granted=False,
            reason_when_allowed="Plugin metadata passed security policy.",
        )
        self._audit("security.plugin_assessed", actor_id, decision)
        return decision

    def assess_tool_invocation(
        self,
        definition: ToolDefinition,
        invocation: ToolInvocation,
    ) -> SecurityDecision:
        """Assess a tool call before the underlying adapter is invoked."""
        text = "\n".join(str(value) for value in invocation.arguments.values())
        findings: list[SecurityFinding] = list(self.scan_text(invocation.invocation_id, text))

        if definition.is_destructive and not self.policy.allow_destructive_tools:
            findings.append(
                SecurityFinding(
                    finding_type=SecurityFindingType.DESTRUCTIVE_OPERATION,
                    severity=RiskLevel.CRITICAL,
                    subject_id=invocation.invocation_id,
                    message="Destructive tool execution is disabled by policy.",
                    evidence=definition.tool_id,
                )
            )

        if definition.risk_level in self.policy.approval_required_risk_levels:
            findings.append(
                SecurityFinding(
                    finding_type=SecurityFindingType.TOOL_POLICY_VIOLATION,
                    severity=definition.risk_level,
                    subject_id=invocation.invocation_id,
                    message=f"Tool risk level requires approval: {definition.risk_level.value}.",
                    evidence=definition.tool_id,
                )
            )

        decision = self._decision_from_findings(
            subject_id=invocation.invocation_id,
            actor_id=invocation.caller_id,
            findings=tuple(findings),
            approval_granted=invocation.approval_granted,
            reason_when_allowed="Tool invocation passed security policy.",
        )
        self._audit("security.tool_assessed", invocation.caller_id, decision)
        return decision

    def _decision_from_findings(
        self,
        *,
        subject_id: str,
        actor_id: str,
        findings: tuple[SecurityFinding, ...],
        approval_granted: bool,
        reason_when_allowed: str,
    ) -> SecurityDecision:
        del actor_id
        blocking_findings = tuple(
            finding
            for finding in findings
            if finding.finding_type
            in {
                SecurityFindingType.BLOCKED_CAPABILITY,
                SecurityFindingType.DESTRUCTIVE_OPERATION,
            }
            or (
                self.policy.block_prompt_injection
                and finding.finding_type == SecurityFindingType.PROMPT_INJECTION
            )
            or (
                self.policy.block_secret_exposure
                and finding.finding_type == SecurityFindingType.SECRET_EXPOSURE
            )
            or finding.finding_type == SecurityFindingType.UNTRUSTED_PLUGIN
        )
        if blocking_findings:
            return SecurityDecision(
                status=SecurityDecisionStatus.BLOCK,
                subject_id=subject_id,
                reason="Security policy blocked execution.",
                findings=findings,
            )

        approval_findings = tuple(
            finding
            for finding in findings
            if finding.severity in self.policy.approval_required_risk_levels
        )
        if approval_findings and not approval_granted:
            return SecurityDecision(
                status=SecurityDecisionStatus.REQUIRES_APPROVAL,
                subject_id=subject_id,
                reason="Security policy requires human approval.",
                findings=findings,
            )

        return SecurityDecision(
            status=SecurityDecisionStatus.ALLOW,
            subject_id=subject_id,
            reason=reason_when_allowed,
            findings=findings,
        )

    def _audit(self, event_type: str, actor_id: str, decision: SecurityDecision) -> None:
        if self.audit_store is None:
            return
        self.audit_store.record(
            SecurityAuditEvent(
                event_type=event_type,
                subject_id=decision.subject_id,
                actor_id=actor_id,
                decision_status=decision.status,
                message=decision.reason,
                finding_ids=tuple(finding.finding_id for finding in decision.findings),
            )
        )

    @staticmethod
    def _scan_patterns(
        *,
        subject_id: str,
        text: str,
        patterns: tuple[re.Pattern[str], ...],
        finding_type: SecurityFindingType,
        severity: RiskLevel,
        message: str,
    ) -> tuple[SecurityFinding, ...]:
        findings: list[SecurityFinding] = []
        for pattern in patterns:
            for match in pattern.finditer(text):
                findings.append(
                    SecurityFinding(
                        finding_type=finding_type,
                        severity=severity,
                        subject_id=subject_id,
                        message=message,
                        evidence=match.group(0)[:120],
                    )
                )
        return tuple(findings)
