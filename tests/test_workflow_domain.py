from __future__ import annotations

import pytest

from agentforge.domain.entities import ProjectTask
from agentforge.domain.value_objects import Capability
from agentforge.domain.workflow import WorkflowDomainError, WorkflowGraph, WorkflowNode


def test_workflow_graph_returns_ready_nodes_when_dependencies_completed() -> None:
    first = WorkflowNode(
        node_id="first",
        title="Plan",
        task=ProjectTask(title="Plan", required_capabilities=(Capability("planning"),)),
    )
    second = WorkflowNode(
        node_id="second",
        title="Review",
        dependencies=("first",),
    )
    graph = WorkflowGraph(name="Example", nodes={"first": first, "second": second})

    ready = graph.ready_nodes()

    assert tuple(node.node_id for node in ready) == ("first",)


def test_workflow_graph_rejects_unknown_dependency() -> None:
    node = WorkflowNode(node_id="node", title="Task", dependencies=("missing",))

    with pytest.raises(WorkflowDomainError, match="unknown dependencies"):
        WorkflowGraph(name="Invalid", nodes={"node": node})


def test_workflow_graph_rejects_dependency_cycles() -> None:
    first = WorkflowNode(node_id="first", title="First", dependencies=("second",))
    second = WorkflowNode(node_id="second", title="Second", dependencies=("first",))

    with pytest.raises(WorkflowDomainError, match="dependency cycles"):
        WorkflowGraph(name="Invalid", nodes={"first": first, "second": second})
