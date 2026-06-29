from __future__ import annotations

from agentforge.application.evaluation.service import EvaluationService
from agentforge.domain.entities import Artifact, ProjectTask
from agentforge.domain.evaluation import EvaluationStatus
from agentforge.domain.value_objects import Capability
from agentforge.infrastructure.persistence.evaluation_store import InMemoryEvaluationStore
from agentforge.runtime.plugins.contracts import AgentExecutionStatus, AgentResult


def test_evaluation_service_passes_strong_agent_result() -> None:
    store = InMemoryEvaluationStore()
    service = EvaluationService(store=store)
    task = ProjectTask(title="Design API", required_capabilities=(Capability("api-development"),))
    result = AgentResult(
        status=AgentExecutionStatus.SUCCESS,
        summary="Generated API design.",
        confidence=0.95,
        artifacts=(Artifact(name="api.md", content="# API\n\nDetailed API design content."),),
    )

    report = service.evaluate_agent_result(task=task, result=result, agent_id="plugin.api")

    assert report.status == EvaluationStatus.PASSED
    assert report.overall_score >= 0.9
    assert service.passes_quality_gate(report)
    assert store.get(report.report_id) == report


def test_evaluation_service_fails_low_confidence_agent_result() -> None:
    service = EvaluationService()
    task = ProjectTask(title="Review code", required_capabilities=(Capability("code-review"),))
    result = AgentResult(
        status=AgentExecutionStatus.SUCCESS,
        summary="Reviewed code with uncertainty.",
        confidence=0.2,
    )

    report = service.evaluate_agent_result(task=task, result=result, agent_id="plugin.review")

    assert report.status == EvaluationStatus.FAILED
    assert not service.passes_quality_gate(report)
    assert any(score.criterion_id == "agent-result-confidence" for score in report.scores)


def test_evaluation_service_warns_when_result_has_no_artifacts_but_gate_allows() -> None:
    service = EvaluationService()
    task = ProjectTask(title="Run tests", required_capabilities=(Capability("quality-assurance"),))
    result = AgentResult(
        status=AgentExecutionStatus.SUCCESS,
        summary="Tests passed.",
        confidence=0.9,
    )

    report = service.evaluate_agent_result(task=task, result=result, agent_id="plugin.qa")

    assert report.status == EvaluationStatus.WARNING
    assert service.passes_quality_gate(report)
    assert any("no artifacts" in finding.message.lower() for finding in report.findings)


def test_evaluation_service_evaluates_artifact_detail() -> None:
    service = EvaluationService()
    artifact = Artifact(
        name="README.md",
        content="# README\n\nThis is a detailed generated document for AgentForge testing.",
    )

    report = service.evaluate_artifact(
        artifact=artifact, capabilities=(Capability("technical-documentation"),)
    )

    assert report.subject.capabilities == (Capability("technical-documentation"),)
    assert report.status in {EvaluationStatus.PASSED, EvaluationStatus.WARNING}
    assert service.passes_quality_gate(report)
