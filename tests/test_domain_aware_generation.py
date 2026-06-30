"""Automated tests for domain-aware documentation generation in AgentForge."""

from __future__ import annotations

import pytest

from agentforge.application.platform import AgentForgePlatform
from agentforge.infrastructure.config import AgentForgeSettings, RuntimeEnvironment


@pytest.fixture()
def platform() -> AgentForgePlatform:
    """Create default test platform."""
    settings = AgentForgeSettings(environment=RuntimeEnvironment.TEST)
    return AgentForgePlatform.create_default(settings=settings)


# Banned global filler terms
BANNED_FILLERS = [
    "the goal is to build a robust system",
    "interacts with the system in a designated role",
    "reference implementation",
    "tight coupling",
    "lack of unit test coverage",
    "incomplete deployment configurations",
    "core domain manager",
]


def assert_domain_specific_artifacts(stored: any, inclusions: list[str], exclusions: list[str]) -> None:
    """Helper to verify that generated files are domain-specific and exclude banned/wrong-domain terms."""
    # Retrieve artifacts
    brief_content = stored.nodes["01_project_brief"].artifacts[0].content
    fr_content = stored.nodes["02_functional_requirements"].artifacts[0].content
    feas_content = stored.nodes["04_feasibility_study"].artifacts[0].content

    # Check inclusions
    for inc in inclusions:
        assert inc.lower() in brief_content.lower(), f"Brief missing domain term: {inc}"
        assert inc.lower() in fr_content.lower(), f"FR missing domain term: {inc}"
        # Feasibility study is high-level, verify relevant key terms
        if inc.lower() not in feas_content.lower():
            # Check if at least one of the major domain nouns is present
            found_any = any(word.lower() in feas_content.lower() for word in inclusions)
            assert found_any, f"Feasibility Study does not contain any of the domain terms: {inclusions}"

    # Check exclusions (wrong-domain terms)
    for exc in exclusions:
        assert exc.lower() not in brief_content.lower(), f"Brief contains wrong-domain term: {exc}"
        assert exc.lower() not in fr_content.lower(), f"FR contains wrong-domain term: {exc}"
        assert exc.lower() not in feas_content.lower(), f"Feasibility contains wrong-domain term: {exc}"

    # Check global banned fillers
    for filler in BANNED_FILLERS:
        assert filler.lower() not in brief_content.lower(), f"Brief contains global banned filler: {filler}"
        assert filler.lower() not in fr_content.lower(), f"FR contains global banned filler: {filler}"
        assert filler.lower() not in feas_content.lower(), f"Feasibility contains global banned filler: {filler}"


def test_school_management_generation(platform: AgentForgePlatform) -> None:
    """Test 1: Verify School Management System output."""
    summary = platform.run_project_request("School Management System")
    assert summary.status == "completed"
    assert summary.error is None

    stored = platform.workflow_store.get(summary.workflow_id)

    inclusions = [
        "Student",
        "Teacher",
        "Parent",
        "Attendance",
        "Exam",
        "Fee",
        "Timetable",
        "Report Card",
    ]
    exclusions = [
        "task crud",
        "book copy",
        "shopping cart",
        "patient record",
    ]
    assert_domain_specific_artifacts(stored, inclusions, exclusions)


def test_gym_membership_generation(platform: AgentForgePlatform) -> None:
    """Test 2: Verify Gym Membership Management System output."""
    summary = platform.run_project_request("Gym Membership Management System")
    assert summary.status == "completed"
    assert summary.error is None

    stored = platform.workflow_store.get(summary.workflow_id)

    inclusions = [
        "Member",
        "Trainer",
        "Membership Plan",
        "Workout Schedule",
        "Payment",
        "Attendance",
    ]
    exclusions = [
        "student attendance",
        "book loan",
        "shopping cart",
    ]
    assert_domain_specific_artifacts(stored, inclusions, exclusions)


def test_hostel_complaint_generation(platform: AgentForgePlatform) -> None:
    """Test 3: Verify Hostel Complaint Management System output."""
    summary = platform.run_project_request("Hostel Complaint Management System")
    assert summary.status == "completed"
    assert summary.error is None

    stored = platform.workflow_store.get(summary.workflow_id)

    inclusions = [
        "Resident",
        "Warden",
        "Room",
        "Complaint",
        "Maintenance Staff",
        "Complaint Status",
    ]
    exclusions = [
        "task crud",
        "task priority",
        "task status",
        "task manager",
        "todo",
        "generic task",
    ]
    assert_domain_specific_artifacts(stored, inclusions, exclusions)


def test_car_rental_generation(platform: AgentForgePlatform) -> None:
    """Test 4: Verify Car Rental Platform output."""
    summary = platform.run_project_request("Car Rental Platform")
    assert summary.status == "completed"
    assert summary.error is None

    stored = platform.workflow_store.get(summary.workflow_id)

    inclusions = [
        "Customer",
        "Vehicle",
        "Booking",
        "Rental Period",
        "Payment",
        "Return Inspection",
    ]
    exclusions = [
        "librarian",
        "student",
        "patient",
    ]
    assert_domain_specific_artifacts(stored, inclusions, exclusions)


def test_blood_donation_generation(platform: AgentForgePlatform) -> None:
    """Test 5: Verify Blood Donation Management System output."""
    summary = platform.run_project_request("Blood Donation Management System")
    assert summary.status == "completed"
    assert summary.error is None

    stored = platform.workflow_store.get(summary.workflow_id)

    inclusions = [
        "Donor",
        "Blood Group",
        "Donation Camp",
        "Blood Inventory",
        "Recipient Request",
    ]
    exclusions = [
        "shopping cart",
        "checkout",
        "book copy",
    ]
    assert_domain_specific_artifacts(stored, inclusions, exclusions)


def test_ecommerce_generation(platform: AgentForgePlatform) -> None:
    """Test 6: Verify Ecommerce Store output."""
    summary = platform.run_project_request("Ecommerce Store")
    assert summary.status == "completed"
    assert summary.error is None

    stored = platform.workflow_store.get(summary.workflow_id)

    inclusions = [
        "Customer",
        "Product",
        "Cart",
        "Checkout",
        "Payment",
        "Order",
        "Inventory",
    ]
    exclusions = [
        "librarian",
        "book copy",
        "loan",
        "overdue fine",
    ]
    assert_domain_specific_artifacts(stored, inclusions, exclusions)
