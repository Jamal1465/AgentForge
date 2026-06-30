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


def test_library_management_for_university_generation(platform: AgentForgePlatform) -> None:
    """Test 1, 2, 3, 4: Verify detailed domain-specific output for 'Library Management For University'."""
    summary = platform.run_project_request("Library Management For University")

    assert summary.status == "completed"
    assert summary.error is None

    stored = platform.workflow_store.get(summary.workflow_id)

    # Banned terms list
    banned_terms = [
        "task crud",
        "task priority",
        "task status",
        "task manager",
        "todo",
        "generic task",
        "interacts with the system in a designated role",
        "reference implementation",
        "tight coupling",
        "lack of unit test coverage",
        "incomplete deployment configurations",
    ]

    # Test 1: Project Brief Assertions
    brief_node = stored.nodes["01_project_brief"]
    brief_content = brief_node.artifacts[0].content
    assert "university library" in brief_content.lower()
    assert "book catalog" in brief_content.lower()
    assert "borrowing" in brief_content.lower()
    assert "returns" in brief_content.lower()
    assert "reservations" in brief_content.lower()
    assert "overdue fines" in brief_content.lower()
    assert "Student" in brief_content
    assert "Faculty Member" in brief_content
    assert "Librarian" in brief_content
    assert "Administrator" in brief_content

    for term in banned_terms:
        assert term not in brief_content.lower(), f"Brief contains banned term: {term}"

    # Test 2: Functional Requirements Assertions
    req_node = stored.nodes["02_functional_requirements"]
    req_content = req_node.artifacts[0].content
    assert "Issue Book" in req_content
    assert "Return Book" in req_content
    assert "Renew Loan" in req_content
    assert "Reserve Book" in req_content
    assert "Overdue Fine" in req_content
    assert "Book Copy" in req_content
    assert "Catalog Search" in req_content or "search" in req_content.lower()
    assert "Audit Log" in req_content

    assert "task crud" not in req_content.lower()
    assert "task priority" not in req_content.lower()
    assert "task status" not in req_content.lower()

    for term in banned_terms:
        assert term not in req_content.lower(), f"FR contains banned term: {term}"

    # Test 3: Non-Functional Requirements Assertions
    nfr_node = stored.nodes["03_non_functional_requirements"]
    nfr_content = nfr_node.artifacts[0].content
    assert "catalog search latency" in nfr_content.lower()
    assert "loan transaction atomicity" in nfr_content.lower()
    assert "book copy inventory consistency" in nfr_content.lower()
    assert "auditability of issue/return transactions" in nfr_content.lower()

    # Test 4: Feasibility Study Assertions
    feas_node = stored.nodes["04_feasibility_study"]
    feas_content = feas_node.artifacts[0].content
    assert "catalog indexing" in feas_content.lower()
    assert "circulation workflow" in feas_content.lower() or "circulation" in feas_content.lower()
    assert "librarian workflow" in feas_content.lower() or "librarian" in feas_content.lower()
    assert "student/faculty self-service" in feas_content.lower() or "self-service" in feas_content.lower()
    assert "fine calculation" in feas_content.lower()
    assert "reservation conflicts" in feas_content.lower()


def test_ecommerce_store_generation(platform: AgentForgePlatform) -> None:
    """Test 5: Verify Ecommerce Store output containing correct details and no library terms."""
    summary = platform.run_project_request("Ecommerce Store")

    assert summary.status == "completed"
    assert summary.error is None

    stored = platform.workflow_store.get(summary.workflow_id)

    # Gather all generated artifact content text
    all_content = ""
    for node in stored.nodes.values():
        for art in node.artifacts:
            all_content += "\n" + art.content

    # Inclusions
    assert "Customer" in all_content
    assert "Merchant" in all_content or "Store Admin" in all_content
    assert "Product Catalog" in all_content or "product" in all_content.lower()
    assert "Shopping Cart" in all_content or "cart" in all_content.lower()
    assert "Checkout" in all_content
    assert "Payment" in all_content
    assert "Order Fulfillment" in all_content or "order" in all_content.lower()
    assert "Inventory" in all_content

    # Library exclusions
    assert "librarian" not in all_content.lower()
    assert "book copy" not in all_content.lower()
    assert "loan" not in all_content.lower()
    assert "overdue fine" not in all_content.lower()


def test_hospital_management_generation(platform: AgentForgePlatform) -> None:
    """Test 6: Verify Hospital Management System output inclusions."""
    summary = platform.run_project_request("Hospital Management System")

    assert summary.status == "completed"
    assert summary.error is None

    stored = platform.workflow_store.get(summary.workflow_id)

    # Gather all generated artifact content text
    all_content = ""
    for node in stored.nodes.values():
        for art in node.artifacts:
            all_content += "\n" + art.content

    # Inclusions
    assert "Patient" in all_content
    assert "Doctor" in all_content
    assert "Appointment" in all_content
    assert "Medical Record" in all_content or "emr" in all_content.lower()
    assert "Billing" in all_content
    assert "Prescription" in all_content


def test_domain_pack_matching(platform: AgentForgePlatform) -> None:
    """Verify different user inputs resolve to correct domain packs."""
    from agentforge.domain_analysis.domain_analyzer import DomainAnalyzer

    analyzer = DomainAnalyzer()

    ctx_lib = analyzer.analyze("I want to construct a online school library catalog system")
    assert ctx_lib.normalized_domain == "library-management"
    assert "Student" in ctx_lib.actors

    ctx_shop = analyzer.analyze("Build an online t-shirt shop store with payment gateway")
    assert ctx_shop.normalized_domain == "ecommerce"
    assert "Customer" in ctx_shop.actors

    ctx_hospital = analyzer.analyze("Create a clinic appointment portal for patients")
    assert ctx_hospital.normalized_domain == "hospital-management"
    assert "Patient" in ctx_hospital.actors

    ctx_lms = analyzer.analyze("Develop a course training learning management system")
    assert ctx_lms.normalized_domain == "learning-management-system"
    assert "Course" in ctx_lms.entities

    ctx_task = analyzer.analyze("Set up a project sprint task tracker kanban board")
    assert ctx_task.normalized_domain == "task-management"

    ctx_inv = analyzer.analyze("Warehouse stock reorder purchase order manager")
    assert ctx_inv.normalized_domain == "inventory-management"
    assert "SKU" in ctx_inv.validation_rules[0]

    ctx_generic = analyzer.analyze("A custom data entry app for organizing files")
    assert ctx_generic.normalized_domain == "generic-business-app"
