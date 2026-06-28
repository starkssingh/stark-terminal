from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.research_artifact_index.health import (
    check_research_artifact_index_health,
)
from stark_terminal_core.research_artifact_index.interactions import (
    default_research_artifact_index_forbidden_interactions,
)
from stark_terminal_core.research_artifact_index.keys import (
    default_research_artifact_index_key_placeholders,
)
from stark_terminal_core.research_artifact_index.lifecycle import (
    default_research_artifact_index_lifecycle_placeholders,
)
from stark_terminal_core.research_artifact_index.metadata import (
    default_research_artifact_index_metadata_placeholders,
)
from stark_terminal_core.research_artifact_index.provenance import (
    default_research_artifact_index_provenance_placeholders,
)
from stark_terminal_core.research_artifact_index.readiness import (
    research_artifact_index_readiness,
)
from stark_terminal_core.research_artifact_index.references import (
    default_research_artifact_index_reference_placeholders,
)
from stark_terminal_core.research_artifact_index.safety import (
    unavailable_response_template,
)
from stark_terminal_core.research_artifact_index.tags import (
    default_research_artifact_index_tag_placeholders,
)
from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexKeyKind,
    ResearchArtifactIndexKind,
    ResearchArtifactIndexLifecycleStatus,
    ResearchArtifactIndexTagKind,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "planning_only": True,
        "unavailable_by_default": True,
        "indexing_engine_enabled": False,
        "search_engine_enabled": False,
        "ranking_engine_enabled": False,
        "retrieval_engine_enabled": False,
        "embeddings_enabled": False,
        "vector_store_enabled": False,
        "active_ingestion_enabled": False,
        "persistent_storage_enabled": False,
        "file_uploads_enabled": False,
        "file_downloads_enabled": False,
        "file_previews_enabled": False,
        "paper_parsing_enabled": False,
        "strategy_generation_enabled": False,
        "backtesting_enabled": False,
        "recommendations_enabled": False,
        "execution_enabled": False,
        "broker_controls_enabled": False,
        "readiness_to_trade_enabled": False,
        "active_decision_objects_enabled": False,
    }


@router.get("/research-artifact-index/health")
def research_artifact_index_health() -> dict[str, Any]:
    status = check_research_artifact_index_health(get_settings())
    return {
        "service": "stark-terminal-research-artifact-index",
        **status.model_dump(),
    }


@router.get("/research-artifact-index/contracts")
def research_artifact_index_contracts() -> dict[str, Any]:
    settings = get_settings()
    forbidden = default_research_artifact_index_forbidden_interactions()
    return {
        "service": "stark-terminal-research-artifact-index",
        "schema_version": settings.research_artifact_index_schema_version,
        "computation_scope": "planning-and-guardrails-only",
        **_safe_flags(),
        "index_kinds": [
            kind.value for kind in ResearchArtifactIndexKind if kind != ResearchArtifactIndexKind.UNKNOWN
        ],
        "key_kinds": [
            kind.value for kind in ResearchArtifactIndexKeyKind if kind != ResearchArtifactIndexKeyKind.UNKNOWN
        ],
        "tag_kinds": [
            kind.value for kind in ResearchArtifactIndexTagKind if kind != ResearchArtifactIndexTagKind.UNKNOWN
        ],
        "lifecycle_statuses": [status.value for status in ResearchArtifactIndexLifecycleStatus],
        "forbidden_interactions": [interaction.kind.value for interaction in forbidden],
        "next_allowed_phase": "api_contract_skeleton",
    }


@router.get("/research-artifact-index/placeholder-index")
def research_artifact_index_placeholder_index() -> dict[str, Any]:
    return {
        "service": "stark-terminal-research-artifact-index",
        **_safe_flags(),
        "metadata_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_artifact_index_metadata_placeholders()
        ],
        "key_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_artifact_index_key_placeholders()
        ],
        "reference_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_artifact_index_reference_placeholders()
        ],
        "tag_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_artifact_index_tag_placeholders()
        ],
        "provenance_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_artifact_index_provenance_placeholders()
        ],
        "lifecycle_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_research_artifact_index_lifecycle_placeholders()
        ],
        "no_indexing_engine": True,
        "no_search_engine": True,
        "no_ranking_engine": True,
        "no_embeddings": True,
        "no_vector_store": True,
        "no_file_contents": True,
        "no_parsed_paper_text": True,
        "no_strategy_logic": True,
        "no_backtest_metrics": True,
        "no_recommendation_text": True,
    }


@router.get("/research-artifact-index/readiness-template")
def research_artifact_index_readiness_template() -> dict[str, Any]:
    readiness = research_artifact_index_readiness(get_settings())
    return {
        "service": "stark-terminal-research-artifact-index",
        **_safe_flags(),
        "readiness_report": readiness.model_dump(mode="json"),
        "next_allowed_phase": readiness.next_allowed_phase,
    }


@router.get("/research-artifact-index/unavailable-template")
def research_artifact_index_unavailable_template() -> dict[str, Any]:
    response = unavailable_response_template()
    return {
        "service": "stark-terminal-research-artifact-index",
        **_safe_flags(),
        "unavailable_response": response.model_dump(mode="json"),
    }
