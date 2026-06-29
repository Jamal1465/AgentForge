"""Pure domain model for AgentForge evaluation.

Evaluation is capability-first. The core platform evaluates task outputs,
plugin results, tool results, workflow state, and artifacts without depending on
hardcoded engineering roles such as backend, frontend, database, or DevOps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import uuid4

from agentforge.domain.value_objects import Capability, RiskLevel


class EvaluationDomainError(ValueError):
    """Raised when an evaluation domain object violates invariants."""


class EvaluationSubjectType(StrEnum):
    """Type of item being evaluated."""

    AGENT_RESULT = "agent_result"
    ARTIFACT = "artifact"
    WORKFLOW = "workflow"
    TOOL_RESULT = "tool_result"


class EvaluationStatus(StrEnum):
    """Final evaluation status."""

    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"


class EvaluationMetricCategory(StrEnum):
    """Quality area measured by an evaluation criterion."""

    CORRECTNESS = "correctness"
    COMPLETENESS = "completeness"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    TRACEABILITY = "traceability"
    CONFIDENCE = "confidence"


@dataclass(frozen=True, slots=True)
class EvaluationSubject:
    """The artifact, plugin result, workflow, or tool result being evaluated."""

    subject_id: str
    subject_type: EvaluationSubjectType
    name: str
    capabilities: tuple[Capability, ...] = ()
    workflow_id: str | None = None
    node_id: str | None = None

    def __post_init__(self) -> None:
        if not self.subject_id.strip():
            raise EvaluationDomainError("Evaluation subject ID cannot be empty.")
        if not self.name.strip():
            raise EvaluationDomainError("Evaluation subject name cannot be empty.")
        object.__setattr__(self, "capabilities", tuple(dict.fromkeys(self.capabilities)))


@dataclass(frozen=True, slots=True)
class EvaluationCriterion:
    """One measurable rule in an evaluation rubric."""

    criterion_id: str
    name: str
    category: EvaluationMetricCategory
    description: str
    weight: float = 1.0
    min_score: float = 0.7
    required: bool = True

    def __post_init__(self) -> None:
        if not self.criterion_id.strip():
            raise EvaluationDomainError("Criterion ID cannot be empty.")
        if not self.name.strip():
            raise EvaluationDomainError("Criterion name cannot be empty.")
        if not self.description.strip():
            raise EvaluationDomainError("Criterion description cannot be empty.")
        if self.weight <= 0:
            raise EvaluationDomainError("Criterion weight must be greater than zero.")
        _validate_score(self.min_score, "Criterion minimum score")


@dataclass(frozen=True, slots=True)
class EvaluationScore:
    """Score for one criterion."""

    criterion_id: str
    score: float
    passed: bool
    reason: str

    def __post_init__(self) -> None:
        if not self.criterion_id.strip():
            raise EvaluationDomainError("Evaluation score criterion ID cannot be empty.")
        _validate_score(self.score, "Evaluation score")
        if not self.reason.strip():
            raise EvaluationDomainError("Evaluation score reason cannot be empty.")


@dataclass(frozen=True, slots=True)
class EvaluationFinding:
    """Human-readable issue or observation produced by evaluation."""

    message: str
    severity: RiskLevel = RiskLevel.LOW
    criterion_id: str | None = None
    evidence: str | None = None

    def __post_init__(self) -> None:
        if not self.message.strip():
            raise EvaluationDomainError("Evaluation finding message cannot be empty.")
        if self.criterion_id is not None and not self.criterion_id.strip():
            raise EvaluationDomainError("Evaluation finding criterion ID cannot be blank.")
        if self.evidence is not None and not self.evidence.strip():
            raise EvaluationDomainError("Evaluation finding evidence cannot be blank.")


@dataclass(frozen=True, slots=True)
class EvaluationRubric:
    """A weighted set of criteria used to evaluate a subject."""

    rubric_id: str
    name: str
    criteria: tuple[EvaluationCriterion, ...]

    def __post_init__(self) -> None:
        if not self.rubric_id.strip():
            raise EvaluationDomainError("Rubric ID cannot be empty.")
        if not self.name.strip():
            raise EvaluationDomainError("Rubric name cannot be empty.")
        if not self.criteria:
            raise EvaluationDomainError("Rubric must contain at least one criterion.")
        criterion_ids = [criterion.criterion_id for criterion in self.criteria]
        if len(criterion_ids) != len(set(criterion_ids)):
            raise EvaluationDomainError("Rubric criterion IDs must be unique.")


@dataclass(frozen=True, slots=True)
class QualityGate:
    """Policy used to decide whether an evaluated output can continue."""

    gate_id: str = "default-quality-gate"
    min_overall_score: float = 0.75
    block_on_failed_required_criteria: bool = True
    block_on_high_or_critical_findings: bool = True

    def __post_init__(self) -> None:
        if not self.gate_id.strip():
            raise EvaluationDomainError("Quality gate ID cannot be empty.")
        _validate_score(self.min_overall_score, "Quality gate minimum score")


@dataclass(frozen=True, slots=True)
class EvaluationReport:
    """Immutable evaluation result saved after a quality check."""

    subject: EvaluationSubject
    rubric: EvaluationRubric
    scores: tuple[EvaluationScore, ...]
    findings: tuple[EvaluationFinding, ...] = ()
    overall_score: float = 0.0
    status: EvaluationStatus = EvaluationStatus.WARNING
    report_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.report_id.strip():
            raise EvaluationDomainError("Evaluation report ID cannot be empty.")
        if not self.scores:
            raise EvaluationDomainError("Evaluation report must contain scores.")
        criterion_ids = {criterion.criterion_id for criterion in self.rubric.criteria}
        unknown_score_ids = {score.criterion_id for score in self.scores} - criterion_ids
        if unknown_score_ids:
            unknown = ", ".join(sorted(unknown_score_ids))
            raise EvaluationDomainError(f"Evaluation report contains unknown criteria: {unknown}")
        _validate_score(self.overall_score, "Evaluation report overall score")

    def failed_required_scores(self) -> tuple[EvaluationScore, ...]:
        """Return failed scores whose criteria are required."""
        required_ids = {
            criterion.criterion_id for criterion in self.rubric.criteria if criterion.required
        }
        return tuple(
            score
            for score in self.scores
            if score.criterion_id in required_ids and not score.passed
        )

    def passes_gate(self, gate: QualityGate) -> bool:
        """Return True when this report is allowed by the supplied quality gate."""
        if self.overall_score < gate.min_overall_score:
            return False
        if gate.block_on_failed_required_criteria and self.failed_required_scores():
            return False
        if gate.block_on_high_or_critical_findings:
            return not any(
                finding.severity in {RiskLevel.HIGH, RiskLevel.CRITICAL}
                for finding in self.findings
            )
        return True


def _validate_score(value: float, label: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise EvaluationDomainError(f"{label} must be between 0.0 and 1.0.")
