from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_submission_package_files_exist() -> None:
    required = [
        "submissions/README.md",
        "submissions/PROJECT_CARD.md",
        "submissions/KAGGLE_SUBMISSION.md",
        "submissions/DEMO_GUIDE.md",
        "submissions/TECHNICAL_ARCHITECTURE_SUMMARY.md",
        "submissions/EVALUATION_EVIDENCE.md",
        "submissions/CAPSTONE_CHECKLIST.md",
        "submissions/ARTIFACT_MANIFEST.md",
        "submissions/PRESENTATION_OUTLINE.md",
        "submissions/VIDEO_STORYBOARD.md",
        "submissions/JUDGE_WALKTHROUGH.md",
        "examples/capstone_demo_project/project_request.md",
        "examples/capstone_demo_project/demo_run.json",
        "examples/capstone_demo_project/expected_workflow.md",
    ]
    for relative_path in required:
        assert (ROOT / relative_path).is_file(), relative_path


def test_submission_narrative_is_capability_first() -> None:
    kaggle_submission = (ROOT / "submissions/KAGGLE_SUBMISSION.md").read_text(encoding="utf-8")
    assert "capability-first" in kaggle_submission.lower()
    assert "plugin-first" in kaggle_submission.lower()
    assert "hardcoded" in kaggle_submission.lower()


def test_demo_run_is_completed() -> None:
    import json

    demo = json.loads(
        (ROOT / "examples/capstone_demo_project/demo_run.json").read_text(encoding="utf-8")
    )
    assert demo["status"] == "completed"
    event_types = {event["event_type"] for event in demo["events"]}
    assert "workflow.started" in event_types
    assert "security.allow" in event_types
    assert "evaluation.passed" in event_types
    assert "workflow.completed" in event_types
