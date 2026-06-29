"""Workflow runner application service.

This module coordinates workflow execution without depending on web frameworks,
databases, or concrete infrastructure. It uses the plugin registry and router to
execute ProjectTask nodes through registered agent plugins.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentforge.application.evaluation.service import EvaluationService
from agentforge.application.memory.service import MemoryService
from agentforge.application.observability.service import ObservabilityService
from agentforge.application.security.service import SecurityService
from agentforge.application.workflows.ports import WorkflowStore
from agentforge.domain.evaluation import EvaluationStatus
from agentforge.domain.observability import TelemetryEventType, TelemetrySeverity, TraceContext
from agentforge.domain.security import SecurityDecisionStatus
from agentforge.domain.workflow import WorkflowGraph, WorkflowNodeStatus, WorkflowStatus
from agentforge.runtime.plugins.contracts import AgentExecutionStatus, AgentResult
from agentforge.runtime.registry.agent_registry import AgentRegistry
from agentforge.runtime.routing.capability_router import CapabilityRouter, RoutingStatus


class WorkflowExecutionError(RuntimeError):
    """Raised when workflow execution cannot continue."""


@dataclass(frozen=True, slots=True)
class WorkflowRunResult:
    """Summary returned after running or resuming a workflow."""

    workflow_id: str
    status: WorkflowStatus
    executed_node_ids: tuple[str, ...]
    pending_approval_node_id: str | None = None
    error: str | None = None


@dataclass(slots=True)
class WorkflowRunner:
    """Executes workflow graphs through registered agent plugins.

    The runner is intentionally deterministic for the first production slice:
    ready nodes are executed in sorted node ID order. Parallel execution can be
    added later without changing the domain model or persistence port.
    """

    registry: AgentRegistry
    router: CapabilityRouter
    store: WorkflowStore
    memory_service: MemoryService | None = None
    security_service: SecurityService | None = None
    evaluation_service: EvaluationService | None = None
    observability_service: ObservabilityService | None = None

    def run(self, workflow: WorkflowGraph) -> WorkflowRunResult:
        """Run a workflow until completion, failure, or approval pause."""
        workflow.status = WorkflowStatus.RUNNING
        workflow.record_event("workflow.started", "Workflow execution started.")
        self._remember(
            workflow.workflow_id,
            "Workflow execution started.",
            tags=("workflow", "started"),
        )
        self._observe_event(
            workflow.workflow_id,
            name="workflow.started",
            event_type=TelemetryEventType.WORKFLOW,
            message="Workflow execution started.",
        )
        self._observe_counter(
            "workflow.started_total",
            workflow.workflow_id,
            labels={"status": workflow.status.value},
        )
        self.store.save(workflow)
        return self._drain_ready_nodes(workflow)

    def resume_after_approval(
        self,
        workflow_id: str,
        node_id: str,
        approved: bool,
    ) -> WorkflowRunResult:
        """Resume a paused workflow after a human approval decision."""
        workflow = self.store.get(workflow_id)
        node = workflow.nodes.get(node_id)
        if node is None:
            raise WorkflowExecutionError(f"Unknown workflow node: {node_id}")
        if node.status != WorkflowNodeStatus.WAITING_FOR_APPROVAL:
            raise WorkflowExecutionError("Only nodes waiting for approval can be resumed.")

        if not approved:
            node.status = WorkflowNodeStatus.FAILED
            node.last_error = "Human approval rejected."
            workflow.status = WorkflowStatus.FAILED
            workflow.record_event(
                "approval.rejected",
                "Human approval rejected; workflow failed.",
                node_id=node.node_id,
            )
            self._remember(
                workflow.workflow_id,
                "Human approval rejected; workflow failed.",
                tags=("approval", "rejected"),
                node_id=node.node_id,
            )
            self._observe_event(
                workflow.workflow_id,
                name="approval.rejected",
                event_type=TelemetryEventType.NODE,
                message="Human approval rejected; workflow failed.",
                node_id=node.node_id,
                severity=TelemetrySeverity.ERROR,
            )
            self.store.save(workflow)
            return WorkflowRunResult(
                workflow_id=workflow.workflow_id,
                status=workflow.status,
                executed_node_ids=(),
                error=node.last_error,
            )

        node.approval_granted = True
        node.status = WorkflowNodeStatus.PENDING
        workflow.status = WorkflowStatus.RUNNING
        workflow.record_event(
            "approval.granted",
            "Human approval granted; workflow resumed.",
            node_id=node.node_id,
        )
        self._remember(
            workflow.workflow_id,
            "Human approval granted; workflow resumed.",
            tags=("approval", "granted"),
            node_id=node.node_id,
        )
        self._observe_event(
            workflow.workflow_id,
            name="approval.granted",
            event_type=TelemetryEventType.NODE,
            message="Human approval granted; workflow resumed.",
            node_id=node.node_id,
        )
        self.store.save(workflow)
        return self._drain_ready_nodes(workflow)

    def _drain_ready_nodes(self, workflow: WorkflowGraph) -> WorkflowRunResult:
        executed: list[str] = []

        while True:
            ready_nodes = sorted(workflow.ready_nodes(), key=lambda node: node.node_id)
            if not ready_nodes:
                break

            for node in ready_nodes:
                if node.requires_approval and not node.approval_granted:
                    node.status = WorkflowNodeStatus.WAITING_FOR_APPROVAL
                    workflow.status = WorkflowStatus.WAITING_FOR_APPROVAL
                    workflow.record_event(
                        "approval.required",
                        "Workflow paused for human approval.",
                        node_id=node.node_id,
                    )
                    self._remember(
                        workflow.workflow_id,
                        "Workflow paused for human approval.",
                        tags=("approval", "pause"),
                        node_id=node.node_id,
                    )
                    self._observe_event(
                        workflow.workflow_id,
                        name="approval.required",
                        event_type=TelemetryEventType.NODE,
                        message="Workflow paused for human approval.",
                        node_id=node.node_id,
                        severity=TelemetrySeverity.WARNING,
                    )
                    self._observe_counter(
                        "workflow.approval_required_total",
                        workflow.workflow_id,
                        node_id=node.node_id,
                    )
                    self.store.save(workflow)
                    return WorkflowRunResult(
                        workflow_id=workflow.workflow_id,
                        status=workflow.status,
                        executed_node_ids=tuple(executed),
                        pending_approval_node_id=node.node_id,
                    )

                self._execute_node(workflow, node.node_id)
                executed.append(node.node_id)
                self.store.save(workflow)

                if workflow.status == WorkflowStatus.FAILED:
                    return WorkflowRunResult(
                        workflow_id=workflow.workflow_id,
                        status=workflow.status,
                        executed_node_ids=tuple(executed),
                        error=workflow.nodes[node.node_id].last_error,
                    )
                if workflow.status == WorkflowStatus.WAITING_FOR_APPROVAL:
                    return WorkflowRunResult(
                        workflow_id=workflow.workflow_id,
                        status=workflow.status,
                        executed_node_ids=tuple(executed),
                        pending_approval_node_id=node.node_id,
                    )

        if workflow.has_failed_nodes():
            workflow.status = WorkflowStatus.FAILED
            workflow.record_event(
                "workflow.failed",
                "Workflow failed because one or more nodes failed.",
            )
            self._remember(
                workflow.workflow_id,
                "Workflow failed because one or more nodes failed.",
                tags=("workflow", "failed"),
            )
            self._observe_event(
                workflow.workflow_id,
                name="workflow.failed",
                event_type=TelemetryEventType.WORKFLOW,
                message="Workflow failed because one or more nodes failed.",
                severity=TelemetrySeverity.ERROR,
            )
            self._observe_counter(
                "workflow.finished_total",
                workflow.workflow_id,
                labels={"status": WorkflowStatus.FAILED.value},
            )
        elif workflow.all_nodes_completed():
            workflow.status = WorkflowStatus.COMPLETED
            workflow.record_event("workflow.completed", "Workflow execution completed.")
            self._remember(
                workflow.workflow_id,
                "Workflow execution completed.",
                tags=("workflow", "completed"),
            )
            self._observe_event(
                workflow.workflow_id,
                name="workflow.completed",
                event_type=TelemetryEventType.WORKFLOW,
                message="Workflow execution completed.",
            )
            self._observe_counter(
                "workflow.finished_total",
                workflow.workflow_id,
                labels={"status": WorkflowStatus.COMPLETED.value},
            )
        else:
            workflow.status = WorkflowStatus.FAILED
            workflow.record_event("workflow.deadlocked", "Workflow could not make progress.")
            self._remember(
                workflow.workflow_id,
                "Workflow could not make progress.",
                tags=("workflow", "deadlocked"),
            )
            self._observe_event(
                workflow.workflow_id,
                name="workflow.deadlocked",
                event_type=TelemetryEventType.WORKFLOW,
                message="Workflow could not make progress.",
                severity=TelemetrySeverity.ERROR,
            )
            self._observe_counter(
                "workflow.finished_total",
                workflow.workflow_id,
                labels={"status": WorkflowStatus.FAILED.value},
            )

        self.store.save(workflow)
        return WorkflowRunResult(
            workflow_id=workflow.workflow_id,
            status=workflow.status,
            executed_node_ids=tuple(executed),
            error=(
                None
                if workflow.status == WorkflowStatus.COMPLETED
                else "Workflow did not complete."
            ),
        )

    def _execute_node(self, workflow: WorkflowGraph, node_id: str) -> None:
        node = workflow.nodes[node_id]
        if node.task is None:
            node.status = WorkflowNodeStatus.COMPLETED
            workflow.record_event(
                "node.completed",
                "Non-agent workflow node completed.",
                node_id=node.node_id,
            )
            self._remember(
                workflow.workflow_id,
                "Non-agent workflow node completed.",
                tags=("node", "completed"),
                node_id=node.node_id,
            )
            self._observe_event(
                workflow.workflow_id,
                name="node.completed",
                event_type=TelemetryEventType.NODE,
                message="Non-agent workflow node completed.",
                node_id=node.node_id,
            )
            self._observe_counter(
                "workflow.node.finished_total",
                workflow.workflow_id,
                node_id=node.node_id,
                labels={"status": WorkflowNodeStatus.COMPLETED.value},
            )
            return

        node.status = WorkflowNodeStatus.RUNNING
        workflow.record_event(
            "node.started",
            "Workflow node execution started.",
            node_id=node.node_id,
        )
        self._remember(
            workflow.workflow_id,
            "Workflow node execution started.",
            tags=("node", "started"),
            node_id=node.node_id,
        )
        self._observe_event(
            workflow.workflow_id,
            name="node.started",
            event_type=TelemetryEventType.NODE,
            message="Workflow node execution started.",
            node_id=node.node_id,
            metadata={"task_id": node.task.task_id},
        )
        self._observe_counter(
            "workflow.node.started_total",
            workflow.workflow_id,
            node_id=node.node_id,
        )

        security_decision = self._assess_task_security(workflow, node_id)
        if security_decision == SecurityDecisionStatus.BLOCK:
            node.status = WorkflowNodeStatus.FAILED
            workflow.status = WorkflowStatus.FAILED
            return
        if security_decision == SecurityDecisionStatus.REQUIRES_APPROVAL:
            node.status = WorkflowNodeStatus.WAITING_FOR_APPROVAL
            workflow.status = WorkflowStatus.WAITING_FOR_APPROVAL
            return

        while node.attempt_count < node.max_attempts:
            node.attempt_count += 1
            decision = self.router.route(node.task)
            if decision.status == RoutingStatus.NO_MATCH or decision.selected_agent_id is None:
                node.status = WorkflowNodeStatus.FAILED
                node.last_error = decision.reason
                workflow.status = WorkflowStatus.FAILED
                workflow.record_event("node.routing_failed", decision.reason, node_id=node.node_id)
                self._remember(
                    workflow.workflow_id,
                    decision.reason,
                    tags=("node", "routing-failed"),
                    node_id=node.node_id,
                )
                self._observe_event(
                    workflow.workflow_id,
                    name="routing.failed",
                    event_type=TelemetryEventType.ROUTING,
                    message=decision.reason,
                    node_id=node.node_id,
                    severity=TelemetrySeverity.ERROR,
                )
                self._observe_counter(
                    "routing.finished_total",
                    workflow.workflow_id,
                    node_id=node.node_id,
                    labels={"status": RoutingStatus.NO_MATCH.value},
                )
                return

            self._observe_event(
                workflow.workflow_id,
                name="routing.routed",
                event_type=TelemetryEventType.ROUTING,
                message=decision.reason,
                node_id=node.node_id,
                agent_id=decision.selected_agent_id,
            )
            self._observe_counter(
                "routing.finished_total",
                workflow.workflow_id,
                node_id=node.node_id,
                labels={"status": RoutingStatus.ROUTED.value},
            )
            agent = self.registry.get(decision.selected_agent_id)
            result = agent.execute(node.task)
            workflow.record_event(
                "node.agent_result",
                self._result_summary(result),
                node_id=node.node_id,
            )
            self._observe_event(
                workflow.workflow_id,
                name=f"plugin.execution.{result.status.value}",
                event_type=TelemetryEventType.PLUGIN,
                message=self._result_summary(result),
                node_id=node.node_id,
                agent_id=agent.metadata.agent_id,
                severity=(
                    TelemetrySeverity.INFO
                    if result.status == AgentExecutionStatus.SUCCESS
                    else TelemetrySeverity.WARNING
                ),
                metadata={"confidence": f"{result.confidence:.2f}"},
            )
            self._observe_counter(
                "plugin.execution.finished_total",
                workflow.workflow_id,
                node_id=node.node_id,
                labels={"agent_id": agent.metadata.agent_id, "status": result.status.value},
            )

            if result.status == AgentExecutionStatus.SUCCESS:
                evaluation_passed = self._evaluate_agent_result(
                    workflow=workflow,
                    node_id=node.node_id,
                    agent_id=agent.metadata.agent_id,
                    result=result,
                )
                if not evaluation_passed:
                    node.status = WorkflowNodeStatus.FAILED
                    workflow.status = WorkflowStatus.FAILED
                    return

                node.status = WorkflowNodeStatus.COMPLETED
                node.last_error = None
                node.artifacts = result.artifacts
                workflow.record_event(
                    "node.completed",
                    "Workflow node completed successfully.",
                    node_id=node.node_id,
                )
                self._remember(
                    workflow.workflow_id,
                    "Workflow node completed successfully.",
                    tags=("node", "completed"),
                    node_id=node.node_id,
                )
                self._observe_event(
                    workflow.workflow_id,
                    name="node.completed",
                    event_type=TelemetryEventType.NODE,
                    message="Workflow node completed successfully.",
                    node_id=node.node_id,
                )
                self._observe_counter(
                    "workflow.node.finished_total",
                    workflow.workflow_id,
                    node_id=node.node_id,
                    labels={"status": WorkflowNodeStatus.COMPLETED.value},
                )
                return

            if result.status == AgentExecutionStatus.NEEDS_APPROVAL:
                node.status = WorkflowNodeStatus.WAITING_FOR_APPROVAL
                workflow.status = WorkflowStatus.WAITING_FOR_APPROVAL
                workflow.record_event(
                    "node.needs_approval",
                    result.summary,
                    node_id=node.node_id,
                )
                self._remember(
                    workflow.workflow_id,
                    result.summary,
                    tags=("node", "needs-approval"),
                    node_id=node.node_id,
                )
                self._observe_event(
                    workflow.workflow_id,
                    name="node.needs_approval",
                    event_type=TelemetryEventType.NODE,
                    message=result.summary,
                    node_id=node.node_id,
                    severity=TelemetrySeverity.WARNING,
                )
                return

            node.last_error = self._result_error(result)
            workflow.record_event(
                "node.retryable_failure",
                node.last_error,
                node_id=node.node_id,
            )
            self._remember(
                workflow.workflow_id,
                node.last_error,
                tags=("node", "retryable-failure"),
                node_id=node.node_id,
            )
            self._observe_event(
                workflow.workflow_id,
                name="node.retryable_failure",
                event_type=TelemetryEventType.NODE,
                message=node.last_error,
                node_id=node.node_id,
                severity=TelemetrySeverity.WARNING,
            )

        node.status = WorkflowNodeStatus.FAILED
        workflow.status = WorkflowStatus.FAILED
        workflow.record_event(
            "node.failed",
            node.last_error or "Workflow node failed after retries.",
            node_id=node.node_id,
        )
        self._remember(
            workflow.workflow_id,
            node.last_error or "Workflow node failed after retries.",
            tags=("node", "failed"),
            node_id=node.node_id,
        )
        self._observe_event(
            workflow.workflow_id,
            name="node.failed",
            event_type=TelemetryEventType.NODE,
            message=node.last_error or "Workflow node failed after retries.",
            node_id=node.node_id,
            severity=TelemetrySeverity.ERROR,
        )
        self._observe_counter(
            "workflow.node.finished_total",
            workflow.workflow_id,
            node_id=node.node_id,
            labels={"status": WorkflowNodeStatus.FAILED.value},
        )

    def _evaluate_agent_result(
        self,
        *,
        workflow: WorkflowGraph,
        node_id: str,
        agent_id: str,
        result: AgentResult,
    ) -> bool:
        if self.evaluation_service is None:
            return True

        node = workflow.nodes[node_id]
        if node.task is None:
            return True

        report = self.evaluation_service.evaluate_agent_result(
            task=node.task,
            result=result,
            agent_id=agent_id,
            workflow_id=workflow.workflow_id,
            node_id=node.node_id,
        )
        workflow.record_event(
            f"evaluation.{report.status.value}",
            f"Evaluation score={report.overall_score:.2f}; report={report.report_id}",
            node_id=node.node_id,
        )
        self._remember(
            workflow.workflow_id,
            f"Evaluation {report.status.value} with score {report.overall_score:.2f}.",
            tags=("evaluation", report.status.value),
            node_id=node.node_id,
        )
        self._observe_event(
            workflow.workflow_id,
            name=f"evaluation.{report.status.value}",
            event_type=TelemetryEventType.EVALUATION,
            message=f"Evaluation score={report.overall_score:.2f}; report={report.report_id}",
            node_id=node.node_id,
            agent_id=agent_id,
            severity=(
                TelemetrySeverity.INFO
                if report.status == EvaluationStatus.PASSED
                else TelemetrySeverity.WARNING
            ),
            metadata={"report_id": report.report_id, "score": f"{report.overall_score:.2f}"},
        )
        self._observe_counter(
            "evaluation.finished_total",
            workflow.workflow_id,
            node_id=node.node_id,
            labels={"status": report.status.value},
        )

        if not self.evaluation_service.passes_quality_gate(report):
            node.last_error = (
                f"Evaluation quality gate failed: score={report.overall_score:.2f}, "
                f"status={report.status.value}."
            )
            workflow.record_event(
                "evaluation.quality_gate_failed",
                node.last_error,
                node_id=node.node_id,
            )
            self._remember(
                workflow.workflow_id,
                node.last_error,
                tags=("evaluation", "quality-gate-failed"),
                node_id=node.node_id,
            )
            self._observe_event(
                workflow.workflow_id,
                name="evaluation.quality_gate_failed",
                event_type=TelemetryEventType.EVALUATION,
                message=node.last_error,
                node_id=node.node_id,
                agent_id=agent_id,
                severity=TelemetrySeverity.ERROR,
            )
            return False

        if report.status == EvaluationStatus.WARNING:
            workflow.record_event(
                "evaluation.warning_accepted",
                "Evaluation produced warnings but passed the configured quality gate.",
                node_id=node.node_id,
            )
        return True

    def _assess_task_security(
        self,
        workflow: WorkflowGraph,
        node_id: str,
    ) -> SecurityDecisionStatus:
        if self.security_service is None:
            return SecurityDecisionStatus.ALLOW

        node = workflow.nodes[node_id]
        if node.task is None:
            return SecurityDecisionStatus.ALLOW

        decision = self.security_service.assess_task(
            node.task,
            actor_id="workflow-runner",
            approval_granted=node.approval_granted,
        )
        workflow.record_event(
            f"security.{decision.status.value}",
            decision.reason,
            node_id=node.node_id,
        )
        self._remember(
            workflow.workflow_id,
            decision.reason,
            tags=("security", decision.status.value),
            node_id=node.node_id,
        )
        self._observe_event(
            workflow.workflow_id,
            name=f"security.{decision.status.value}",
            event_type=TelemetryEventType.SECURITY,
            message=decision.reason,
            node_id=node.node_id,
            severity=(
                TelemetrySeverity.INFO
                if decision.status == SecurityDecisionStatus.ALLOW
                else TelemetrySeverity.WARNING
            ),
            metadata={"decision_id": decision.decision_id},
        )
        self._observe_counter(
            "security.decision_total",
            workflow.workflow_id,
            node_id=node.node_id,
            labels={"status": decision.status.value},
        )

        if (
            decision.status == SecurityDecisionStatus.BLOCK
            or decision.status == SecurityDecisionStatus.REQUIRES_APPROVAL
        ):
            node.last_error = decision.reason

        return decision.status

    def _remember(
        self,
        workflow_id: str,
        content: str,
        *,
        tags: tuple[str, ...],
        node_id: str | None = None,
    ) -> None:
        if self.memory_service is None:
            return
        self.memory_service.remember_workflow_event(
            workflow_id=workflow_id,
            content=content,
            tags=tags,
            node_id=node_id,
        )

    def _observe_event(
        self,
        workflow_id: str,
        *,
        name: str,
        event_type: TelemetryEventType,
        message: str,
        node_id: str | None = None,
        severity: TelemetrySeverity = TelemetrySeverity.INFO,
        agent_id: str | None = None,
        tool_id: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        if self.observability_service is None:
            return
        self.observability_service.emit_event(
            name=name,
            event_type=event_type,
            severity=severity,
            message=message,
            context=TraceContext.for_workflow(workflow_id, node_id=node_id),
            agent_id=agent_id,
            tool_id=tool_id,
            metadata=metadata or {},
        )

    def _observe_counter(
        self,
        name: str,
        workflow_id: str,
        *,
        node_id: str | None = None,
        labels: dict[str, str] | None = None,
        value: float = 1.0,
    ) -> None:
        if self.observability_service is None:
            return
        self.observability_service.increment_counter(
            name=name,
            value=value,
            context=TraceContext.for_workflow(workflow_id, node_id=node_id),
            labels=labels or {},
        )

    @staticmethod
    def _result_summary(result: AgentResult) -> str:
        return result.summary.strip() or f"Agent returned status {result.status.value}."

    @staticmethod
    def _result_error(result: AgentResult) -> str:
        if result.errors:
            return "; ".join(result.errors)
        return result.summary.strip() or f"Agent returned status {result.status.value}."
