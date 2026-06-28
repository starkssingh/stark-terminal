from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_api.responses import (
    ResearchArtifactLifecycleResponsePlaceholder,
    ResearchArtifactMetadataResponsePlaceholder,
    ResearchArtifactRegistryApiResponsePlaceholder,
    default_research_artifact_registry_api_response_placeholder,
)


def test_api_response_placeholders_validate() -> None:
    response = default_research_artifact_registry_api_response_placeholder()

    assert response.unavailable is True
    assert response.placeholder_only is True
    assert response.persistent_record_created is False
    assert response.parsed_paper_content_present is False
    assert response.generated_strategy_present is False
    assert response.backtest_result_present is False
    assert response.recommendation_present is False
    assert response.decision_object_present is False
    assert response.readiness_to_trade_present is False
    assert response.execution_fields_present is False


@pytest.mark.parametrize(
    "field_name",
    [
        "persistent_record_created",
        "validated_artifact_record",
        "parsed_paper_content_present",
        "generated_strategy_present",
        "backtest_result_present",
        "recommendation_present",
        "decision_object_present",
        "readiness_to_trade_present",
        "execution_fields_present",
    ],
)
def test_api_response_placeholders_reject_generated_outputs(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactMetadataResponsePlaceholder(response_id="response", **{field_name: True})


def test_api_response_placeholders_require_unavailable_and_placeholder_only() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryApiResponsePlaceholder(response_id="response", unavailable=False)
    with pytest.raises(ValidationError):
        ResearchArtifactRegistryApiResponsePlaceholder(response_id="response", placeholder_only=False)


@pytest.mark.parametrize("field_name", ["approved_strategy", "validated_strategy", "execution_ready"])
def test_lifecycle_response_rejects_strategy_and_execution_states(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactLifecycleResponsePlaceholder(response_id="response", **{field_name: True})


def test_api_response_placeholder_models_have_no_active_output_fields() -> None:
    fields = set(ResearchArtifactRegistryApiResponsePlaceholder.model_fields)

    assert "parsed_paper_content" not in fields
    assert "generated_strategy" not in fields
    assert "backtest_result" not in fields
    assert "recommendation" not in fields
    assert "decision_object" not in fields
    assert "readiness_to_trade" not in fields
    assert "execution" not in fields
