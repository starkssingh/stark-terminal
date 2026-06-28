from __future__ import annotations

from pathlib import Path

from stark_terminal_core.research_artifact_registry.interactions import (
    default_research_artifact_forbidden_interaction_registry,
)
from stark_terminal_core.research_artifact_registry.placeholders import (
    default_research_artifact_registry_planning_contract,
)
from stark_terminal_core.research_artifact_registry.readiness import (
    research_artifact_registry_readiness,
)


ROOT = Path(__file__).resolve().parents[1]


def test_planning_contracts_and_placeholders_remain_planning_only() -> None:
    contract = default_research_artifact_registry_planning_contract()

    assert contract.planning_only is True
    assert contract.unavailable_by_default is True
    assert contract.metadata_placeholders
    assert contract.reference_placeholders
    assert contract.provenance_placeholders
    assert contract.lifecycle_placeholders
    assert contract.active_ingestion_enabled is False
    assert contract.persistent_storage_enabled is False
    assert contract.file_uploads_enabled is False
    assert contract.file_downloads_enabled is False
    assert contract.paper_parsing_enabled is False
    assert contract.strategy_generation_enabled is False
    assert contract.backtesting_enabled is False
    assert contract.recommendations_enabled is False
    assert contract.execution_enabled is False


def test_forbidden_interactions_and_readiness_remain_fail_closed() -> None:
    registry = default_research_artifact_forbidden_interaction_registry()
    readiness = research_artifact_registry_readiness()

    forbidden = {interaction.kind.value for interaction in registry.interactions}
    for expected in [
        "ACTIVE_INGESTION",
        "PERSISTENT_STORAGE",
        "FILE_UPLOAD",
        "FILE_DOWNLOAD",
        "PAPER_PARSING",
        "STRATEGY_GENERATION",
        "BACKTESTING",
        "RECOMMENDATION_GENERATION",
        "EXECUTION",
    ]:
        assert expected in forbidden

    assert readiness.registry_planning_ready is True
    assert readiness.active_ingestion_enabled is False
    assert readiness.persistent_storage_enabled is False
    assert readiness.file_uploads_enabled is False
    assert readiness.file_downloads_enabled is False
    assert readiness.paper_parsing_enabled is False
    assert readiness.strategy_generation_enabled is False
    assert readiness.backtesting_enabled is False
    assert readiness.recommendations_enabled is False
    assert readiness.execution_enabled is False


def test_planning_milestone_doc_states_required_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_PLANNING_MILESTONE_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "planning contracts exist",
        "metadata placeholders exist",
        "reference placeholders exist",
        "provenance placeholders exist",
        "lifecycle placeholders exist",
        "forbidden interactions exist",
        "safety/readiness helpers remain fail-closed",
        "no active ingestion/storage",
        "no upload/download",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no execution apis",
    ]:
        assert phrase in text
