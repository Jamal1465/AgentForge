"""Framework-independent API request and response schemas."""

from __future__ import annotations

from dataclasses import dataclass


class ApiValidationError(ValueError):
    """Raised when an API payload is invalid."""


@dataclass(frozen=True, slots=True)
class CreateProjectRequest:
    """Request body for creating a project workflow."""

    description: str

    @classmethod
    def from_payload(cls, payload: dict[str, object]) -> CreateProjectRequest:
        """Create request schema from untrusted JSON payload."""
        description = payload.get("description")
        if not isinstance(description, str) or not description.strip():
            raise ApiValidationError("description is required and must be a non-empty string.")
        return cls(description=description)


@dataclass(frozen=True, slots=True)
class ApprovalRequest:
    """Request body for approving or rejecting a paused node."""

    workflow_id: str
    node_id: str
    approved: bool

    @classmethod
    def from_payload(cls, payload: dict[str, object]) -> ApprovalRequest:
        """Create approval schema from untrusted JSON payload."""
        workflow_id = payload.get("workflow_id")
        node_id = payload.get("node_id")
        approved = payload.get("approved")
        if not isinstance(workflow_id, str) or not workflow_id.strip():
            raise ApiValidationError("workflow_id is required and must be a non-empty string.")
        if not isinstance(node_id, str) or not node_id.strip():
            raise ApiValidationError("node_id is required and must be a non-empty string.")
        if not isinstance(approved, bool):
            raise ApiValidationError("approved is required and must be a boolean.")
        return cls(workflow_id=workflow_id, node_id=node_id, approved=approved)
