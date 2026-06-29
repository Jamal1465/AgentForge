"""Evaluation application ports."""

from __future__ import annotations

from typing import Protocol

from agentforge.domain.evaluation import EvaluationReport


class EvaluationStore(Protocol):
    """Persistence boundary for evaluation reports."""

    def save(self, report: EvaluationReport) -> None:
        """Persist one evaluation report."""
        ...

    def get(self, report_id: str) -> EvaluationReport:
        """Return one evaluation report by ID."""
        ...

    def list_by_subject(self, subject_id: str) -> tuple[EvaluationReport, ...]:
        """Return reports for a subject."""
        ...

    def list_by_workflow(self, workflow_id: str) -> tuple[EvaluationReport, ...]:
        """Return reports for a workflow."""
        ...
