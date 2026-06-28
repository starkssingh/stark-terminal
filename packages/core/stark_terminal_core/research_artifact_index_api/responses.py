from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)
from stark_terminal_core.research_artifact_index_api.references import (
    ResearchArtifactIndexApiReferencePlaceholder,
    ResearchArtifactIndexKeyReferencePlaceholder,
    ResearchArtifactIndexMetadataReferencePlaceholder,
    ResearchArtifactIndexProvenanceReferencePlaceholder,
    ResearchArtifactIndexRegistryReferencePlaceholder,
    default_research_artifact_index_api_reference_placeholder,
    default_research_artifact_index_key_reference_placeholder,
    default_research_artifact_index_metadata_reference_placeholder,
    default_research_artifact_index_provenance_reference_placeholder,
    default_research_artifact_index_registry_reference_placeholder,
)
from stark_terminal_core.research_artifact_index_api.unavailable import (
    ResearchArtifactIndexApiUnavailableResponse,
    unavailable_response_template,
)


class _IndexApiResponsePlaceholderBase(BaseModel):
    response_id: str
    unavailable: bool = True
    placeholder_only: bool = True
    indexed_artifact_records_present: bool = False
    search_results_present: bool = False
    ranking_results_present: bool = False
    retrieval_results_present: bool = False
    embeddings_present: bool = False
    vector_ids_present: bool = False
    parsed_paper_content_present: bool = False
    generated_strategy_present: bool = False
    backtest_result_present: bool = False
    recommendation_present: bool = False
    decision_object_present: bool = False
    readiness_to_trade_present: bool = False
    execution_fields_present: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API response placeholder text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def response_must_fail_closed(self) -> _IndexApiResponsePlaceholderBase:
        if not self.unavailable:
            raise ValueError("Research Artifact Index API response placeholder must remain unavailable")
        if not self.placeholder_only:
            raise ValueError("Research Artifact Index API response placeholder must remain placeholder-only")
        dangerous_flags = {
            "indexed artifact records": self.indexed_artifact_records_present,
            "search results": self.search_results_present,
            "ranking results": self.ranking_results_present,
            "retrieval results": self.retrieval_results_present,
            "embeddings": self.embeddings_present,
            "vector IDs": self.vector_ids_present,
            "parsed paper content": self.parsed_paper_content_present,
            "generated strategy": self.generated_strategy_present,
            "backtest result": self.backtest_result_present,
            "recommendation": self.recommendation_present,
            "DecisionObject": self.decision_object_present,
            "readiness-to-trade": self.readiness_to_trade_present,
            "execution fields": self.execution_fields_present,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"Research Artifact Index API response placeholder cannot include: {', '.join(enabled)}")
        return self


class ResearchArtifactIndexMetadataResponsePlaceholder(_IndexApiResponsePlaceholderBase):
    metadata_reference: ResearchArtifactIndexMetadataReferencePlaceholder = Field(
        default_factory=default_research_artifact_index_metadata_reference_placeholder
    )


class ResearchArtifactIndexKeyResponsePlaceholder(_IndexApiResponsePlaceholderBase):
    key_reference: ResearchArtifactIndexKeyReferencePlaceholder = Field(
        default_factory=default_research_artifact_index_key_reference_placeholder
    )


class ResearchArtifactIndexReferenceResponsePlaceholder(_IndexApiResponsePlaceholderBase):
    api_reference: ResearchArtifactIndexApiReferencePlaceholder = Field(
        default_factory=default_research_artifact_index_api_reference_placeholder
    )
    registry_reference: ResearchArtifactIndexRegistryReferencePlaceholder = Field(
        default_factory=default_research_artifact_index_registry_reference_placeholder
    )


class ResearchArtifactIndexTagResponsePlaceholder(_IndexApiResponsePlaceholderBase):
    tag_reference_id: str = "research-artifact-index-api-tag-reference-placeholder-v1"
    search_enabled: bool = False
    ranking_enabled: bool = False

    @field_validator("tag_reference_id")
    @classmethod
    def tag_reference_id_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index tag response placeholder text fields")

    @model_validator(mode="after")
    def tag_response_must_fail_closed(self) -> ResearchArtifactIndexTagResponsePlaceholder:
        if self.search_enabled:
            raise ValueError("tag response cannot enable search")
        if self.ranking_enabled:
            raise ValueError("tag response cannot enable ranking")
        return self


class ResearchArtifactIndexProvenanceResponsePlaceholder(_IndexApiResponsePlaceholderBase):
    provenance_reference: ResearchArtifactIndexProvenanceReferencePlaceholder = Field(
        default_factory=default_research_artifact_index_provenance_reference_placeholder
    )


class ResearchArtifactIndexLifecycleResponsePlaceholder(_IndexApiResponsePlaceholderBase):
    lifecycle_reference_id: str = "research-artifact-index-api-lifecycle-reference-placeholder-v1"
    indexed_status: bool = False
    searchable_status: bool = False
    retrieved_status: bool = False
    approved_strategy: bool = False
    validated_strategy: bool = False
    execution_ready: bool = False

    @field_validator("lifecycle_reference_id")
    @classmethod
    def lifecycle_reference_id_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index lifecycle response placeholder text fields")

    @model_validator(mode="after")
    def lifecycle_response_must_fail_closed(self) -> ResearchArtifactIndexLifecycleResponsePlaceholder:
        dangerous_flags = {
            "indexed status": self.indexed_status,
            "searchable status": self.searchable_status,
            "retrieved status": self.retrieved_status,
            "approved strategy": self.approved_strategy,
            "validated strategy": self.validated_strategy,
            "execution-ready": self.execution_ready,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"Research Artifact Index lifecycle response cannot include: {', '.join(enabled)}")
        return self


class ResearchArtifactIndexApiResponsePlaceholder(_IndexApiResponsePlaceholderBase):
    metadata_response: ResearchArtifactIndexMetadataResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactIndexMetadataResponsePlaceholder(
            response_id="research-artifact-index-api-metadata-response-placeholder-v1",
        )
    )
    key_response: ResearchArtifactIndexKeyResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactIndexKeyResponsePlaceholder(
            response_id="research-artifact-index-api-key-response-placeholder-v1",
        )
    )
    reference_response: ResearchArtifactIndexReferenceResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactIndexReferenceResponsePlaceholder(
            response_id="research-artifact-index-api-reference-response-placeholder-v1",
        )
    )
    tag_response: ResearchArtifactIndexTagResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactIndexTagResponsePlaceholder(
            response_id="research-artifact-index-api-tag-response-placeholder-v1",
        )
    )
    provenance_response: ResearchArtifactIndexProvenanceResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactIndexProvenanceResponsePlaceholder(
            response_id="research-artifact-index-api-provenance-response-placeholder-v1",
        )
    )
    lifecycle_response: ResearchArtifactIndexLifecycleResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactIndexLifecycleResponsePlaceholder(
            response_id="research-artifact-index-api-lifecycle-response-placeholder-v1",
        )
    )
    unavailable_response: ResearchArtifactIndexApiUnavailableResponse = Field(
        default_factory=unavailable_response_template
    )


def default_research_artifact_index_api_response_placeholder() -> ResearchArtifactIndexApiResponsePlaceholder:
    return ResearchArtifactIndexApiResponsePlaceholder(
        response_id="research-artifact-index-api-response-placeholder-v1",
        notes=["Response placeholder contains unavailable metadata only; no index records or generated outputs."],
    )
