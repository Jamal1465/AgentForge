from __future__ import annotations

import pytest

from agentforge.application.evaluation.service import EvaluationService
from agentforge.domain.entities import ProjectTask
from agentforge.domain.value_objects import Capability
from agentforge.infrastructure.persistence.evaluation_store import (
    EvaluationStoreError,
    InMemoryEvaluationStore,
)
from agentforge.runtime.plugins.contracts import AgentExecutionStatus, AgentResult


def test_in_memory_evaluation_store_lists_by_subject_and_workflow() -> None:
    store = InMemoryEvaluationStore()
    service = EvaluationService(store=store)
    task = ProjectTask(title="Plan", required_capabilities=(Capability("planning"),))
    result = AgentResult(
        status=AgentExecutionStatus.SUCCESS,
        summary="Planned.",
        confidence=0.9,
    )

    report = service.evaluate_agent_result(
        task=task,
        result=result,
        agent_id="plugin.planner",
        workflow_id="workflow-1",
        node_id="node-1",
    )

    assert store.list_by_subject(report.subject.subject_id) == (report,)
    assert store.list_by_workflow("workflow-1") == (report,)


def test_in_memory_evaluation_store_rejects_duplicates() -> None:
    store = InMemoryEvaluationStore()
    service = EvaluationService(store=store)
    task = ProjectTask(title="Plan", required_capabilities=(Capability("planning"),))
    result = AgentResult(status=AgentExecutionStatus.SUCCESS, summary="Planned.", confidence=0.9)
    report = service.evaluate_agent_result(task=task, result=result, agent_id="plugin.planner")

    with pytest.raises(EvaluationStoreError):
        store.save(report)
