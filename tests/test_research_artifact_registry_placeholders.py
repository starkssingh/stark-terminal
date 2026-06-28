from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.placeholders import (
    ResearchArtifactRegistryPlanningContract,
    default_research_artifact_registry_planning_contract,
)
from stark_terminal_core.research_artifact_registry.types import ResearchArtifactKind


def test_default_planning_contract_is_placeholder_only() -> None:
    contract = default_research_artifact_registry_planning_contract()

    assert contract.planning_only is True
    assert contract.unavailable_by_default is True
    assert contract.next_allowed_phase == "api_contract_skeleton"
    assert ResearchArtifactKind.BACKTEST_REFERENCE_PLACEHOLDER in contract.artifact_kinds
    assert ResearchArtifactKind.STRATEGY_REFERENCE_PLACEHOLDER in contract.artifact_kinds
    assert contract.active_ingestion_enabled is False
    assert contract.persistent_storage_enabled is False
    assert contract.file_uploads_enabled is False
    assert contract.file_downloads_enabled is False
    assert contract.paper_parsing_enabled is False
    assert contract.strategy_generation_enabled is False
    assert contract.backtesting_enabled is False
    assert contract.recommendations_enabled is False
    assert contract.execution_enabled is False


@pytest.mark.parametrize(
    "field_name",
    [
        "planning_only",
        "unavailable_by_default",
    ],
)
def test_planning_contract_enforces_required_true_flags(field_name: str) -> None:
    contract = default_research_artifact_registry_planning_contract()
    data = contract.model_dump()
    data[field_name] = False

    with pytest.raises(ValidationError):
        ResearchArtifactRegistryPlanningContract(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ingestion_enabled",
        "persistent_storage_enabled",
        "file_uploads_enabled",
        "file_downloads_enabled",
        "paper_parsing_enabled",
        "strategy_generation_enabled",
        "backtesting_enabled",
        "recommendations_enabled",
        "execution_enabled",
    ],
)
def test_planning_contract_rejects_dangerous_enabled_flags(field_name: str) -> None:
    contract = default_research_artifact_registry_planning_contract()
    data = contract.model_dump()
    data[field_name] = True

    with pytest.raises(ValidationError):
        ResearchArtifactRegistryPlanningContract(**data)

