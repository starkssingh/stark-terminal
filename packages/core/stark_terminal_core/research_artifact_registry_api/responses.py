from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)
from stark_terminal_core.research_artifact_registry_api.references import (
    ResearchArtifactApiReferencePlaceholder,
    ResearchArtifactMetadataReferencePlaceholder,
    ResearchArtifactProvenanceReferencePlaceholder,
    default_research_artifact_api_reference_placeholder,
    default_research_artifact_metadata_reference_placeholder,
    default_research_artifact_provenance_reference_placeholder,
)
from stark_terminal_core.research_artifact_registry_api.unavailable import (
    ResearchArtifactRegistryApiUnavailableResponse,
    unavailable_response_template,
)


class _ResponsePlaceholderBase(BaseModel):
    response_id: str
    unavailable: bool = True
    placeholder_only: bool = True
    persistent_record_created: bool = False
    validated_artifact_record: bool = False
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
        return non_empty_text(value, "research artifact registry API response placeholder text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def response_must_fail_closed(self) -> _ResponsePlaceholderBase:
        if not self.unavailable:
            raise ValueError("API response placeholder must remain unavailable")
        if not self.placeholder_only:
            raise ValueError("API response placeholder must remain placeholder-only")
        dangerous_flags = {
            "persistent record": self.persistent_record_created,
            "validated artifact": self.validated_artifact_record,
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
            raise ValueError(f"API response placeholder cannot include: {', '.join(enabled)}")
        return self


class ResearchArtifactMetadataResponsePlaceholder(_ResponsePlaceholderBase):
    metadata_reference: ResearchArtifactMetadataReferencePlaceholder = Field(
        default_factory=default_research_artifact_metadata_reference_placeholder
    )


class ResearchArtifactReferenceResponsePlaceholder(_ResponsePlaceholderBase):
    api_reference: ResearchArtifactApiReferencePlaceholder = Field(
        default_factory=default_research_artifact_api_reference_placeholder
    )


class ResearchArtifactProvenanceResponsePlaceholder(_ResponsePlaceholderBase):
    provenance_reference: ResearchArtifactProvenanceReferencePlaceholder = Field(
        default_factory=default_research_artifact_provenance_reference_placeholder
    )


class ResearchArtifactLifecycleResponsePlaceholder(_ResponsePlaceholderBase):
    lifecycle_reference_id: str = "research-artifact-api-lifecycle-reference-placeholder-v1"
    approved_strategy: bool = False
    validated_strategy: bool = False
    execution_ready: bool = False

    @field_validator("lifecycle_reference_id")
    @classmethod
    def lifecycle_reference_id_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact lifecycle response placeholder text fields")

    @model_validator(mode="after")
    def lifecycle_response_must_fail_closed(self) -> ResearchArtifactLifecycleResponsePlaceholder:
        if self.approved_strategy:
            raise ValueError("lifecycle response cannot approve a strategy")
        if self.validated_strategy:
            raise ValueError("lifecycle response cannot validate a strategy")
        if self.execution_ready:
            raise ValueError("lifecycle response cannot be execution-ready")
        return self


class ResearchArtifactRegistryApiResponsePlaceholder(_ResponsePlaceholderBase):
    metadata_response: ResearchArtifactMetadataResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactMetadataResponsePlaceholder(
            response_id="research-artifact-api-metadata-response-placeholder-v1",
        )
    )
    reference_response: ResearchArtifactReferenceResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactReferenceResponsePlaceholder(
            response_id="research-artifact-api-reference-response-placeholder-v1",
        )
    )
    provenance_response: ResearchArtifactProvenanceResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactProvenanceResponsePlaceholder(
            response_id="research-artifact-api-provenance-response-placeholder-v1",
        )
    )
    lifecycle_response: ResearchArtifactLifecycleResponsePlaceholder = Field(
        default_factory=lambda: ResearchArtifactLifecycleResponsePlaceholder(
            response_id="research-artifact-api-lifecycle-response-placeholder-v1",
        )
    )
    unavailable_response: ResearchArtifactRegistryApiUnavailableResponse = Field(
        default_factory=unavailable_response_template
    )


def default_research_artifact_registry_api_response_placeholder() -> ResearchArtifactRegistryApiResponsePlaceholder:
    return ResearchArtifactRegistryApiResponsePlaceholder(
        response_id="research-artifact-registry-api-response-placeholder-v1",
        notes=["Response placeholder contains unavailable metadata only; no registry persistence or generated outputs."],
    )
