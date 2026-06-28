from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_artifact_registry_api.contracts import (
    default_research_artifact_registry_api_contract,
)
from stark_terminal_core.research_artifact_registry_api.health import (
    research_artifact_registry_api_health,
)
from stark_terminal_core.research_artifact_registry_api.references import (
    default_research_artifact_api_reference_placeholder,
    default_research_artifact_metadata_reference_placeholder,
    default_research_artifact_provenance_reference_placeholder,
)
from stark_terminal_core.research_artifact_registry_api.requests import (
    default_research_artifact_lifecycle_request_placeholder,
    default_research_artifact_metadata_request_placeholder,
    default_research_artifact_provenance_request_placeholder,
    default_research_artifact_reference_request_placeholder,
)
from stark_terminal_core.research_artifact_registry_api.responses import (
    default_research_artifact_registry_api_response_placeholder,
)
from stark_terminal_core.research_artifact_registry_api.safety import (
    research_artifact_registry_api_forbidden_actions,
)
from stark_terminal_core.research_artifact_registry_api.unavailable import (
    unavailable_response_template,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "api_contract_skeleton_only": True,
        "read_only": True,
        "unavailable_by_default": True,
        "active_ingestion_enabled": False,
        "persistent_storage_enabled": False,
        "file_uploads_enabled": False,
        "file_downloads_enabled": False,
        "paper_parsing_enabled": False,
        "strategy_generation_enabled": False,
        "backtesting_enabled": False,
        "recommendations_enabled": False,
        "execution_enabled": False,
        "broker_controls_enabled": False,
        "readiness_to_trade_enabled": False,
        "active_decision_objects_enabled": False,
    }


@router.get("/research-artifact-registry-api/health")
def research_artifact_registry_api_health_endpoint() -> dict[str, Any]:
    status = research_artifact_registry_api_health(get_settings())
    return status.model_dump()


@router.get("/research-artifact-registry-api/contracts")
def research_artifact_registry_api_contracts() -> dict[str, Any]:
    contract = default_research_artifact_registry_api_contract()
    forbidden = research_artifact_registry_api_forbidden_actions()
    return {
        "service": "stark-terminal-research-artifact-registry-api",
        "computation_scope": "api-contract-skeleton-only",
        **_safe_flags(),
        "contract": contract.model_dump(mode="json"),
        "forbidden_actions": [action.value for action in forbidden],
    }


@router.get("/research-artifact-registry-api/unavailable-template")
def research_artifact_registry_api_unavailable_template() -> dict[str, Any]:
    response = unavailable_response_template()
    return {
        "service": "stark-terminal-research-artifact-registry-api",
        **_safe_flags(),
        "unavailable_response": response.model_dump(mode="json"),
        "no_broker_controls": True,
        "no_readiness_to_trade": True,
        "no_active_decision_objects": True,
    }


@router.get("/research-artifact-registry-api/response-placeholder")
def research_artifact_registry_api_response_placeholder() -> dict[str, Any]:
    response = default_research_artifact_registry_api_response_placeholder()
    return {
        "service": "stark-terminal-research-artifact-registry-api",
        **_safe_flags(),
        "request_placeholders": {
            "metadata": default_research_artifact_metadata_request_placeholder().model_dump(mode="json"),
            "reference": default_research_artifact_reference_request_placeholder().model_dump(mode="json"),
            "provenance": default_research_artifact_provenance_request_placeholder().model_dump(mode="json"),
            "lifecycle": default_research_artifact_lifecycle_request_placeholder().model_dump(mode="json"),
        },
        "response_placeholder": response.model_dump(mode="json"),
        "no_parsed_paper_content": True,
        "no_generated_strategy": True,
        "no_backtest_result": True,
        "no_recommendation": True,
        "no_decision_object": True,
        "no_execution_fields": True,
    }


@router.get("/research-artifact-registry-api/reference-placeholder")
def research_artifact_registry_api_reference_placeholder() -> dict[str, Any]:
    return {
        "service": "stark-terminal-research-artifact-registry-api",
        **_safe_flags(),
        "api_reference": default_research_artifact_api_reference_placeholder().model_dump(mode="json"),
        "metadata_reference": default_research_artifact_metadata_reference_placeholder().model_dump(mode="json"),
        "provenance_reference": default_research_artifact_provenance_reference_placeholder().model_dump(mode="json"),
        "no_external_fetch": True,
        "no_local_file_read": True,
        "no_source_trust_claim": True,
    }
