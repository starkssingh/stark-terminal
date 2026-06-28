from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_display.contracts import (
    ResearchArtifactRegistryDisplayContract,
    default_research_artifact_registry_display_contract,
)


def test_display_contract_defaults_are_safe() -> None:
    contract = default_research_artifact_registry_display_contract()

    assert contract.service == "stark-terminal-research-artifact-registry-display"
    assert contract.stage == "display_contract_skeleton"
    assert contract.read_only is True
    assert contract.unavailable_by_default is True
    assert contract.active_ui_enabled is False
    assert contract.frontend_components_enabled is False
    assert contract.desktop_components_enabled is False
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
        "active_ui_enabled",
        "frontend_components_enabled",
        "desktop_components_enabled",
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
def test_display_contract_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryDisplayContract(contract_id="display-contract", **{field_name: True})


def test_display_contract_enforces_read_only_and_unavailable() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryDisplayContract(contract_id="display-contract", read_only=False)
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryDisplayContract(contract_id="display-contract", unavailable_by_default=False)
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryDisplayContract(contract_id="display-contract", stage="active_ui")
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryDisplayContract(contract_id="")
