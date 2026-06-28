from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    non_empty_text,
    normalize_datetime,
    optional_text,
    utc_now,
)


class ResearchArtifactIndexReferencePlaceholder(BaseModel):
    reference_id: str
    index_id: str
    artifact_id_placeholder: str | None = None
    registry_id_placeholder: str | None = None
    provenance_id_placeholder: str | None = None
    lifecycle_id_placeholder: str | None = None
    source_label: str | None = None
    schema_version: str = "v1"
    planning_only: bool = True
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("reference_id", "index_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index reference placeholder text fields")

    @field_validator(
        "artifact_id_placeholder",
        "registry_id_placeholder",
        "provenance_id_placeholder",
        "lifecycle_id_placeholder",
        "source_label",
    )
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        return optional_text(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def reference_must_remain_descriptive(self) -> ResearchArtifactIndexReferencePlaceholder:
        if not self.planning_only:
            raise ValueError("research artifact index reference must remain planning-only")
        for field_name, value in {
            "artifact_id_placeholder": self.artifact_id_placeholder,
            "registry_id_placeholder": self.registry_id_placeholder,
            "provenance_id_placeholder": self.provenance_id_placeholder,
            "lifecycle_id_placeholder": self.lifecycle_id_placeholder,
        }.items():
            if value is not None and "placeholder" not in value.lower():
                raise ValueError(f"{field_name} must remain placeholder-only")
        searchable = " ".join(
            value or ""
            for value in [
                self.source_label,
                self.artifact_id_placeholder,
                self.registry_id_placeholder,
                self.provenance_id_placeholder,
                self.lifecycle_id_placeholder,
            ]
        ).lower()
        forbidden_claims = {"validated source", "trusted source", "real market data"}
        if any(claim in searchable for claim in forbidden_claims):
            raise ValueError("research artifact index reference cannot claim source trust")
        return self


def default_research_artifact_index_reference_placeholders() -> list[ResearchArtifactIndexReferencePlaceholder]:
    return [
        ResearchArtifactIndexReferencePlaceholder(
            reference_id="research-artifact-index-registry-reference-placeholder-v1",
            index_id="research-artifact-index-metadata-placeholder-v1",
            artifact_id_placeholder="artifact-id-placeholder",
            registry_id_placeholder="registry-id-placeholder",
            provenance_id_placeholder="provenance-id-placeholder",
            lifecycle_id_placeholder="lifecycle-id-placeholder",
            source_label="Descriptive registry reference placeholder",
        ),
        ResearchArtifactIndexReferencePlaceholder(
            reference_id="research-artifact-index-artifact-reference-placeholder-v1",
            index_id="research-artifact-index-key-placeholder-v1",
            artifact_id_placeholder="artifact-reference-placeholder",
            source_label="Descriptive artifact reference placeholder",
        ),
    ]
