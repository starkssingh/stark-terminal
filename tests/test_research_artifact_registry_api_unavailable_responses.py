from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_api.unavailable import (
    ResearchArtifactRegistryApiUnavailableResponse,
    unavailable_response_template,
)


def test_api_unavailable_response_template_is_fail_closed() -> None:
    response = unavailable_response_template()

    assert response.unavailable is True
    assert response.allowed_stage == "api_contract_skeleton"
    assert response.active_ingestion_enabled is False
    assert response.persistent_storage_enabled is False
    assert response.file_uploads_enabled is False
    assert response.file_downloads_enabled is False
    assert response.paper_parsing_enabled is False
    assert response.strategy_generation_enabled is False
    assert response.backtesting_enabled is False
    assert response.recommendations_enabled is False
    assert response.execution_enabled is False


def test_api_unavailable_response_requires_reason_and_stage() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryApiUnavailableResponse(reason=" ")
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryApiUnavailableResponse(reason="blocked", allowed_stage="active")


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
def test_api_unavailable_response_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryApiUnavailableResponse(reason="blocked", **{field_name: True})


def test_api_unavailable_response_must_remain_unavailable() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryApiUnavailableResponse(reason="blocked", unavailable=False)
