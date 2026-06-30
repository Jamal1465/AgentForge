"""Domain Consistency Evaluator for AgentForge.

Checks that generated artifacts adhere to the target domain, contain expected
domain keywords, actors, and entities, and exclude wrong-domain or banned terms.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from agentforge.domain.value_objects import RiskLevel

if TYPE_CHECKING:
    from agentforge.domain.entities import Artifact
    from agentforge.domain.evaluation import EvaluationFinding
    from agentforge.domain_analysis.domain_context import DomainContext


BANNED_TERMS_BY_DOMAIN: dict[str, list[str]] = {
    "library-management": [
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
    ],
    "ecommerce": [
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
        "librarian",
        "book copy",
        "loan",
        "overdue fine",
    ],
    "hospital-management": [
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
        "librarian",
        "book copy",
        "loan",
        "overdue fine",
        "shopping cart",
        "checkout process",
    ],
    "learning-management-system": [
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
        "librarian",
        "book copy",
        "loan",
        "overdue fine",
    ],
    "inventory-management": [
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
        "librarian",
        "book copy",
        "loan",
        "overdue fine",
    ],
    "task-management": [
        "librarian",
        "book copy",
        "loan",
        "overdue fine",
        "interacts with the system in a designated role",
        "reference implementation",
        "tight coupling",
        "lack of unit test coverage",
        "incomplete deployment configurations",
    ],
    "generic-business-app": [
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
    ],
}


class DomainConsistencyEvaluator:
    """Evaluates artifacts against the target domain context."""

    def evaluate(
        self,
        artifact: Artifact,
        ctx: DomainContext,
    ) -> tuple[float, str, list[EvaluationFinding]]:
        """Score the artifact content based on domain consistency and check for issues."""
        from agentforge.domain.evaluation import EvaluationFinding

        content_lower = artifact.content.lower()
        findings: list[EvaluationFinding] = []
        score = 1.0
        reasons: list[str] = []

        # 1. Check for banned wrong-domain keywords
        domain_key = ctx.normalized_domain
        banned_terms = BANNED_TERMS_BY_DOMAIN.get(domain_key, BANNED_TERMS_BY_DOMAIN["generic-business-app"])

        for term in banned_terms:
            if term in content_lower:
                score = 0.0
                reasons.append(f"Contains wrong-domain/banned term: '{term}'")
                findings.append(
                    EvaluationFinding(
                        message=f"Banned term found: '{term}'",
                        severity=RiskLevel.HIGH,
                        criterion_id="agent-result-domain-consistency",
                        evidence=f"artifact={artifact.name}, term={term}",
                    )
                )

        # 2. Check for required domain actors (specifically for brief/requirements)
        if "brief" in artifact.name or "requirements" in artifact.name:
            missing_actors = []
            for actor in ctx.actors:
                if actor.lower() not in content_lower:
                    missing_actors.append(actor)
            
            if missing_actors:
                score = max(0.0, score - 0.1 * len(missing_actors))
                reasons.append(f"Missing domain actors: {', '.join(missing_actors)}")
                findings.append(
                    EvaluationFinding(
                        message=f"Missing expected actors: {', '.join(missing_actors)}",
                        severity=RiskLevel.MEDIUM,
                        criterion_id="agent-result-domain-consistency",
                        evidence=f"artifact={artifact.name}, missing={missing_actors}",
                    )
                )

        # 3. Check for required domain entities (specifically for requirements/architecture)
        if "requirements" in artifact.name or "architecture" in artifact.name:
            missing_entities = []
            for entity in ctx.entities:
                parts = re.split(r'\s*/\s*|\s+', entity.lower())
                found = any(part in content_lower for part in parts if len(part) > 2)
                if not found:
                    missing_entities.append(entity)

            if missing_entities:
                score = max(0.0, score - 0.05 * len(missing_entities))
                reasons.append(f"Missing domain entities: {', '.join(missing_entities)}")
                findings.append(
                    EvaluationFinding(
                        message=f"Missing expected entities: {', '.join(missing_entities)}",
                        severity=RiskLevel.MEDIUM,
                        criterion_id="agent-result-domain-consistency",
                        evidence=f"artifact={artifact.name}, missing={missing_entities}",
                    )
                )

        if score == 1.0:
            reasons.append("Perfect domain consistency maintained.")

        return score, "; ".join(reasons), findings
