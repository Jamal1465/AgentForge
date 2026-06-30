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


def test_domain_aware_library_system_generation(platform: AgentForgePlatform) -> None:
    """Test that a Library Management System input generates domain-appropriate docs."""
    summary = platform.run_project_request("Build a library Management System")

    assert summary.status == "completed"
    assert summary.error is None

    # Retrieve stored workflow graph to inspect nodes
    stored = platform.workflow_store.get(summary.workflow_id)

    # 1. Assert Project Brief target users / actors
    brief_node = stored.nodes["01_project_brief"]
    brief_content = brief_node.artifacts[0].content
    assert "Student" in brief_content
    assert "Faculty" in brief_content
    assert "Librarian" in brief_content
    assert "Administrator" in brief_content

    # 2. Assert 02_functional_requirements content
    req_node = stored.nodes["02_functional_requirements"]
    assert len(req_node.artifacts) == 1
    req_content = req_node.artifacts[0].content

    # Assert correct domain-specific inclusions
    assert "Student" in req_content
    assert "Faculty" in req_content
    assert "Librarian" in req_content
    assert "Administrator" in req_content
    assert "Book" in req_content
    assert "Issue Book" in req_content
    assert "Return Book" in req_content
    assert "Reservation" in req_content
    assert "Fine" in req_content

    # Assert wrong-domain words are not present
    wrong_words = [
        "task crud",
        "task priority",
        "task status",
        "task manager",
        "todo",
        "generic task",
    ]
    for word in wrong_words:
        assert word not in req_content.lower()

    # 3. Assert 05_system_architecture content
    arch_node = stored.nodes["05_system_architecture"]
    assert len(arch_node.artifacts) == 1
    arch_content = arch_node.artifacts[0].content

    assert "Catalog Service" in arch_content
    assert "Circulation Service" in arch_content
    assert "Reservation Service" in arch_content
    assert "Fine Service" in arch_content

    # Assert SQL database tables
    assert "books" in arch_content.lower()
    assert "book_copies" in arch_content.lower()
    assert "loans" in arch_content.lower()
    assert "reservations" in arch_content.lower()
    assert "fines" in arch_content.lower()


def test_domain_aware_ecommerce_generation(platform: AgentForgePlatform) -> None:
    """Test that an Ecommerce Store input generates domain-appropriate docs."""
    summary = platform.run_project_request("Ecommerce Store")

    assert summary.status == "completed"
    assert summary.error is None

    # Retrieve stored workflow graph to inspect nodes
    stored = platform.workflow_store.get(summary.workflow_id)

    # 1. Assert Project Brief target users / actors
    brief_node = stored.nodes["01_project_brief"]
    brief_content = brief_node.artifacts[0].content
    assert "Customer" in brief_content
    assert "Merchant" in brief_content

    # 2. Assert 02_functional_requirements content
    req_node = stored.nodes["02_functional_requirements"]
    assert len(req_node.artifacts) == 1
    req_content = req_node.artifacts[0].content

    # Assert correct domain-specific inclusions
    assert "Customer" in req_content
    assert "Merchant" in req_content
    assert "Product" in req_content
    assert "Cart" in req_content
    assert "Checkout" in req_content
    assert "Payment" in req_content
    assert "Order" in req_content
    assert "Inventory" in req_content

    # Assert wrong-domain words are not present
    wrong_words = [
        "task crud",
        "task priority",
        "task status",
        "task manager",
        "todo",
        "generic task",
    ]
    for word in wrong_words:
        assert word not in req_content.lower()

    # 3. Assert 05_system_architecture content
    arch_node = stored.nodes["05_system_architecture"]
    assert len(arch_node.artifacts) == 1
    arch_content = arch_node.artifacts[0].content

    assert "Product" in arch_content
    assert "Cart" in arch_content
    assert "Order" in arch_content
    assert "Payment" in arch_content

    # Assert SQL database tables
    assert "products" in arch_content.lower()
    assert "orders" in arch_content.lower()
    assert "payments" in arch_content.lower()
    assert "carts" in arch_content.lower()


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
    assert "Sprint" in ctx_task.entities

    ctx_inv = analyzer.analyze("Warehouse stock reorder purchase order manager")
    assert ctx_inv.normalized_domain == "inventory-management"
    assert "SKU" in ctx_inv.validation_rules[0]

    ctx_generic = analyzer.analyze("A custom data entry app for organizing files")
    assert ctx_generic.normalized_domain == "generic-business-app"
