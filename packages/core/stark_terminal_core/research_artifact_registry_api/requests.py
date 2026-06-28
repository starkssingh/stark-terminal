from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactKind,
    ResearchArtifactLifecycleStatus,
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


class _RequestPlaceholderBase(BaseModel):
    request_id: str
    api_contract_skeleton_only: bool = True
    executable_request: bool = False
    file_bytes_present: bool = False
    file_path_read_requested: bool = False
    upload_payload_present: bool = False
    fetch_url_present: bool = False
    paper_text_present: bool = False
    parsed_content_present: bool = False
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
        return non_empty_text(value, "research artifact registry API request placeholder text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def request_must_fail_closed(self) -> _RequestPlaceholderBase:
        if not self.api_contract_skeleton_only:
            raise ValueError("request placeholder must remain API-contract-skeleton-only")
        dangerous_flags = {
            "executable request": self.executable_request,
            "file bytes": self.file_bytes_present,
            "file path read": self.file_path_read_requested,
            "upload payload": self.upload_payload_present,
            "fetch URL": self.fetch_url_present,
            "paper text": self.paper_text_present,
            "parsed content": self.parsed_content_present,
            "strategy logic": self.strategy_logic_present,
            "backtest parameters": self.backtest_parameters_present,
            "recommendation fields": self.recommendation_fields_present,
            "broker/execution fields": self.broker_execution_fields_present,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"request placeholder cannot include: {', '.join(enabled)}")
        return self


class ResearchArtifactMetadataRequestPlaceholder(_RequestPlaceholderBase):
    artifact_kind: ResearchArtifactKind = ResearchArtifactKind.PAPER_REFERENCE
    requested_metadata_fields: list[str] = Field(default_factory=list)

    @field_validator("requested_metadata_fields")
    @classmethod
    def requested_metadata_fields_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @model_validator(mode="after")
    def metadata_request_must_use_known_kind(self) -> ResearchArtifactMetadataRequestPlaceholder:
        if self.artifact_kind == ResearchArtifactKind.UNKNOWN:
            raise ValueError("UNKNOWN artifact kind is not allowed in API request placeholders")
        return self


class ResearchArtifactReferenceRequestPlaceholder(_RequestPlaceholderBase):
    artifact_id_placeholder: str = "artifact-id-placeholder"
    reference_id_placeholder: str = "reference-id-placeholder"

    @field_validator("artifact_id_placeholder", "reference_id_placeholder")
    @classmethod
    def placeholder_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact API reference request placeholder fields")


class ResearchArtifactProvenanceRequestPlaceholder(_RequestPlaceholderBase):
    artifact_id_placeholder: str = "artifact-id-placeholder"
    provenance_id_placeholder: str = "provenance-id-placeholder"

    @field_validator("artifact_id_placeholder", "provenance_id_placeholder")
    @classmethod
    def placeholder_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact API provenance request placeholder fields")


class ResearchArtifactLifecycleRequestPlaceholder(_RequestPlaceholderBase):
    artifact_id_placeholder: str = "artifact-id-placeholder"
    lifecycle_status: ResearchArtifactLifecycleStatus = ResearchArtifactLifecycleStatus.PLACEHOLDER

    @field_validator("artifact_id_placeholder")
    @classmethod
    def placeholder_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact API lifecycle request placeholder fields")

    @model_validator(mode="after")
    def lifecycle_request_must_use_safe_status(self) -> ResearchArtifactLifecycleRequestPlaceholder:
        if self.lifecycle_status == ResearchArtifactLifecycleStatus.UNKNOWN:
            raise ValueError("UNKNOWN lifecycle status is not allowed in API request placeholders")
        return self


def default_research_artifact_metadata_request_placeholder() -> ResearchArtifactMetadataRequestPlaceholder:
    return ResearchArtifactMetadataRequestPlaceholder(
        request_id="research-artifact-api-metadata-request-placeholder-v1",
        requested_metadata_fields=["artifact_id", "artifact_kind", "title", "lifecycle_status"],
        notes=["Metadata request placeholder only; no upload, fetch, parse, strategy, backtest, or execution."],
    )


def default_research_artifact_reference_request_placeholder() -> ResearchArtifactReferenceRequestPlaceholder:
    return ResearchArtifactReferenceRequestPlaceholder(
        request_id="research-artifact-api-reference-request-placeholder-v1",
        notes=["Reference request placeholder only; no file read, URL fetch, download, or checksum validation."],
    )


def default_research_artifact_provenance_request_placeholder() -> ResearchArtifactProvenanceRequestPlaceholder:
    return ResearchArtifactProvenanceRequestPlaceholder(
        request_id="research-artifact-api-provenance-request-placeholder-v1",
        notes=["Provenance request placeholder only; descriptive metadata and no source trust claim."],
    )


def default_research_artifact_lifecycle_request_placeholder() -> ResearchArtifactLifecycleRequestPlaceholder:
    return ResearchArtifactLifecycleRequestPlaceholder(
        request_id="research-artifact-api-lifecycle-request-placeholder-v1",
        notes=["Lifecycle request placeholder only; no approval, readiness-to-trade, or execution state."],
    )
