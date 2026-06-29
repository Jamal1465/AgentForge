from __future__ import annotations

from agentforge.interfaces.cli.main import run_create


def test_run_create_can_return_json() -> None:
    output = run_create("Build a portfolio app", as_json=True)

    assert '"status": "completed"' in output
    assert '"executed_node_ids"' in output
