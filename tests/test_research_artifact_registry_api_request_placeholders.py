from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactKind,
    ResearchArtifactLifecycleStatus,
)
from stark_terminal_core.research_artifact_registry_api.requests import (
    ResearchArtifactLifecycleRequestPlaceholder,
    ResearchArtifactMetadataRequestPlaceholder,
    ResearchArtifactProvenanceRequestPlaceholder,
    ResearchArtifactReferenceRequestPlaceholder,
    default_research_artifact_lifecycle_request_placeholder,
    default_research_artifact_metadata_request_placeholder,
    default_research_artifact_provenance_request_placeholder,
    default_research_artifact_reference_request_placeholder,
)


def test_api_request_placeholders_validate() -> None:
    placeholders = [
        default_research_artifact_metadata_request_placeholder(),
        default_research_artifact_reference_request_placeholder(),
        default_research_artifact_provenance_request_placeholder(),
        default_research_artifact_lifecycle_request_placeholder(),
    ]

    assert all(placeholder.api_contract_skeleton_only for placeholder in placeholders)
    assert all(not placeholder.executable_request for placeholder in placeholders)


@pytest.mark.parametrize(
    "field_name",
    [
        "executable_request",
        "file_bytes_present",
        "file_path_read_requested",
        "upload_payload_present",
        "fetch_url_present",
        "paper_text_present",
        "parsed_content_present",
        "strategy_logic_present",
        "backtest_parameters_present",
        "recommendation_fields_present",
        "broker_execution_fields_present",
    ],
)
def test_api_request_placeholders_reject_dangerous_content(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactMetadataRequestPlaceholder(request_id="request", **{field_name: True})


def test_api_request_placeholders_reject_unknown_kind_and_status() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactMetadataRequestPlaceholder(
            request_id="request",
            artifact_kind=ResearchArtifactKind.UNKNOWN,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactLifecycleRequestPlaceholder(
            request_id="request",
            lifecycle_status=ResearchArtifactLifecycleStatus.UNKNOWN,
        )


def test_api_request_placeholder_models_have_no_payload_fields() -> None:
    fields = set(ResearchArtifactMetadataRequestPlaceholder.model_fields)

    assert "file_bytes" not in fields
    assert "file_path" not in fields
    assert "upload_payload" not in fields
    assert "fetch_url" not in fields
    assert "paper_text" not in fields
    assert "parsed_content" not in fields
    assert "strategy_logic" not in fields
    assert "backtest_parameters" not in fields
    assert "recommendation" not in fields
    assert "execution" not in fields


@pytest.mark.parametrize(
    "model",
    [
        ResearchArtifactReferenceRequestPlaceholder,
        ResearchArtifactProvenanceRequestPlaceholder,
    ],
)
def test_reference_style_request_placeholders_reject_empty_ids(model: type) -> None:
    with pytest.raises(ValidationError):
        model(request_id=" ")
