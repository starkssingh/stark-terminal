from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_display.unavailable import (
    ResearchArtifactRegistryDisplayUnavailableResponse,
    unavailable_display_response_template,
)


def test_unavailable_display_response_defaults_to_unavailable() -> None:
    response = unavailable_display_response_template()

    assert response.unavailable is True
    assert response.allowed_stage == "display_contract_skeleton"
    assert response.active_ui_enabled is False
    assert response.frontend_components_enabled is False
    assert response.desktop_components_enabled is False
    assert response.active_ingestion_enabled is False
    assert response.persistent_storage_enabled is False
    assert response.file_uploads_enabled is False
    assert response.file_downloads_enabled is False
    assert response.paper_parsing_enabled is False
    assert response.strategy_generation_enabled is False
    assert response.backtesting_enabled is False
    assert response.recommendations_enabled is False
    assert response.execution_enabled is False


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
def test_unavailable_display_response_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryDisplayUnavailableResponse(reason="Unavailable", **{field_name: True})


def test_unavailable_display_response_requires_reason_and_stage() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryDisplayUnavailableResponse(reason="")
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryDisplayUnavailableResponse(reason="Unavailable", allowed_stage="active_ui")
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryDisplayUnavailableResponse(reason="Unavailable", unavailable=False)
