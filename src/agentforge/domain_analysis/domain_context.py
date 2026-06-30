"""Domain Context definition for AgentForge."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DomainContext:
    """Stores inferred domain information for generation."""

    project_name: str
    normalized_domain: str
    domain_summary: str
    institution_context: str = ""
    primary_users: list[str] = field(default_factory=list)
    secondary_users: list[str] = field(default_factory=list)
    actors_with_responsibilities: dict[str, str] = field(default_factory=dict)
    domain_problems: list[str] = field(default_factory=list)
    business_goals: list[str] = field(default_factory=list)
    measurable_success_criteria: list[str] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)
    workflows: list[str] = field(default_factory=list)
    modules: list[str] = field(default_factory=list)
    business_rules: list[str] = field(default_factory=list)
    functional_requirements: list[str] = field(default_factory=list)
    non_functional_requirements: list[str] = field(default_factory=list)
    feasibility_points: dict[str, str] = field(default_factory=dict)
    api_resources: list[str] = field(default_factory=list)
    database_tables: list[str] = field(default_factory=list)
    reports: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)

    # Legacy & helpers for backward compatibility
    actors: list[str] = field(default_factory=list)
    validation_rules: list[str] = field(default_factory=list)
    edge_cases: list[str] = field(default_factory=list)
    request_response_examples: str = ""
    authorization_matrix: str = ""
    traceability_matrix: str = ""

    def to_dict(self) -> dict[str, object]:
        """Serialize domain context."""
        return {
            "project_name": self.project_name,
            "normalized_domain": self.normalized_domain,
            "domain_summary": self.domain_summary,
            "institution_context": self.institution_context,
            "primary_users": list(self.primary_users),
            "secondary_users": list(self.secondary_users),
            "actors_with_responsibilities": dict(self.actors_with_responsibilities),
            "domain_problems": list(self.domain_problems),
            "business_goals": list(self.business_goals),
            "measurable_success_criteria": list(self.measurable_success_criteria),
            "entities": list(self.entities),
            "workflows": list(self.workflows),
            "modules": list(self.modules),
            "business_rules": list(self.business_rules),
            "functional_requirements": list(self.functional_requirements),
            "non_functional_requirements": list(self.non_functional_requirements),
            "feasibility_points": dict(self.feasibility_points),
            "api_resources": list(self.api_resources),
            "database_tables": list(self.database_tables),
            "reports": list(self.reports),
            "risks": list(self.risks),
            "assumptions": list(self.assumptions),
            "constraints": list(self.constraints),
            "out_of_scope": list(self.out_of_scope),
            "actors": list(self.actors),
            "validation_rules": list(self.validation_rules),
            "edge_cases": list(self.edge_cases),
            "request_response_examples": self.request_response_examples,
            "authorization_matrix": self.authorization_matrix,
            "traceability_matrix": self.traceability_matrix,
        }
