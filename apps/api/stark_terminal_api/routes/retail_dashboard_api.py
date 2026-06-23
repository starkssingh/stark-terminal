from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.retail_dashboard_api.contracts import (
    default_retail_dashboard_api_contract_metadata,
)
from stark_terminal_core.retail_dashboard_api.health import check_retail_dashboard_api_health
from stark_terminal_core.retail_dashboard_api.requests import (
    default_retail_dashboard_api_request_placeholder,
)
from stark_terminal_core.retail_dashboard_api.responses import (
    default_retail_dashboard_api_response_placeholder,
)
from stark_terminal_core.retail_dashboard_api.unavailable import (
    default_retail_dashboard_api_unavailable_response,
)

router = APIRouter()


@router.get("/retail-dashboard-api/health")
def retail_dashboard_api_health() -> dict[str, Any]:
    status = check_retail_dashboard_api_health(get_settings())
    return {
        "service": "stark-terminal-retail-dashboard-api",
        **status.model_dump(),
    }


@router.get("/retail-dashboard-api/contracts")
def retail_dashboard_api_contracts() -> dict[str, Any]:
    settings = get_settings()
    metadata = default_retail_dashboard_api_contract_metadata()
    return {
        "service": "stark-terminal-retail-dashboard-api",
        "schema_version": settings.retail_dashboard_api_schema_version,
        "computation_scope": "api-contract-skeleton-only",
        "active_ui_allowed_now": False,
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "broker_controls_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "returns_unavailable_by_default": True,
        "request_kinds": [request_kind.value for request_kind in metadata.request_kinds],
        "unavailable_reasons": [reason.value for reason in metadata.unavailable_reasons],
        "forbidden_outputs": list(metadata.forbidden_outputs),
    }


@router.get("/retail-dashboard-api/unavailable-template")
def retail_dashboard_api_unavailable_template() -> dict[str, Any]:
    unavailable = default_retail_dashboard_api_unavailable_response()
    return {
        "service": "stark-terminal-retail-dashboard-api",
        "api_contract_skeleton_only": True,
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_active_ui": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_broker_controls": True,
        "no_execution": True,
        "no_approval": True,
        "no_override": True,
    }


@router.get("/retail-dashboard-api/response-placeholder")
def retail_dashboard_api_response_placeholder() -> dict[str, Any]:
    request_placeholder = default_retail_dashboard_api_request_placeholder()
    response_placeholder = default_retail_dashboard_api_response_placeholder(
        request_id=request_placeholder.request_id,
    )
    return {
        "service": "stark-terminal-retail-dashboard-api",
        "api_contract_skeleton_only": True,
        "request_placeholder": request_placeholder.model_dump(mode="json"),
        "response_placeholder": response_placeholder.model_dump(mode="json"),
        "data_reference": response_placeholder.data_reference.model_dump(mode="json"),
        "decision_reference": response_placeholder.decision_reference.model_dump(mode="json"),
        "safety_reference": response_placeholder.safety_reference.model_dump(mode="json"),
        "unavailable_response": response_placeholder.unavailable_response.model_dump(mode="json"),
        "no_generated_outputs": True,
        "active_ui_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade_generated": False,
        "broker_control_generated": False,
        "execution_ready": False,
        "approval_granted": False,
        "override_granted": False,
    }
