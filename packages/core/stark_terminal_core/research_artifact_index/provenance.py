from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    non_empty_text,
    normalize_datetime,
    optional_text,
    sanitize_text_list,
    utc_now,
)


class ResearchArtifactIndexProvenancePlaceholder(BaseModel):
    provenance_id: str
    index_id: str
    registry_reference_placeholder: str | None = None
    source_reference_placeholder: str | None = None
    audit_notes: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    planning_only: bool = True
    source_validated: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("provenance_id", "index_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index provenance placeholder text fields")

    @field_validator("registry_reference_placeholder", "source_reference_placeholder")
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        return optional_text(value)

    @field_validator("audit_notes")
    @classmethod
    def audit_notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def provenance_must_remain_descriptive(self) -> ResearchArtifactIndexProvenancePlaceholder:
        if not self.planning_only:
            raise ValueError("research artifact index provenance must remain planning-only")
        if self.source_validated:
            raise ValueError("research artifact index provenance source_validated must remain false")
        for field_name, value in {
            "registry_reference_placeholder": self.registry_reference_placeholder,
            "source_reference_placeholder": self.source_reference_placeholder,
        }.items():
            if value is not None and "placeholder" not in value.lower():
                raise ValueError(f"{field_name} must remain placeholder-only")
        searchable = " ".join([*(self.audit_notes or []), self.registry_reference_placeholder or ""]).lower()
        if "trusted real market data" in searchable or "validated real market data" in searchable:
            raise ValueError("research artifact index provenance cannot claim trusted real market data")
        return self


def default_research_artifact_index_provenance_placeholders() -> list[ResearchArtifactIndexProvenancePlaceholder]:
    return [
        ResearchArtifactIndexProvenancePlaceholder(
            provenance_id="research-artifact-index-provenance-placeholder-v1",
            index_id="research-artifact-index-metadata-placeholder-v1",
            registry_reference_placeholder="registry-reference-placeholder",
            source_reference_placeholder="source-reference-placeholder",
            audit_notes=["Descriptive only; no external fetch, validation, indexing, or storage."],
        )
    ]
