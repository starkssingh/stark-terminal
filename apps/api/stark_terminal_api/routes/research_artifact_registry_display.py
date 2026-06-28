from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_artifact_registry_display.badges import (
    default_research_artifact_lifecycle_badge_placeholder,
    default_research_artifact_safety_badge_placeholder,
)
from stark_terminal_core.research_artifact_registry_display.cards import (
    default_research_artifact_card_placeholder,
    default_research_artifact_metadata_card_placeholder,
    default_research_artifact_reference_card_placeholder,
)
from stark_terminal_core.research_artifact_registry_display.contracts import (
    default_research_artifact_registry_display_contract,
)
from stark_terminal_core.research_artifact_registry_display.health import (
    research_artifact_registry_display_health,
)
from stark_terminal_core.research_artifact_registry_display.lifecycle import (
    default_research_artifact_lifecycle_display_placeholder,
)
from stark_terminal_core.research_artifact_registry_display.provenance import (
    default_research_artifact_provenance_display_placeholder,
)
from stark_terminal_core.research_artifact_registry_display.references import (
    default_research_artifact_display_reference_placeholder,
    default_research_artifact_source_display_placeholder,
)
from stark_terminal_core.research_artifact_registry_display.safety import (
    research_artifact_registry_display_forbidden_actions,
)
from stark_terminal_core.research_artifact_registry_display.unavailable import (
    unavailable_display_response_template,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "display_contract_skeleton_only": True,
        "read_only": True,
        "unavailable_by_default": True,
        "active_ui_enabled": False,
        "frontend_components_enabled": False,
        "desktop_components_enabled": False,
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


@router.get("/research-artifact-registry-display/health")
def research_artifact_registry_display_health_endpoint() -> dict[str, Any]:
    status = research_artifact_registry_display_health(get_settings())
    return status.model_dump()


@router.get("/research-artifact-registry-display/contracts")
def research_artifact_registry_display_contracts() -> dict[str, Any]:
    contract = default_research_artifact_registry_display_contract()
    forbidden = research_artifact_registry_display_forbidden_actions()
    return {
        "service": "stark-terminal-research-artifact-registry-display",
        "computation_scope": "display-contract-skeleton-only",
        **_safe_flags(),
        "contract": contract.model_dump(mode="json"),
        "forbidden_actions": [action.value for action in forbidden],
    }


@router.get("/research-artifact-registry-display/unavailable-template")
def research_artifact_registry_display_unavailable_template() -> dict[str, Any]:
    response = unavailable_display_response_template()
    return {
        "service": "stark-terminal-research-artifact-registry-display",
        **_safe_flags(),
        "unavailable_response": response.model_dump(mode="json"),
        "no_broker_controls": True,
        "no_readiness_to_trade": True,
        "no_active_decision_objects": True,
    }


@router.get("/research-artifact-registry-display/placeholder-card")
def research_artifact_registry_display_placeholder_card() -> dict[str, Any]:
    return {
        "service": "stark-terminal-research-artifact-registry-display",
        **_safe_flags(),
        "card_placeholders": {
            "artifact_card": default_research_artifact_card_placeholder().model_dump(mode="json"),
            "metadata_card": default_research_artifact_metadata_card_placeholder().model_dump(mode="json"),
            "reference_card": default_research_artifact_reference_card_placeholder().model_dump(mode="json"),
        },
        "badge_placeholders": {
            "lifecycle": default_research_artifact_lifecycle_badge_placeholder().model_dump(mode="json"),
            "safety": default_research_artifact_safety_badge_placeholder().model_dump(mode="json"),
        },
        "no_active_ui": True,
        "no_frontend_components": True,
        "no_desktop_components": True,
        "no_file_preview": True,
        "no_parsed_paper_content": True,
        "no_generated_strategy": True,
        "no_backtest_metrics": True,
        "no_recommendation": True,
        "no_execution_controls": True,
    }


@router.get("/research-artifact-registry-display/placeholder-provenance")
def research_artifact_registry_display_placeholder_provenance() -> dict[str, Any]:
    return {
        "service": "stark-terminal-research-artifact-registry-display",
        **_safe_flags(),
        "provenance_display": default_research_artifact_provenance_display_placeholder().model_dump(mode="json"),
        "display_reference": default_research_artifact_display_reference_placeholder().model_dump(mode="json"),
        "source_display": default_research_artifact_source_display_placeholder().model_dump(mode="json"),
        "no_external_fetch": True,
        "no_local_file_read": True,
        "no_source_trust_claim": True,
        "no_parsed_paper_excerpt": True,
    }


@router.get("/research-artifact-registry-display/placeholder-lifecycle")
def research_artifact_registry_display_placeholder_lifecycle() -> dict[str, Any]:
    return {
        "service": "stark-terminal-research-artifact-registry-display",
        **_safe_flags(),
        "lifecycle_display": default_research_artifact_lifecycle_display_placeholder().model_dump(mode="json"),
        "lifecycle_badge": default_research_artifact_lifecycle_badge_placeholder().model_dump(mode="json"),
        "safety_badge": default_research_artifact_safety_badge_placeholder().model_dump(mode="json"),
        "no_validated_strategy": True,
        "no_approved_strategy": True,
        "no_backtested_strategy": True,
        "no_recommendation": True,
        "no_readiness_to_trade": True,
        "no_execution": True,
    }
