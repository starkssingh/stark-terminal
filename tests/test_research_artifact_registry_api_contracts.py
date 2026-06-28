from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_api.contracts import (
    ResearchArtifactRegistryApiContract,
    default_research_artifact_registry_api_contract,
)


def test_api_contract_defaults_validate() -> None:
    contract = default_research_artifact_registry_api_contract()

    assert contract.service == "stark-terminal-research-artifact-registry-api"
    assert contract.stage == "api_contract_skeleton"
    assert contract.read_only is True
    assert contract.unavailable_by_default is True
    assert contract.active_ingestion_enabled is False
    assert contract.persistent_storage_enabled is False
    assert contract.file_uploads_enabled is False
    assert contract.file_downloads_enabled is False
    assert contract.paper_parsing_enabled is False
    assert contract.strategy_generation_enabled is False
    assert contract.backtesting_enabled is False
    assert contract.recommendations_enabled is False
    assert contract.execution_enabled is False


@pytest.mark.parametrize("field_name", ["contract_id", "service", "stage", "schema_version"])
def test_api_contract_rejects_empty_text(field_name: str) -> None:
    data = {"contract_id": "contract", field_name: " "}
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryApiContract(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "read_only",
        "unavailable_by_default",
    ],
)
def test_api_contract_requires_safe_true_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryApiContract(contract_id="contract", **{field_name: False})


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
def test_api_contract_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryApiContract(contract_id="contract", **{field_name: True})
