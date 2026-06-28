from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_artifact_registry.health import (
    check_research_artifact_registry_health,
)
from stark_terminal_core.research_artifact_registry.interactions import (
    default_research_artifact_forbidden_interaction_registry,
)
from stark_terminal_core.research_artifact_registry.placeholders import (
    default_research_artifact_registry_planning_contract,
)
from stark_terminal_core.research_artifact_registry.readiness import (
    research_artifact_registry_readiness,
)
from stark_terminal_core.research_artifact_registry.safety import (
    unavailable_response_template,
)
from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactLifecycleStatus,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "planning_only": True,
        "unavailable_by_default": True,
        "active_ingestion_enabled": False,
        "persistent_storage_enabled": False,
        "file_uploads_enabled": False,
        "file_downloads_enabled": False,
        "paper_parsing_enabled": False,
        "pdf_parsing_enabled": False,
        "arxiv_ingestion_enabled": False,
        "llm_analysis_enabled": False,
        "strategy_generation_enabled": False,
        "backtesting_enabled": False,
        "recommendations_enabled": False,
        "execution_enabled": False,
        "broker_controls_enabled": False,
        "readiness_to_trade_enabled": False,
        "active_decision_objects_enabled": False,
    }


@router.get("/research-artifact-registry/health")
def research_artifact_registry_health() -> dict[str, Any]:
    status = check_research_artifact_registry_health(get_settings())
    return {
        "service": "stark-terminal-research-artifact-registry",
        **status.model_dump(),
    }


@router.get("/research-artifact-registry/contracts")
def research_artifact_registry_contracts() -> dict[str, Any]:
    settings = get_settings()
    contract = default_research_artifact_registry_planning_contract()
    registry = default_research_artifact_forbidden_interaction_registry()
    return {
        "service": "stark-terminal-research-artifact-registry",
        "schema_version": settings.research_artifact_registry_schema_version,
        "computation_scope": "planning-and-guardrails-only",
        **_safe_flags(),
        "artifact_kinds": [kind.value for kind in contract.artifact_kinds],
        "lifecycle_statuses": [status.value for status in ResearchArtifactLifecycleStatus],
        "forbidden_interactions": [interaction.kind.value for interaction in registry.interactions],
        "next_allowed_phase": contract.next_allowed_phase,
    }


@router.get("/research-artifact-registry/placeholder-artifact")
def research_artifact_registry_placeholder_artifact() -> dict[str, Any]:
    contract = default_research_artifact_registry_planning_contract()
    return {
        "service": "stark-terminal-research-artifact-registry",
        **_safe_flags(),
        "metadata_placeholders": [
            placeholder.model_dump(mode="json") for placeholder in contract.metadata_placeholders
        ],
        "reference_placeholders": [
            placeholder.model_dump(mode="json") for placeholder in contract.reference_placeholders
        ],
        "provenance_placeholders": [
            placeholder.model_dump(mode="json") for placeholder in contract.provenance_placeholders
        ],
        "lifecycle_placeholders": [
            placeholder.model_dump(mode="json") for placeholder in contract.lifecycle_placeholders
        ],
        "no_file_contents": True,
        "no_parsed_paper_text": True,
        "no_strategy_logic": True,
        "no_backtest_metrics": True,
        "no_recommendation_text": True,
    }


@router.get("/research-artifact-registry/readiness-template")
def research_artifact_registry_readiness_template() -> dict[str, Any]:
    readiness = research_artifact_registry_readiness(get_settings())
    return {
        "service": "stark-terminal-research-artifact-registry",
        **_safe_flags(),
        "readiness_report": readiness.model_dump(mode="json"),
        "next_allowed_phase": readiness.next_allowed_phase,
    }


@router.get("/research-artifact-registry/unavailable-template")
def research_artifact_registry_unavailable_template() -> dict[str, Any]:
    response = unavailable_response_template()
    return {
        "service": "stark-terminal-research-artifact-registry",
        **_safe_flags(),
        "unavailable_response": response.model_dump(mode="json"),
    }

