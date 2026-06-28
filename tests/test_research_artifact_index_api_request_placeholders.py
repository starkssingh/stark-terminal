from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexKeyKind,
    ResearchArtifactIndexKind,
    ResearchArtifactIndexLifecycleStatus,
    ResearchArtifactIndexTagKind,
)
from stark_terminal_core.research_artifact_index_api.requests import (
    ResearchArtifactIndexKeyRequestPlaceholder,
    ResearchArtifactIndexLifecycleRequestPlaceholder,
    ResearchArtifactIndexMetadataRequestPlaceholder,
    ResearchArtifactIndexProvenanceRequestPlaceholder,
    ResearchArtifactIndexReferenceRequestPlaceholder,
    ResearchArtifactIndexTagRequestPlaceholder,
    default_research_artifact_index_key_request_placeholder,
    default_research_artifact_index_lifecycle_request_placeholder,
    default_research_artifact_index_metadata_request_placeholder,
    default_research_artifact_index_provenance_request_placeholder,
    default_research_artifact_index_reference_request_placeholder,
    default_research_artifact_index_tag_request_placeholder,
)


def test_research_artifact_index_api_request_placeholders_validate() -> None:
    placeholders = [
        default_research_artifact_index_metadata_request_placeholder(),
        default_research_artifact_index_key_request_placeholder(),
        default_research_artifact_index_reference_request_placeholder(),
        default_research_artifact_index_tag_request_placeholder(),
        default_research_artifact_index_provenance_request_placeholder(),
        default_research_artifact_index_lifecycle_request_placeholder(),
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
        "indexing_payload_present",
        "search_query_execution_requested",
        "ranking_request_present",
        "retrieval_request_present",
        "embedding_payload_present",
        "vector_store_request_present",
        "strategy_logic_present",
        "backtest_parameters_present",
        "recommendation_fields_present",
        "broker_execution_fields_present",
    ],
)
def test_research_artifact_index_api_request_placeholders_reject_dangerous_content(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexMetadataRequestPlaceholder(request_id="request", **{field_name: True})


def test_research_artifact_index_api_request_placeholders_reject_unknown_values() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexMetadataRequestPlaceholder(
            request_id="request",
            index_kind=ResearchArtifactIndexKind.UNKNOWN,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactIndexKeyRequestPlaceholder(
            request_id="request",
            key_kind=ResearchArtifactIndexKeyKind.UNKNOWN,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactIndexTagRequestPlaceholder(
            request_id="request",
            tag_kind=ResearchArtifactIndexTagKind.UNKNOWN,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactIndexLifecycleRequestPlaceholder(
            request_id="request",
            lifecycle_status=ResearchArtifactIndexLifecycleStatus.UNKNOWN,
        )


def test_research_artifact_index_api_request_models_have_no_payload_fields() -> None:
    fields = set(ResearchArtifactIndexMetadataRequestPlaceholder.model_fields)

    for field in [
        "file_bytes",
        "file_path",
        "upload_payload",
        "fetch_url",
        "paper_text",
        "parsed_content",
        "indexing_payload",
        "search_query",
        "ranking_request",
        "retrieval_request",
        "embedding_payload",
        "vector_store_request",
        "strategy_logic",
        "backtest_parameters",
        "recommendation",
        "execution",
    ]:
        assert field not in fields


@pytest.mark.parametrize(
    "model",
    [
        ResearchArtifactIndexReferenceRequestPlaceholder,
        ResearchArtifactIndexProvenanceRequestPlaceholder,
    ],
)
def test_research_artifact_index_reference_style_request_placeholders_reject_empty_ids(model: type) -> None:
    with pytest.raises(ValidationError):
        model(request_id=" ")
