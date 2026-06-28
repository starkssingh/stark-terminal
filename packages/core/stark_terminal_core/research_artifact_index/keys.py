from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexKeyKind,
    non_empty_text,
    normalize_datetime,
    optional_text,
    utc_now,
)


class ResearchArtifactIndexKeyPlaceholder(BaseModel):
    key_id: str
    key_kind: ResearchArtifactIndexKeyKind
    key_label: str
    key_value_placeholder: str | None = None
    registry_reference_placeholder: str | None = None
    artifact_reference_placeholder: str | None = None
    schema_version: str = "v1"
    planning_only: bool = True
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("key_id", "key_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index key placeholder text fields")

    @field_validator(
        "key_value_placeholder",
        "registry_reference_placeholder",
        "artifact_reference_placeholder",
    )
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        return optional_text(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def key_must_remain_placeholder(self) -> ResearchArtifactIndexKeyPlaceholder:
        if self.key_kind == ResearchArtifactIndexKeyKind.UNKNOWN:
            raise ValueError("UNKNOWN research artifact index key kind is not allowed")
        if not self.planning_only:
            raise ValueError("research artifact index key must remain planning-only")
        for field_name, value in {
            "key_value_placeholder": self.key_value_placeholder,
            "registry_reference_placeholder": self.registry_reference_placeholder,
            "artifact_reference_placeholder": self.artifact_reference_placeholder,
        }.items():
            if value is not None and "placeholder" not in value.lower():
                raise ValueError(f"{field_name} must remain placeholder-only")
        return self


def default_research_artifact_index_key_placeholders() -> list[ResearchArtifactIndexKeyPlaceholder]:
    return [
        ResearchArtifactIndexKeyPlaceholder(
            key_id="research-artifact-index-artifact-id-key-placeholder-v1",
            key_kind=ResearchArtifactIndexKeyKind.ARTIFACT_ID,
            key_label="Artifact ID placeholder",
            key_value_placeholder="artifact-id-placeholder",
            artifact_reference_placeholder="artifact-reference-placeholder",
        ),
        ResearchArtifactIndexKeyPlaceholder(
            key_id="research-artifact-index-registry-id-key-placeholder-v1",
            key_kind=ResearchArtifactIndexKeyKind.REGISTRY_ID,
            key_label="Registry ID placeholder",
            key_value_placeholder="registry-id-placeholder",
            registry_reference_placeholder="registry-reference-placeholder",
        ),
        ResearchArtifactIndexKeyPlaceholder(
            key_id="research-artifact-index-provenance-id-key-placeholder-v1",
            key_kind=ResearchArtifactIndexKeyKind.PROVENANCE_ID,
            key_label="Provenance ID placeholder",
            key_value_placeholder="provenance-id-placeholder",
        ),
    ]
