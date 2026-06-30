"""Evaluation application service for AgentForge.

The service performs deterministic quality checks that can be used in tests,
CI, workflow execution, and future LLM-as-judge adapters. It remains
capability-first and does not depend on concrete agent class names.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.application.evaluation.ports import EvaluationStore
from agentforge.domain.entities import Artifact, ProjectTask
from agentforge.domain.evaluation import (
    EvaluationCriterion,
    EvaluationFinding,
    EvaluationMetricCategory,
    EvaluationReport,
    EvaluationRubric,
    EvaluationScore,
    EvaluationStatus,
    EvaluationSubject,
    EvaluationSubjectType,
    QualityGate,
)
from agentforge.domain.value_objects import Capability, RiskLevel
from agentforge.domain.workflow import WorkflowGraph, WorkflowStatus
from agentforge.runtime.plugins.contracts import AgentExecutionStatus, AgentResult


@dataclass(slots=True)
class EvaluationService:
    """Coordinates evaluation and quality gate checks."""

    store: EvaluationStore | None = None
    default_agent_result_rubric: EvaluationRubric | None = None
    default_artifact_rubric: EvaluationRubric | None = None
    default_workflow_rubric: EvaluationRubric | None = None
    default_quality_gate: QualityGate = QualityGate()

    def evaluate_agent_result(
        self,
        *,
        task: ProjectTask,
        result: AgentResult,
        agent_id: str,
        workflow_id: str | None = None,
        node_id: str | None = None,
        rubric: EvaluationRubric | None = None,
    ) -> EvaluationReport:
        """Evaluate a plugin result produced for one capability-routed task."""
        active_rubric = rubric or self.default_agent_result_rubric or default_agent_result_rubric()
        subject = EvaluationSubject(
            subject_id=f"agent-result:{agent_id}:{task.task_id}",
            subject_type=EvaluationSubjectType.AGENT_RESULT,
            name=f"Agent result for {task.title}",
            capabilities=task.required_capabilities,
            workflow_id=workflow_id,
            node_id=node_id,
        )
        scores: list[EvaluationScore] = []
        findings: list[EvaluationFinding] = []

        for criterion in active_rubric.criteria:
            score, reason, extra_findings = self._score_agent_result_criterion(
                criterion=criterion,
                result=result,
                task=task,
            )
            scores.append(
                EvaluationScore(
                    criterion_id=criterion.criterion_id,
                    score=score,
                    passed=score >= criterion.min_score,
                    reason=reason,
                )
            )
            findings.extend(extra_findings)

        report = self._build_report(subject, active_rubric, tuple(scores), tuple(findings))
        self._save(report)
        return report

    def evaluate_artifact(
        self,
        *,
        artifact: Artifact,
        capabilities: tuple[Capability, ...] = (),
        workflow_id: str | None = None,
        node_id: str | None = None,
        rubric: EvaluationRubric | None = None,
    ) -> EvaluationReport:
        """Evaluate one generated artifact without relying on agent role names."""
        active_rubric = rubric or self.default_artifact_rubric or default_artifact_rubric()
        subject = EvaluationSubject(
            subject_id=f"artifact:{artifact.name}",
            subject_type=EvaluationSubjectType.ARTIFACT,
            name=artifact.name,
            capabilities=capabilities,
            workflow_id=workflow_id,
            node_id=node_id,
        )
        scores: list[EvaluationScore] = []
        findings: list[EvaluationFinding] = []
        for criterion in active_rubric.criteria:
            score, reason, extra_findings = self._score_artifact_criterion(criterion, artifact)
            scores.append(
                EvaluationScore(
                    criterion_id=criterion.criterion_id,
                    score=score,
                    passed=score >= criterion.min_score,
                    reason=reason,
                )
            )
            findings.extend(extra_findings)

        report = self._build_report(subject, active_rubric, tuple(scores), tuple(findings))
        self._save(report)
        return report

    def evaluate_workflow(
        self,
        workflow: WorkflowGraph,
        *,
        rubric: EvaluationRubric | None = None,
    ) -> EvaluationReport:
        """Evaluate workflow health and completion quality."""
        active_rubric = rubric or self.default_workflow_rubric or default_workflow_rubric()
        subject = EvaluationSubject(
            subject_id=f"workflow:{workflow.workflow_id}",
            subject_type=EvaluationSubjectType.WORKFLOW,
            name=workflow.name,
            workflow_id=workflow.workflow_id,
        )
        scores: list[EvaluationScore] = []
        findings: list[EvaluationFinding] = []
        for criterion in active_rubric.criteria:
            score, reason, extra_findings = self._score_workflow_criterion(criterion, workflow)
            scores.append(
                EvaluationScore(
                    criterion_id=criterion.criterion_id,
                    score=score,
                    passed=score >= criterion.min_score,
                    reason=reason,
                )
            )
            findings.extend(extra_findings)

        report = self._build_report(subject, active_rubric, tuple(scores), tuple(findings))
        self._save(report)
        return report

    def passes_quality_gate(
        self,
        report: EvaluationReport,
        gate: QualityGate | None = None,
    ) -> bool:
        """Return whether a report may pass the configured quality gate."""
        active_gate = gate or self.default_quality_gate
        return report.passes_gate(active_gate)

    def _score_agent_result_criterion(
        self,
        *,
        criterion: EvaluationCriterion,
        result: AgentResult,
        task: ProjectTask,
    ) -> tuple[float, str, tuple[EvaluationFinding, ...]]:
        findings: list[EvaluationFinding] = []
        match criterion.criterion_id:
            case "agent-result-status":
                if result.status == AgentExecutionStatus.SUCCESS:
                    return 1.0, "Agent result completed successfully.", ()
                if result.status == AgentExecutionStatus.NEEDS_APPROVAL:
                    findings.append(
                        EvaluationFinding(
                            message="Agent result requires human approval.",
                            severity=RiskLevel.MEDIUM,
                            criterion_id=criterion.criterion_id,
                        )
                    )
                    return 0.5, "Agent requested approval before completion.", tuple(findings)
                findings.append(
                    EvaluationFinding(
                        message="Agent result failed.",
                        severity=RiskLevel.HIGH,
                        criterion_id=criterion.criterion_id,
                    )
                )
                return 0.0, "Agent result failed.", tuple(findings)
            case "agent-result-confidence":
                if result.confidence < criterion.min_score:
                    findings.append(
                        EvaluationFinding(
                            message="Agent result confidence is below threshold.",
                            severity=RiskLevel.MEDIUM,
                            criterion_id=criterion.criterion_id,
                            evidence=f"confidence={result.confidence:.2f}",
                        )
                    )
                return (
                    result.confidence,
                    f"Agent confidence is {result.confidence:.2f}.",
                    tuple(findings),
                )
            case "agent-result-error-free":
                if result.errors:
                    findings.append(
                        EvaluationFinding(
                            message="Agent result contains errors.",
                            severity=RiskLevel.HIGH,
                            criterion_id=criterion.criterion_id,
                            evidence="; ".join(result.errors),
                        )
                    )
                    return 0.0, "Agent result contains errors.", tuple(findings)
                return 1.0, "Agent result contains no errors.", ()
            case "agent-result-artifact-integrity":
                if not result.artifacts:
                    findings.append(
                        EvaluationFinding(
                            message="Agent result produced no artifacts.",
                            severity=RiskLevel.LOW,
                            criterion_id=criterion.criterion_id,
                        )
                    )
                    return (
                        0.75,
                        "No artifacts were produced; this is acceptable for non-generative tasks.",
                        tuple(findings),
                    )
                empty_artifacts = tuple(
                    artifact.name for artifact in result.artifacts if not artifact.content.strip()
                )
                if empty_artifacts:
                    findings.append(
                        EvaluationFinding(
                            message="One or more artifacts have empty content.",
                            severity=RiskLevel.HIGH,
                            criterion_id=criterion.criterion_id,
                            evidence=", ".join(empty_artifacts),
                        )
                    )
                    return (
                        0.0,
                        "Artifact integrity failed because empty artifacts exist.",
                        tuple(findings),
                    )
                return 1.0, "All artifacts contain non-empty content.", ()
            case "agent-result-domain-consistency":
                from agentforge.agents.artifact_agents import get_resolved_context
                from agentforge.application.evaluation.domain_consistency import (
                    DomainConsistencyEvaluator,
                )

                ctx = get_resolved_context(task)
                evaluator = DomainConsistencyEvaluator()
                total_score = 1.0
                reasons = []
                for artifact in result.artifacts:
                    art_score, art_reason, art_findings = evaluator.evaluate(artifact, ctx)
                    total_score = min(total_score, art_score)
                    if art_reason:
                        reasons.append(f"{artifact.name}: {art_reason}")
                    findings.extend(art_findings)

                if total_score < 1.0:
                    return total_score, "; ".join(reasons), tuple(findings)
                return 1.0, "All artifacts maintain perfect domain consistency.", ()
            case _:
                return 1.0, "Criterion has no deterministic checker yet; treated as satisfied.", ()

    def _score_artifact_criterion(
        self,
        criterion: EvaluationCriterion,
        artifact: Artifact,
    ) -> tuple[float, str, tuple[EvaluationFinding, ...]]:
        findings: list[EvaluationFinding] = []
        match criterion.criterion_id:
            case "artifact-non-empty":
                if not artifact.content.strip():
                    findings.append(
                        EvaluationFinding(
                            message="Artifact content is empty.",
                            severity=RiskLevel.HIGH,
                            criterion_id=criterion.criterion_id,
                        )
                    )
                    return 0.0, "Artifact is empty.", tuple(findings)
                return 1.0, "Artifact contains content.", ()
            case "artifact-minimum-detail":
                if len(artifact.content.strip()) < 80:
                    findings.append(
                        EvaluationFinding(
                            message="Artifact appears too short for reliable review.",
                            severity=RiskLevel.MEDIUM,
                            criterion_id=criterion.criterion_id,
                        )
                    )
                    return (
                        0.5,
                        "Artifact is shorter than the minimum detail threshold.",
                        tuple(findings),
                    )
                return 1.0, "Artifact has sufficient detail.", ()
            case "artifact-has-title":
                first_line = (
                    artifact.content.strip().splitlines()[0] if artifact.content.strip() else ""
                )
                if not first_line.startswith("#"):
                    findings.append(
                        EvaluationFinding(
                            message="Markdown artifact does not start with a title heading.",
                            severity=RiskLevel.LOW,
                            criterion_id=criterion.criterion_id,
                        )
                    )
                    return 0.7, "Artifact lacks a top-level markdown title.", tuple(findings)
                return 1.0, "Artifact starts with a markdown title.", ()
            case _:
                return 1.0, "Criterion has no deterministic checker yet; treated as satisfied.", ()

    def _score_workflow_criterion(
        self,
        criterion: EvaluationCriterion,
        workflow: WorkflowGraph,
    ) -> tuple[float, str, tuple[EvaluationFinding, ...]]:
        findings: list[EvaluationFinding] = []
        match criterion.criterion_id:
            case "workflow-completion":
                if workflow.status == WorkflowStatus.COMPLETED:
                    return 1.0, "Workflow completed successfully.", ()
                findings.append(
                    EvaluationFinding(
                        message="Workflow did not complete successfully.",
                        severity=RiskLevel.HIGH,
                        criterion_id=criterion.criterion_id,
                        evidence=workflow.status.value,
                    )
                )
                return 0.0, f"Workflow status is {workflow.status.value}.", tuple(findings)
            case "workflow-node-health":
                total = len(workflow.nodes)
                completed = len(workflow.completed_node_ids())
                score = completed / total if total else 0.0
                if score < criterion.min_score:
                    findings.append(
                        EvaluationFinding(
                            message="Not enough workflow nodes completed.",
                            severity=RiskLevel.HIGH,
                            criterion_id=criterion.criterion_id,
                            evidence=f"completed={completed}, total={total}",
                        )
                    )
                return score, f"{completed}/{total} workflow nodes completed.", tuple(findings)
            case "workflow-auditability":
                if not workflow.events:
                    findings.append(
                        EvaluationFinding(
                            message="Workflow has no audit events.",
                            severity=RiskLevel.MEDIUM,
                            criterion_id=criterion.criterion_id,
                        )
                    )
                    return 0.0, "Workflow has no audit events.", tuple(findings)
                return 1.0, "Workflow contains audit events.", ()
            case _:
                return 1.0, "Criterion has no deterministic checker yet; treated as satisfied.", ()

    def _build_report(
        self,
        subject: EvaluationSubject,
        rubric: EvaluationRubric,
        scores: tuple[EvaluationScore, ...],
        findings: tuple[EvaluationFinding, ...],
    ) -> EvaluationReport:
        weighted_total = 0.0
        total_weight = 0.0
        for criterion in rubric.criteria:
            criterion_score = next(
                score for score in scores if score.criterion_id == criterion.criterion_id
            )
            weighted_total += criterion_score.score * criterion.weight
            total_weight += criterion.weight
        overall = weighted_total / total_weight if total_weight else 0.0
        status = _derive_status(
            rubric=rubric, scores=scores, findings=findings, overall_score=overall
        )
        return EvaluationReport(
            subject=subject,
            rubric=rubric,
            scores=scores,
            findings=findings,
            overall_score=overall,
            status=status,
        )

    def _save(self, report: EvaluationReport) -> None:
        if self.store is not None:
            self.store.save(report)


def _derive_status(
    *,
    rubric: EvaluationRubric,
    scores: tuple[EvaluationScore, ...],
    findings: tuple[EvaluationFinding, ...],
    overall_score: float,
) -> EvaluationStatus:
    required_ids = {criterion.criterion_id for criterion in rubric.criteria if criterion.required}
    has_failed_required = any(
        score.criterion_id in required_ids and not score.passed for score in scores
    )
    has_high_finding = any(
        finding.severity in {RiskLevel.HIGH, RiskLevel.CRITICAL} for finding in findings
    )
    if has_failed_required or has_high_finding:
        return EvaluationStatus.FAILED
    if findings or overall_score < 0.9:
        return EvaluationStatus.WARNING
    return EvaluationStatus.PASSED


def default_agent_result_rubric() -> EvaluationRubric:
    """Return the default capability-first plugin result rubric."""
    return EvaluationRubric(
        rubric_id="agent-result-default",
        name="Default Agent Result Rubric",
        criteria=(
            EvaluationCriterion(
                criterion_id="agent-result-status",
                name="Execution Status",
                category=EvaluationMetricCategory.CORRECTNESS,
                description="The plugin should complete the task successfully.",
                weight=3.0,
                min_score=1.0,
                required=True,
            ),
            EvaluationCriterion(
                criterion_id="agent-result-error-free",
                name="Error-Free Result",
                category=EvaluationMetricCategory.CORRECTNESS,
                description="The plugin result should not contain errors.",
                weight=2.0,
                min_score=1.0,
                required=True,
            ),
            EvaluationCriterion(
                criterion_id="agent-result-confidence",
                name="Confidence",
                category=EvaluationMetricCategory.CONFIDENCE,
                description="The plugin should report sufficient confidence.",
                weight=2.0,
                min_score=0.6,
                required=True,
            ),
            EvaluationCriterion(
                criterion_id="agent-result-artifact-integrity",
                name="Artifact Integrity",
                category=EvaluationMetricCategory.COMPLETENESS,
                description="Generated artifacts should be non-empty when artifacts are produced.",
                weight=1.0,
                min_score=0.7,
                required=False,
            ),
            EvaluationCriterion(
                criterion_id="agent-result-domain-consistency",
                name="Domain Consistency",
                category=EvaluationMetricCategory.CORRECTNESS,
                description="Checks that all generated artifacts maintain domain consistency and exclude wrong-domain content.",
                weight=3.0,
                min_score=1.0,
                required=True,
            ),
        ),
    )


def default_artifact_rubric() -> EvaluationRubric:
    """Return the default artifact rubric."""
    return EvaluationRubric(
        rubric_id="artifact-default",
        name="Default Artifact Rubric",
        criteria=(
            EvaluationCriterion(
                criterion_id="artifact-non-empty",
                name="Non-Empty Artifact",
                category=EvaluationMetricCategory.COMPLETENESS,
                description="The artifact must contain content.",
                weight=3.0,
                min_score=1.0,
                required=True,
            ),
            EvaluationCriterion(
                criterion_id="artifact-minimum-detail",
                name="Minimum Detail",
                category=EvaluationMetricCategory.MAINTAINABILITY,
                description="The artifact should contain enough detail to be useful.",
                weight=1.0,
                min_score=0.7,
                required=False,
            ),
            EvaluationCriterion(
                criterion_id="artifact-has-title",
                name="Markdown Title",
                category=EvaluationMetricCategory.MAINTAINABILITY,
                description="Markdown artifacts should begin with a title heading.",
                weight=1.0,
                min_score=0.7,
                required=False,
            ),
        ),
    )


def default_workflow_rubric() -> EvaluationRubric:
    """Return the default workflow health rubric."""
    return EvaluationRubric(
        rubric_id="workflow-default",
        name="Default Workflow Rubric",
        criteria=(
            EvaluationCriterion(
                criterion_id="workflow-completion",
                name="Workflow Completion",
                category=EvaluationMetricCategory.CORRECTNESS,
                description="The workflow should complete successfully.",
                weight=3.0,
                min_score=1.0,
                required=True,
            ),
            EvaluationCriterion(
                criterion_id="workflow-node-health",
                name="Node Health",
                category=EvaluationMetricCategory.COMPLETENESS,
                description="All workflow nodes should complete.",
                weight=2.0,
                min_score=1.0,
                required=True,
            ),
            EvaluationCriterion(
                criterion_id="workflow-auditability",
                name="Auditability",
                category=EvaluationMetricCategory.TRACEABILITY,
                description="Workflow execution should produce audit events.",
                weight=1.0,
                min_score=1.0,
                required=True,
            ),
        ),
    )
