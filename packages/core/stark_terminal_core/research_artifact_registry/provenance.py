from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactProvenanceSourceType,
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


class ResearchArtifactProvenancePlaceholder(BaseModel):
    provenance_id: str
    artifact_id: str
    source_type: ResearchArtifactProvenanceSourceType
    source_label: str | None = None
    source_data_reference: str | None = None
    audit_notes: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("provenance_id", "artifact_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact provenance placeholder text fields")

    @field_validator("source_label", "source_data_reference")
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("audit_notes")
    @classmethod
    def audit_notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def provenance_must_remain_descriptive(self) -> ResearchArtifactProvenancePlaceholder:
        if self.source_type == ResearchArtifactProvenanceSourceType.UNKNOWN:
            raise ValueError("UNKNOWN research artifact provenance source type is not allowed")
        if self.source_data_reference is not None and "placeholder" not in self.source_data_reference.lower():
            raise ValueError("source_data_reference must remain placeholder-only")
        forbidden_claims = {"trusted real market data", "validated real market data", "production data"}
        searchable = " ".join([*(self.audit_notes or []), self.source_label or ""]).lower()
        if any(claim in searchable for claim in forbidden_claims):
            raise ValueError("provenance placeholder cannot claim trusted real market data")
        return self


def default_research_artifact_provenance_placeholders() -> list[ResearchArtifactProvenancePlaceholder]:
    return [
        ResearchArtifactProvenancePlaceholder(
            provenance_id="research-artifact-paper-provenance-placeholder-v1",
            artifact_id="research-artifact-paper-reference-placeholder-v1",
            source_type=ResearchArtifactProvenanceSourceType.PAPER_REFERENCE,
            source_label="Paper reference provenance placeholder",
            source_data_reference="paper-source-data-placeholder",
            audit_notes=["Descriptive only; no paper ingestion, parsing, or method extraction."],
        ),
        ResearchArtifactProvenancePlaceholder(
            provenance_id="research-artifact-dataset-provenance-placeholder-v1",
            artifact_id="research-artifact-dataset-reference-placeholder-v1",
            source_type=ResearchArtifactProvenanceSourceType.DATASET_REFERENCE,
            source_label="Dataset reference provenance placeholder",
            source_data_reference="dataset-source-data-placeholder",
            audit_notes=["Descriptive only; no real/live data trust claim."],
        ),
        ResearchArtifactProvenancePlaceholder(
            provenance_id="research-artifact-hypothesis-provenance-placeholder-v1",
            artifact_id="research-artifact-hypothesis-reference-placeholder-v1",
            source_type=ResearchArtifactProvenanceSourceType.LOCAL_REFERENCE_PLACEHOLDER,
            source_label="Hypothesis provenance placeholder",
            source_data_reference="hypothesis-source-data-placeholder",
            audit_notes=["Descriptive only; no strategy generation."],
        ),
        ResearchArtifactProvenancePlaceholder(
            provenance_id="research-artifact-experiment-provenance-placeholder-v1",
            artifact_id="research-artifact-experiment-reference-placeholder-v1",
            source_type=ResearchArtifactProvenanceSourceType.LOCAL_REFERENCE_PLACEHOLDER,
            source_label="Experiment provenance placeholder",
            source_data_reference="experiment-source-data-placeholder",
            audit_notes=["Descriptive only; no executable backtest or optimization."],
        ),
    ]

