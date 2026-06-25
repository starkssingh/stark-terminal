from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.retail_trader_experience_api.contracts import (
    default_retail_trader_experience_api_contract_metadata,
)
from stark_terminal_core.retail_trader_experience_api.health import (
    check_retail_trader_experience_api_health,
)
from stark_terminal_core.retail_trader_experience_api.requests import (
    default_retail_trader_experience_api_request_placeholder,
)
from stark_terminal_core.retail_trader_experience_api.responses import (
    default_retail_trader_experience_api_response_placeholder,
)
from stark_terminal_core.retail_trader_experience_api.unavailable import (
    default_retail_trader_experience_api_unavailable_response,
)

router = APIRouter()


@router.get("/retail-trader-experience-api/health")
def retail_trader_experience_api_health() -> dict[str, Any]:
    status = check_retail_trader_experience_api_health(get_settings())
    return {
        "service": "stark-terminal-retail-trader-experience-api",
        **status.model_dump(),
    }


@router.get("/retail-trader-experience-api/contracts")
def retail_trader_experience_api_contracts() -> dict[str, Any]:
    settings = get_settings()
    metadata = default_retail_trader_experience_api_contract_metadata()
    return {
        "service": "stark-terminal-retail-trader-experience-api",
        "schema_version": settings.retail_trader_experience_api_schema_version,
        "computation_scope": "api-contract-skeleton-only",
        "active_ui_allowed_now": False,
        "frontend_components_allowed_now": False,
        "desktop_components_allowed_now": False,
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "broker_controls_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "suitability_profiling_allowed_now": False,
        "returns_unavailable_by_default": True,
        "request_kinds": [request_kind.value for request_kind in metadata.request_kinds],
        "unavailable_reasons": [reason.value for reason in metadata.unavailable_reasons],
        "forbidden_outputs": list(metadata.forbidden_outputs),
    }


@router.get("/retail-trader-experience-api/unavailable-template")
def retail_trader_experience_api_unavailable_template() -> dict[str, Any]:
    unavailable = default_retail_trader_experience_api_unavailable_response()
    return {
        "service": "stark-terminal-retail-trader-experience-api",
        "api_contract_skeleton_only": True,
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_active_ui": True,
        "no_frontend_components": True,
        "no_desktop_components": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_broker_controls": True,
        "no_suitability_profiling": True,
        "no_execution": True,
        "no_approval": True,
        "no_override": True,
    }


@router.get("/retail-trader-experience-api/response-placeholder")
def retail_trader_experience_api_response_placeholder() -> dict[str, Any]:
    request_placeholder = default_retail_trader_experience_api_request_placeholder()
    response_placeholder = default_retail_trader_experience_api_response_placeholder(
        request_id=request_placeholder.request_id,
    )
    return {
        "service": "stark-terminal-retail-trader-experience-api",
        "api_contract_skeleton_only": True,
        "request_placeholder": request_placeholder.model_dump(mode="json"),
        "response_placeholder": response_placeholder.model_dump(mode="json"),
        "persona_reference": response_placeholder.persona_reference.model_dump(mode="json"),
        "journey_reference": response_placeholder.journey_reference.model_dump(mode="json"),
        "dashboard_reference": response_placeholder.dashboard_reference.model_dump(mode="json"),
        "decision_reference": response_placeholder.decision_reference.model_dump(mode="json"),
        "safety_reference": response_placeholder.safety_reference.model_dump(mode="json"),
        "unavailable_response": response_placeholder.unavailable_response.model_dump(mode="json"),
        "no_generated_outputs": True,
        "no_suitability_profiling": True,
        "active_ui_generated": False,
        "frontend_component_generated": False,
        "desktop_component_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade_generated": False,
        "broker_control_generated": False,
        "suitability_profile_generated": False,
        "execution_ready": False,
        "approval_granted": False,
        "override_granted": False,
    }
