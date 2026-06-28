from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexKeyKind,
    ResearchArtifactIndexKind,
    ResearchArtifactIndexLifecycleStatus,
    ResearchArtifactIndexTagKind,
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


class _IndexApiRequestPlaceholderBase(BaseModel):
    request_id: str
    api_contract_skeleton_only: bool = True
    executable_request: bool = False
    file_bytes_present: bool = False
    file_path_read_requested: bool = False
    upload_payload_present: bool = False
    fetch_url_present: bool = False
    paper_text_present: bool = False
    parsed_content_present: bool = False
    indexing_payload_present: bool = False
    search_query_execution_requested: bool = False
    ranking_request_present: bool = False
    retrieval_request_present: bool = False
    embedding_payload_present: bool = False
    vector_store_request_present: bool = False
    strategy_logic_present: bool = False
    backtest_parameters_present: bool = False
    recommendation_fields_present: bool = False
    broker_execution_fields_present: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("request_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API request placeholder text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def request_must_fail_closed(self) -> _IndexApiRequestPlaceholderBase:
        if not self.api_contract_skeleton_only:
            raise ValueError("Research Artifact Index API request placeholder must remain contract-skeleton-only")
        dangerous_flags = {
            "executable request": self.executable_request,
            "file bytes": self.file_bytes_present,
            "file path read": self.file_path_read_requested,
            "upload payload": self.upload_payload_present,
            "fetch URL": self.fetch_url_present,
            "paper text": self.paper_text_present,
            "parsed content": self.parsed_content_present,
            "indexing payload": self.indexing_payload_present,
            "search query execution": self.search_query_execution_requested,
            "ranking request": self.ranking_request_present,
            "retrieval request": self.retrieval_request_present,
            "embedding payload": self.embedding_payload_present,
            "vector-store request": self.vector_store_request_present,
            "strategy logic": self.strategy_logic_present,
            "backtest parameters": self.backtest_parameters_present,
            "recommendation fields": self.recommendation_fields_present,
            "broker/execution fields": self.broker_execution_fields_present,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"Research Artifact Index API request placeholder cannot include: {', '.join(enabled)}")
        return self


class ResearchArtifactIndexMetadataRequestPlaceholder(_IndexApiRequestPlaceholderBase):
    index_kind: ResearchArtifactIndexKind = ResearchArtifactIndexKind.METADATA_INDEX_PLACEHOLDER
    requested_metadata_fields: list[str] = Field(default_factory=list)

    @field_validator("requested_metadata_fields")
    @classmethod
    def requested_metadata_fields_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @model_validator(mode="after")
    def metadata_request_must_use_known_kind(self) -> ResearchArtifactIndexMetadataRequestPlaceholder:
        if self.index_kind == ResearchArtifactIndexKind.UNKNOWN:
            raise ValueError("UNKNOWN index kind is not allowed in API request placeholders")
        return self


class ResearchArtifactIndexKeyRequestPlaceholder(_IndexApiRequestPlaceholderBase):
    key_kind: ResearchArtifactIndexKeyKind = ResearchArtifactIndexKeyKind.ARTIFACT_ID
    key_label_placeholder: str = "artifact-id-key-placeholder"

    @field_validator("key_label_placeholder")
    @classmethod
    def placeholder_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API key request placeholder fields")

    @model_validator(mode="after")
    def key_request_must_use_known_kind(self) -> ResearchArtifactIndexKeyRequestPlaceholder:
        if self.key_kind == ResearchArtifactIndexKeyKind.UNKNOWN:
            raise ValueError("UNKNOWN key kind is not allowed in API request placeholders")
        return self


class ResearchArtifactIndexReferenceRequestPlaceholder(_IndexApiRequestPlaceholderBase):
    index_id_placeholder: str = "index-id-placeholder"
    reference_id_placeholder: str = "reference-id-placeholder"
    registry_id_placeholder: str = "registry-id-placeholder"

    @field_validator("index_id_placeholder", "reference_id_placeholder", "registry_id_placeholder")
    @classmethod
    def placeholder_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API reference request placeholder fields")


class ResearchArtifactIndexTagRequestPlaceholder(_IndexApiRequestPlaceholderBase):
    tag_kind: ResearchArtifactIndexTagKind = ResearchArtifactIndexTagKind.TOPIC
    tag_label_placeholder: str = "tag-label-placeholder"

    @field_validator("tag_label_placeholder")
    @classmethod
    def placeholder_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API tag request placeholder fields")

    @model_validator(mode="after")
    def tag_request_must_use_known_kind(self) -> ResearchArtifactIndexTagRequestPlaceholder:
        if self.tag_kind == ResearchArtifactIndexTagKind.UNKNOWN:
            raise ValueError("UNKNOWN tag kind is not allowed in API request placeholders")
        return self


class ResearchArtifactIndexProvenanceRequestPlaceholder(_IndexApiRequestPlaceholderBase):
    index_id_placeholder: str = "index-id-placeholder"
    provenance_id_placeholder: str = "provenance-id-placeholder"

    @field_validator("index_id_placeholder", "provenance_id_placeholder")
    @classmethod
    def placeholder_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API provenance request placeholder fields")


class ResearchArtifactIndexLifecycleRequestPlaceholder(_IndexApiRequestPlaceholderBase):
    index_id_placeholder: str = "index-id-placeholder"
    lifecycle_status: ResearchArtifactIndexLifecycleStatus = ResearchArtifactIndexLifecycleStatus.PLACEHOLDER

    @field_validator("index_id_placeholder")
    @classmethod
    def placeholder_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API lifecycle request placeholder fields")

    @model_validator(mode="after")
    def lifecycle_request_must_use_safe_status(self) -> ResearchArtifactIndexLifecycleRequestPlaceholder:
        if self.lifecycle_status == ResearchArtifactIndexLifecycleStatus.UNKNOWN:
            raise ValueError("UNKNOWN lifecycle status is not allowed in API request placeholders")
        return self


def default_research_artifact_index_metadata_request_placeholder() -> ResearchArtifactIndexMetadataRequestPlaceholder:
    return ResearchArtifactIndexMetadataRequestPlaceholder(
        request_id="research-artifact-index-api-metadata-request-placeholder-v1",
        requested_metadata_fields=["index_id", "index_kind", "title", "schema_version"],
        notes=["Metadata request placeholder only; no indexing, search, retrieval, embeddings, parsing, or execution."],
    )


def default_research_artifact_index_key_request_placeholder() -> ResearchArtifactIndexKeyRequestPlaceholder:
    return ResearchArtifactIndexKeyRequestPlaceholder(
        request_id="research-artifact-index-api-key-request-placeholder-v1",
        notes=["Key request placeholder only; no lookup, ranking, retrieval, or source fetch."],
    )


def default_research_artifact_index_reference_request_placeholder() -> ResearchArtifactIndexReferenceRequestPlaceholder:
    return ResearchArtifactIndexReferenceRequestPlaceholder(
        request_id="research-artifact-index-api-reference-request-placeholder-v1",
        notes=["Reference request placeholder only; no registry lookup, file read, URL fetch, or persistence."],
    )


def default_research_artifact_index_tag_request_placeholder() -> ResearchArtifactIndexTagRequestPlaceholder:
    return ResearchArtifactIndexTagRequestPlaceholder(
        request_id="research-artifact-index-api-tag-request-placeholder-v1",
        notes=["Tag request placeholder only; no search query execution or ranking weight behavior."],
    )


def default_research_artifact_index_provenance_request_placeholder() -> ResearchArtifactIndexProvenanceRequestPlaceholder:
    return ResearchArtifactIndexProvenanceRequestPlaceholder(
        request_id="research-artifact-index-api-provenance-request-placeholder-v1",
        notes=["Provenance request placeholder only; descriptive metadata and no source validation claim."],
    )


def default_research_artifact_index_lifecycle_request_placeholder() -> ResearchArtifactIndexLifecycleRequestPlaceholder:
    return ResearchArtifactIndexLifecycleRequestPlaceholder(
        request_id="research-artifact-index-api-lifecycle-request-placeholder-v1",
        notes=["Lifecycle request placeholder only; no indexed/searchable/retrieved/recommended/executable state."],
    )
