from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.decision_human_review.health import check_decision_human_review_health
from stark_terminal_core.decision_human_review.queues import default_decision_review_queue_placeholders
from stark_terminal_core.decision_human_review.roles import default_decision_reviewer_role_placeholders
from stark_terminal_core.decision_human_review.status import default_decision_human_review_status_placeholder
from stark_terminal_core.decision_human_review.tasks import default_decision_review_task_placeholders
from stark_terminal_core.decision_human_review.unavailable import (
    default_decision_human_review_unavailable_response,
)
from stark_terminal_core.decision_human_review.workflow import (
    default_decision_human_review_workflow_contract,
)

router = APIRouter()


@router.get("/decision-human-review/health")
def decision_human_review_health() -> dict[str, Any]:
    status = check_decision_human_review_health(get_settings())
    return {
        "service": "stark-terminal-decision-human-review",
        **status.model_dump(),
    }


@router.get("/decision-human-review/contracts")
def decision_human_review_contracts() -> dict[str, Any]:
    settings = get_settings()
    contract = default_decision_human_review_workflow_contract()
    return {
        "service": "stark-terminal-decision-human-review",
        "schema_version": settings.decision_human_review_schema_version,
        "computation_scope": "workflow-skeleton-only",
        "active_workflow_allowed_now": False,
        "task_assignment_allowed_now": False,
        "reviewer_auth_allowed_now": False,
        "notifications_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "execution_allowed_now": False,
        "task_kinds": [task_kind.value for task_kind in contract.task_kinds],
        "reviewer_roles": [role.value for role in contract.reviewer_roles],
        "queue_kinds": [queue_kind.value for queue_kind in contract.queue_kinds],
        "forbidden_outputs": list(contract.forbidden_outputs),
    }


@router.get("/decision-human-review/unavailable-template")
def decision_human_review_unavailable_template() -> dict[str, Any]:
    unavailable = default_decision_human_review_unavailable_response()
    return {
        "service": "stark-terminal-decision-human-review",
        "workflow_skeleton_only": True,
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_active_workflow": True,
        "no_task_assignment": True,
        "no_reviewer_auth": True,
        "no_notifications": True,
        "no_approval": True,
        "no_override": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_execution": True,
    }


@router.get("/decision-human-review/placeholder-workflow")
def decision_human_review_placeholder_workflow() -> dict[str, Any]:
    workflow_contract = default_decision_human_review_workflow_contract()
    task_placeholders = default_decision_review_task_placeholders()
    role_placeholders = default_decision_reviewer_role_placeholders()
    queue_placeholders = default_decision_review_queue_placeholders()
    status_placeholder = default_decision_human_review_status_placeholder()
    unavailable = default_decision_human_review_unavailable_response()
    return {
        "service": "stark-terminal-decision-human-review",
        "workflow_skeleton_only": True,
        "workflow_contract": workflow_contract.model_dump(mode="json"),
        "task_placeholders": [task.model_dump(mode="json") for task in task_placeholders],
        "role_placeholders": [role.model_dump(mode="json") for role in role_placeholders],
        "queue_placeholders": [queue.model_dump(mode="json") for queue in queue_placeholders],
        "status_placeholder": status_placeholder.model_dump(mode="json"),
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_active_workflow": True,
        "no_generated_outputs": True,
        "workflow_active": False,
        "task_assignment_allowed": False,
        "reviewer_auth_allowed": False,
        "notifications_allowed": False,
        "approval_granted": False,
        "override_granted": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade_generated": False,
        "execution_ready": False,
    }
