"""Evaluation report persistence adapters."""

from __future__ import annotations

from dataclasses import dataclass, field

from agentforge.domain.evaluation import EvaluationReport


class EvaluationStoreError(RuntimeError):
    """Raised when evaluation report persistence fails."""


@dataclass(slots=True)
class InMemoryEvaluationStore:
    """Deterministic in-memory evaluation report store."""

    _reports: dict[str, EvaluationReport] = field(default_factory=dict)

    def save(self, report: EvaluationReport) -> None:
        """Persist a report."""
        if report.report_id in self._reports:
            raise EvaluationStoreError(f"Evaluation report already exists: {report.report_id}")
        self._reports[report.report_id] = report

    def get(self, report_id: str) -> EvaluationReport:
        """Return a report by ID."""
        try:
            return self._reports[report_id]
        except KeyError as exc:
            raise EvaluationStoreError(f"Unknown evaluation report: {report_id}") from exc

    def list_by_subject(self, subject_id: str) -> tuple[EvaluationReport, ...]:
        """Return reports for one subject."""
        return tuple(
            sorted(
                (
                    report
                    for report in self._reports.values()
                    if report.subject.subject_id == subject_id
                ),
                key=lambda report: report.report_id,
            )
        )

    def list_by_workflow(self, workflow_id: str) -> tuple[EvaluationReport, ...]:
        """Return reports attached to one workflow."""
        return tuple(
            sorted(
                (
                    report
                    for report in self._reports.values()
                    if report.subject.workflow_id == workflow_id
                ),
                key=lambda report: report.report_id,
            )
        )
