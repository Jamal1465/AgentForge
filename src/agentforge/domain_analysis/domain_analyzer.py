"""Domain Analyzer service to infer project domain context."""

from __future__ import annotations

import re
from typing import Final

from agentforge.domain_analysis.domain_context import DomainContext
from agentforge.domain_analysis.domain_packs import DOMAIN_PACKS

# Keyword lists for domain matching
KEYWORDS_LIBRARY: Final[list[str]] = ["library", "book", "catalog", "isbn", "borrow", "librarian"]
KEYWORDS_TASK: Final[list[str]] = ["task", "todo", "kanban", "sprint", "project management"]
KEYWORDS_ECOMMERCE: Final[list[str]] = ["shop", "store", "product", "cart", "order", "payment", "checkout", "e-commerce", "ecommerce"]
KEYWORDS_LMS: Final[list[str]] = ["course", "lms", "lesson", "quiz", "enroll", "instructor", "learning management"]
KEYWORDS_HOSPITAL: Final[list[str]] = ["hospital", "patient", "doctor", "appointment", "clinic", "medical", "prescribe", "prescription"]
KEYWORDS_INVENTORY: Final[list[str]] = ["inventory", "warehouse", "stock", "supplier", "purchase order"]


class DomainAnalyzer:
    """Analyzes a project request description to identify the domain pack."""

    def analyze(self, description: str) -> DomainContext:
        """Scan description for keywords and return the matched DomainContext."""
        desc_lower = description.lower()

        # Check in order of specificity
        if any(kw in desc_lower for kw in KEYWORDS_LIBRARY):
            matched_key = "library-management"
        elif any(kw in desc_lower for kw in KEYWORDS_LMS):
            matched_key = "learning-management-system"
        elif any(kw in desc_lower for kw in KEYWORDS_HOSPITAL):
            matched_key = "hospital-management"
        elif any(kw in desc_lower for kw in KEYWORDS_INVENTORY):
            matched_key = "inventory-management"
        elif any(kw in desc_lower for kw in KEYWORDS_ECOMMERCE):
            matched_key = "ecommerce"
        elif any(kw in desc_lower for kw in KEYWORDS_TASK):
            matched_key = "task-management"
        else:
            matched_key = "generic-business-app"

        template_ctx = DOMAIN_PACKS[matched_key]

        # Clean project name based on description if possible
        # e.g., "Build a library Management System" -> "Library Management System"
        project_name = template_ctx.project_name
        clean_match = re.search(
            r"(?:build|create|make|develop)\s+(?:a\s+|an\s+)?([^.]+)",
            description,
            re.IGNORECASE,
        )
        if clean_match:
            candidate = clean_match.group(1).strip()
            # If the candidate looks like a short title (under 50 chars), use it title-cased
            if 3 < len(candidate) < 60:
                project_name = candidate.title()

        # Re-instantiate with custom project name for this run
        return DomainContext(
            project_name=project_name,
            normalized_domain=template_ctx.normalized_domain,
            domain_summary=template_ctx.domain_summary,
            actors=list(template_ctx.actors),
            entities=list(template_ctx.entities),
            workflows=list(template_ctx.workflows),
            modules=list(template_ctx.modules),
            business_rules=list(template_ctx.business_rules),
            api_resources=list(template_ctx.api_resources),
            database_tables=list(template_ctx.database_tables),
            reports=list(template_ctx.reports),
            risks=list(template_ctx.risks),
            assumptions=list(template_ctx.assumptions),
            out_of_scope=list(template_ctx.out_of_scope),
            functional_requirements=list(template_ctx.functional_requirements),
            validation_rules=list(template_ctx.validation_rules),
            edge_cases=list(template_ctx.edge_cases),
            request_response_examples=template_ctx.request_response_examples,
            authorization_matrix=template_ctx.authorization_matrix,
            traceability_matrix=template_ctx.traceability_matrix,
        )
