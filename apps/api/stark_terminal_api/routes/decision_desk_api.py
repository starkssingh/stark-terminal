from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.decision_api.contracts import default_decision_desk_api_contract_metadata
from stark_terminal_core.decision_api.health import check_decision_api_health
from stark_terminal_core.decision_api.requests import default_decision_desk_request_placeholder
from stark_terminal_core.decision_api.responses import default_decision_desk_response_placeholder
from stark_terminal_core.decision_api.unavailable import default_decision_desk_unavailable_response

router = APIRouter()


@router.get("/decision-desk-api/health")
def decision_desk_api_health() -> dict[str, Any]:
    status = check_decision_api_health(get_settings())
    return {
        "service": "stark-terminal-decision-desk-api",
        **status.model_dump(),
    }


@router.get("/decision-desk-api/contracts")
def decision_desk_api_contracts() -> dict[str, Any]:
    settings = get_settings()
    metadata = default_decision_desk_api_contract_metadata()
    return {
        "service": "stark-terminal-decision-desk-api",
        "schema_version": settings.decision_api_schema_version,
        "computation_scope": "contract-skeleton-only",
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "returns_unavailable_by_default": True,
        "request_kinds": [request_kind.value for request_kind in metadata.request_kinds],
        "unavailable_reasons": [reason.value for reason in metadata.unavailable_reasons],
        "forbidden_outputs": list(metadata.forbidden_outputs),
    }


@router.get("/decision-desk-api/unavailable-template")
def decision_desk_api_unavailable_template() -> dict[str, Any]:
    unavailable = default_decision_desk_unavailable_response()
    return {
        "service": "stark-terminal-decision-desk-api",
        "contract_skeleton_only": True,
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_approval": True,
        "no_override": True,
        "no_execution": True,
    }


@router.get("/decision-desk-api/response-placeholder")
def decision_desk_api_response_placeholder() -> dict[str, Any]:
    request_placeholder = default_decision_desk_request_placeholder()
    response_placeholder = default_decision_desk_response_placeholder()
    return {
        "service": "stark-terminal-decision-desk-api",
        "request_placeholder": request_placeholder.model_dump(mode="json"),
        "response_placeholder": response_placeholder.model_dump(mode="json"),
        "evidence_reference_placeholder": response_placeholder.evidence_reference.model_dump(mode="json"),
        "safety_reference_placeholder": response_placeholder.safety_reference.model_dump(mode="json"),
        "unavailable_response": response_placeholder.unavailable_response.model_dump(mode="json"),
        "no_generated_outputs": True,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "execution_ready": False,
        "approval_granted": False,
        "override_granted": False,
    }
