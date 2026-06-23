from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.decision_readiness_api.contracts import (
    default_decision_readiness_api_contract_metadata,
)
from stark_terminal_core.decision_readiness_api.health import check_decision_readiness_api_health
from stark_terminal_core.decision_readiness_api.requests import (
    default_decision_readiness_request_placeholder,
)
from stark_terminal_core.decision_readiness_api.responses import (
    default_decision_readiness_response_placeholder,
)
from stark_terminal_core.decision_readiness_api.unavailable import (
    default_decision_readiness_unavailable_response,
)

router = APIRouter()


@router.get("/decision-readiness-api/health")
def decision_readiness_api_health() -> dict[str, Any]:
    status = check_decision_readiness_api_health(get_settings())
    return {
        "service": "stark-terminal-decision-readiness-api",
        **status.model_dump(),
    }


@router.get("/decision-readiness-api/contracts")
def decision_readiness_api_contracts() -> dict[str, Any]:
    settings = get_settings()
    metadata = default_decision_readiness_api_contract_metadata()
    return {
        "service": "stark-terminal-decision-readiness-api",
        "schema_version": settings.decision_readiness_api_schema_version,
        "computation_scope": "readiness-contract-skeleton-only",
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "readiness_status_generation_allowed_now": False,
        "returns_unavailable_by_default": True,
        "request_kinds": [request_kind.value for request_kind in metadata.request_kinds],
        "unavailable_reasons": [reason.value for reason in metadata.unavailable_reasons],
        "forbidden_outputs": list(metadata.forbidden_outputs),
    }


@router.get("/decision-readiness-api/unavailable-template")
def decision_readiness_api_unavailable_template() -> dict[str, Any]:
    unavailable = default_decision_readiness_unavailable_response()
    return {
        "service": "stark-terminal-decision-readiness-api",
        "readiness_contract_skeleton_only": True,
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_readiness_status_generation": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_approval": True,
        "no_override": True,
        "no_execution": True,
    }


@router.get("/decision-readiness-api/response-placeholder")
def decision_readiness_api_response_placeholder() -> dict[str, Any]:
    request_placeholder = default_decision_readiness_request_placeholder()
    response_placeholder = default_decision_readiness_response_placeholder()
    return {
        "service": "stark-terminal-decision-readiness-api",
        "request_placeholder": request_placeholder.model_dump(mode="json"),
        "response_placeholder": response_placeholder.model_dump(mode="json"),
        "evidence_reference_placeholder": response_placeholder.evidence_reference.model_dump(mode="json"),
        "safety_reference_placeholder": response_placeholder.safety_reference.model_dump(mode="json"),
        "human_review_reference_placeholder": response_placeholder.human_review_reference.model_dump(mode="json"),
        "blocked_output_reference_placeholder": response_placeholder.blocked_output_reference.model_dump(
            mode="json"
        ),
        "unavailable_response": response_placeholder.unavailable_response.model_dump(mode="json"),
        "no_generated_outputs": True,
        "readiness_status_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "execution_ready": False,
        "approval_granted": False,
        "override_granted": False,
    }
