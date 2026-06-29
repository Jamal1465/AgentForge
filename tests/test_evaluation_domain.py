from __future__ import annotations

import pytest

from agentforge.domain.evaluation import (
    EvaluationCriterion,
    EvaluationDomainError,
    EvaluationMetricCategory,
    EvaluationReport,
    EvaluationRubric,
    EvaluationScore,
    EvaluationStatus,
    EvaluationSubject,
    EvaluationSubjectType,
    QualityGate,
)
from agentforge.domain.value_objects import Capability


def test_evaluation_subject_normalizes_duplicate_capabilities() -> None:
    subject = EvaluationSubject(
        subject_id="subject-1",
        subject_type=EvaluationSubjectType.AGENT_RESULT,
        name="Agent Result",
        capabilities=(Capability("API Development"), Capability("api-development")),
    )

    assert subject.capabilities == (Capability("api-development"),)


def test_evaluation_criterion_rejects_invalid_score_threshold() -> None:
    with pytest.raises(EvaluationDomainError):
        EvaluationCriterion(
            criterion_id="confidence",
            name="Confidence",
            category=EvaluationMetricCategory.CONFIDENCE,
            description="Confidence must be valid.",
            min_score=1.5,
        )


def test_evaluation_report_tracks_failed_required_scores() -> None:
    criterion = EvaluationCriterion(
        criterion_id="status",
        name="Status",
        category=EvaluationMetricCategory.CORRECTNESS,
        description="Status must pass.",
        min_score=1.0,
        required=True,
    )
    rubric = EvaluationRubric(rubric_id="rubric", name="Rubric", criteria=(criterion,))
    subject = EvaluationSubject(
        subject_id="subject",
        subject_type=EvaluationSubjectType.AGENT_RESULT,
        name="Subject",
    )
    report = EvaluationReport(
        subject=subject,
        rubric=rubric,
        scores=(
            EvaluationScore(
                criterion_id="status",
                score=0.0,
                passed=False,
                reason="Failed.",
            ),
        ),
        overall_score=0.0,
        status=EvaluationStatus.FAILED,
    )

    assert report.failed_required_scores()
    assert not report.passes_gate(QualityGate(min_overall_score=0.75))
