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
        project_name = template_ctx.project_name
        clean_match = re.search(
            r"(?:build|create|make|develop)\s+(?:a\s+|an\s+)?([^.]+)",
            description,
            re.IGNORECASE,
        )
        if clean_match:
            candidate = clean_match.group(1).strip()
            # If the candidate looks like a short title (under 60 chars), use it title-cased
            if 3 < len(candidate) < 60:
                project_name = candidate.title()

        # Re-instantiate with custom project name and copy all domain properties
        return DomainContext(
            project_name=project_name,
            normalized_domain=template_ctx.normalized_domain,
            domain_summary=template_ctx.domain_summary,
            institution_context=template_ctx.institution_context,
            primary_users=list(template_ctx.primary_users),
            secondary_users=list(template_ctx.secondary_users),
            actors_with_responsibilities=dict(template_ctx.actors_with_responsibilities),
            domain_problems=list(template_ctx.domain_problems),
            business_goals=list(template_ctx.business_goals),
            measurable_success_criteria=list(template_ctx.measurable_success_criteria),
            entities=list(template_ctx.entities),
            workflows=list(template_ctx.workflows),
            modules=list(template_ctx.modules),
            business_rules=list(template_ctx.business_rules),
            functional_requirements=list(template_ctx.functional_requirements),
            non_functional_requirements=list(template_ctx.non_functional_requirements),
            feasibility_points=dict(template_ctx.feasibility_points),
            api_resources=list(template_ctx.api_resources),
            database_tables=list(template_ctx.database_tables),
            reports=list(template_ctx.reports),
            risks=list(template_ctx.risks),
            assumptions=list(template_ctx.assumptions),
            constraints=list(template_ctx.constraints),
            out_of_scope=list(template_ctx.out_of_scope),
            actors=list(template_ctx.actors),
            validation_rules=list(template_ctx.validation_rules),
            edge_cases=list(template_ctx.edge_cases),
            request_response_examples=template_ctx.request_response_examples,
            authorization_matrix=template_ctx.authorization_matrix,
            traceability_matrix=template_ctx.traceability_matrix,
        )
