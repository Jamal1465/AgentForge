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
KEYWORDS_SCHOOL: Final[list[str]] = ["school", "student", "teacher", "parent", "principal", "timetable", "report card"]
KEYWORDS_GYM: Final[list[str]] = ["gym", "workout", "fitness", "trainer", "membership"]
KEYWORDS_HOSTEL: Final[list[str]] = ["hostel", "dorm", "warden", "complaint"]
KEYWORDS_CAR_RENTAL: Final[list[str]] = ["car", "vehicle", "rent", "hire", "rental"]
KEYWORDS_BLOOD_DONATION: Final[list[str]] = ["blood", "donor", "donation"]


class DomainAnalyzer:
    """Analyzes a project request description to identify the domain pack."""

    def analyze(self, description: str) -> DomainContext:
        """Scan description for keywords and return the matched DomainContext."""
        desc_lower = description.lower()

        # Clean project name based on description if possible
        project_name = "Generated Project"
        clean_match = re.search(
            r"(?:build|create|make|develop|design)\s+(?:a\s+|an\s+)?([^.]+)",
            description,
            re.IGNORECASE,
        )
        if clean_match:
            candidate = clean_match.group(1).strip()
            if 3 < len(candidate) < 60:
                project_name = candidate.title()
        else:
            # Fall back to description if short
            if 3 < len(description) < 60:
                project_name = description.strip().title()

        # Check if Gemini/LLM is configured
        import os
        gemini_api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if gemini_api_key:
            try:
                import json

                import google.generativeai as genai  # type: ignore[import-untyped]
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"""Analyze this project description: "{description}" (name: "{project_name}").
Generate a complete, domain-specific, industry-standard DomainContext JSON object.
Do NOT use generic boilerplate sentences such as:
- "The goal is to build a robust system"
- "interacts with the system in a designated role"
- "tight coupling"
- "lack of unit test coverage"
- "reference implementation"
- "core domain manager"
- "task CRUD"

Ensure every paragraph or list item is fully customized for the target domain (e.g. if the domain is a gym, use member, trainer, membership plan; if a hostel, warden, resident, room, complaint).
Every sentence must contain at least one domain-specific concept.

Return a JSON object matching this schema exactly:
{{
    "project_name": "...",
    "normalized_domain": "...",
    "domain_type": "...",
    "domain_summary": "...",
    "institution_context": "...",
    "primary_users": ["..."],
    "secondary_users": ["..."],
    "actors_with_responsibilities": {{ "actor1": "responsibility1", ... }},
    "domain_problems": ["problem1", "problem2", ...],
    "business_goals": ["goal1", "goal2", ...],
    "measurable_success_criteria": ["criteria1", ...],
    "entities": ["entity1", ...],
    "workflows": ["workflow1", ...],
    "modules": ["module1", ...],
    "business_rules": ["rule1", ...],
    "functional_requirements": ["FR-001 ...", ...],
    "non_functional_requirements": ["NFR-001 ...", ...],
    "feasibility_points": {{ "technical": "...", "operational": "...", "economic": "...", "schedule": "...", "legal": "..." }},
    "api_resources": ["/api/v1/...", ...],
    "database_tables": ["table1", ...],
    "reports": ["report1", ...],
    "risks": ["risk1", ...],
    "assumptions": ["assumption1", ...],
    "constraints": ["constraint1", ...],
    "out_of_scope": ["outofscope1", ...]
}}
"""
                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                data = json.loads(response.text)
                return DomainContext(
                    project_name=data.get("project_name", project_name),
                    normalized_domain=data.get("normalized_domain", "custom-domain"),
                    domain_type=data.get("domain_type", "Custom Domain"),
                    domain_summary=data.get("domain_summary", "Custom system operations."),
                    institution_context=data.get("institution_context", "Custom Organization Environment"),
                    primary_users=data.get("primary_users", ["User"]),
                    secondary_users=data.get("secondary_users", ["Administrator"]),
                    actors_with_responsibilities=data.get("actors_with_responsibilities", {}),
                    domain_problems=data.get("domain_problems", []),
                    business_goals=data.get("business_goals", []),
                    measurable_success_criteria=data.get("measurable_success_criteria", []),
                    entities=data.get("entities", []),
                    workflows=data.get("workflows", []),
                    modules=data.get("modules", []),
                    business_rules=data.get("business_rules", []),
                    functional_requirements=data.get("functional_requirements", []),
                    non_functional_requirements=data.get("non_functional_requirements", []),
                    feasibility_points=data.get("feasibility_points", {}),
                    api_resources=data.get("api_resources", []),
                    database_tables=data.get("database_tables", []),
                    reports=data.get("reports", []),
                    risks=data.get("risks", []),
                    assumptions=data.get("assumptions", []),
                    constraints=data.get("constraints", []),
                    out_of_scope=data.get("out_of_scope", []),
                )
            except Exception:
                pass

        # Deterministic heuristic matching
        matched_key = ""
        if any(kw in desc_lower for kw in KEYWORDS_SCHOOL):
            matched_key = "school-management"
        elif any(kw in desc_lower for kw in KEYWORDS_GYM):
            matched_key = "gym-membership"
        elif any(kw in desc_lower for kw in KEYWORDS_HOSTEL):
            matched_key = "hostel-complaint"
        elif any(kw in desc_lower for kw in KEYWORDS_CAR_RENTAL):
            matched_key = "car-rental"
        elif any(kw in desc_lower for kw in KEYWORDS_BLOOD_DONATION):
            matched_key = "blood-donation"
        elif any(kw in desc_lower for kw in KEYWORDS_LIBRARY):
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

        if matched_key:
            template_ctx = DOMAIN_PACKS[matched_key]
            # Use candidate title if found, otherwise keep template project name
            p_name = project_name if project_name != "Generated Project" else template_ctx.project_name
            return DomainContext(
                project_name=p_name,
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

        # Fully dynamic heuristic generation for completely unseen domains
        # 1. Clean project name
        if project_name == "Generated Project":
            # Guess from input
            project_name = description.strip().title()
        
        # 2. Extract domain noun phrase
        subject_singular = "Business Process"
        # Match singular subject (e.g. Restaurant System -> Restaurant)
        candidate_clean = re.sub(r"\s+(?:system|platform|app|portal|service|software|application|manager|tracker)$", "", project_name, flags=re.IGNORECASE).strip()
        if candidate_clean:
            subject_singular = candidate_clean.title()

        norm = re.sub(r"[^a-z0-9]+", "-", subject_singular.lower()).strip("-")
        if not norm:
            norm = "custom-business-app"

        # 3. Dynamic domain generation
        domain_type = f"{subject_singular} Management"
        domain_summary = f"The {subject_singular} Management System coordinates {subject_singular.lower()} lifecycle tracking, client registration, operational workflows, and payment record checking."
        institution_context = f"{subject_singular} Operations and Compliance Environment"
        
        primary_user = f"{subject_singular} Client"
        secondary_user = f"{subject_singular} Operator"
        admin_user = f"{subject_singular} Administrator"

        actors_with_responsibilities = {
            primary_user: f"interacts with the {subject_singular.lower()} catalog, requests services, and views transaction statuses.",
            secondary_user: f"manages active {subject_singular.lower()} operations, verifies client credentials, and logs statuses.",
            admin_user: f"configures core {subject_singular.lower()} policies, reviews reporting dashboards, and manages staff roles.",
        }

        domain_problems = [
            f"Lack of centralized tracking for active {subject_singular.lower()} operational states.",
            "Inconsistent registration details and manual data logging errors.",
            "Slow check queries and delay in status transitions.",
        ]

        business_goals = [
            f"Digitize all {subject_singular.lower()} records and client details.",
            "Automate daily operational workflows and check-ins.",
            f"Ensure transaction consistency across active {subject_singular.lower()} statuses.",
            "Provide role-based secure login dashboards.",
        ]

        measurable_success_criteria = [
            f"{subject_singular} record search query response times remain under 250ms.",
            "100% of status transitions are logged in the audit trail ledger.",
            "Zero duplicate transactions are allowed for the same active client.",
        ]

        entities = [
            "Client Profile",
            f"{subject_singular} Record",
            f"{subject_singular} Transaction",
            "Status Change Log",
            "Payment Log",
            "Compliance Audit Trail",
        ]

        workflows = [
            "Register client profile",
            f"Add new {subject_singular.lower()} record",
            f"Initiate {subject_singular.lower()} transaction",
            "Verify transaction state details",
            "Update status transition logs",
            "Generate operational ledger",
        ]

        modules = [
            "Client Directory Management",
            f"{subject_singular} Core Registry",
            "Transaction State Control",
            "Reporting and Metrics",
            "Access Security Audits",
        ]

        business_rules = [
            f"{subject_singular} transactions require active client profiles.",
            "Only authorized staff operators can update status logs and close active transactions.",
            "Record updates are logged for auditing.",
        ]

        functional_requirements = [
            "FR-001 Client Registration and Portals",
            f"FR-002 {subject_singular} Registry and Catalog",
            "FR-003 Transaction Flow Processing",
            "FR-004 Status Change Notifications",
            "FR-005 Performance Reporting",
        ]

        non_functional_requirements = [
            f"{subject_singular} query response times stay under 250ms.",
            "Transaction consistency across status states.",
            "Enforcement of access controls on client record updates.",
        ]

        feasibility_points = {
            "technical": f"Highly feasible. Standard relational database operations handle {subject_singular.lower()} logs and transaction states.",
            "operational": "Replaces manual tracking with automated workflows, enhancing staff productivity.",
            "economic": "Reduces administrative hours and data entry errors.",
            "schedule": "4-week phased delivery.",
            "legal": "Ensures compliance with basic data privacy guidelines.",
        }

        api_resources = [
            "/api/v1/auth",
            "/api/v1/clients",
            f"/api/v1/{norm}s",
            "/api/v1/transactions",
            "/api/v1/reports",
        ]

        database_tables = [
            "users",
            "roles",
            "clients",
            f"{norm}_records",
            "transactions",
            "audit_logs",
        ]

        reports = [
            f"Daily {subject_singular} Utilization Summary",
            "Transaction Ledger",
            "Audit Access Logs",
        ]

        risks = [
            f"Discrepancies in active {subject_singular.lower()} states due to concurrent modifications.",
            "Unauthorized access to sensitive client record logs.",
            "Failed status updates due to network connection issues.",
        ]

        assumptions = [
            "Users have web browsers.",
            "Data network is reliable.",
        ]

        constraints = [
            "Authentication must integrate with role-based policies.",
        ]

        out_of_scope = [
            "Direct physical shipment logistics.",
            "Third-party ERP software integrations.",
        ]

        return DomainContext(
            project_name=project_name,
            normalized_domain=norm,
            domain_summary=domain_summary,
            institution_context=institution_context,
            primary_users=[primary_user, secondary_user],
            secondary_users=[admin_user],
            actors_with_responsibilities=actors_with_responsibilities,
            domain_problems=domain_problems,
            business_goals=business_goals,
            measurable_success_criteria=measurable_success_criteria,
            entities=entities,
            workflows=workflows,
            modules=modules,
            business_rules=business_rules,
            functional_requirements=functional_requirements,
            non_functional_requirements=non_functional_requirements,
            feasibility_points=feasibility_points,
            api_resources=api_resources,
            database_tables=database_tables,
            reports=reports,
            risks=risks,
            assumptions=assumptions,
            constraints=constraints,
            out_of_scope=out_of_scope,
            domain_type=domain_type,
            primary_problem=domain_problems[0],
            target_users=[primary_user, secondary_user, admin_user],
            core_entities=entities,
            core_workflows=workflows,
            domain_risks=risks,
        )
