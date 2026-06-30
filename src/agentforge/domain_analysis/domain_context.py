"""Domain Context definition for AgentForge."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DomainContext:
    """Stores inferred domain information for generation."""

    project_name: str
    normalized_domain: str
    domain_summary: str
    actors: list[str] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)
    workflows: list[str] = field(default_factory=list)
    modules: list[str] = field(default_factory=list)
    business_rules: list[str] = field(default_factory=list)
    api_resources: list[str] = field(default_factory=list)
    database_tables: list[str] = field(default_factory=list)
    reports: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    
    # Extended fields for functional requirements and matrices
    functional_requirements: list[str] = field(default_factory=list)
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
            "actors": list(self.actors),
            "entities": list(self.entities),
            "workflows": list(self.workflows),
            "modules": list(self.modules),
            "business_rules": list(self.business_rules),
            "api_resources": list(self.api_resources),
            "database_tables": list(self.database_tables),
            "reports": list(self.reports),
            "risks": list(self.risks),
            "assumptions": list(self.assumptions),
            "out_of_scope": list(self.out_of_scope),
            "functional_requirements": list(self.functional_requirements),
            "validation_rules": list(self.validation_rules),
            "edge_cases": list(self.edge_cases),
            "request_response_examples": self.request_response_examples,
            "authorization_matrix": self.authorization_matrix,
            "traceability_matrix": self.traceability_matrix,
        }
