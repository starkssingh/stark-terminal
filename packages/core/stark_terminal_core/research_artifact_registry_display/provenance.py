from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


class ResearchArtifactProvenanceDisplayPlaceholder(BaseModel):
    provenance_display_id: str
    provenance_reference_placeholder: str = "provenance-reference-placeholder"
    descriptive_only: bool = True
    source_validation_claim: bool = False
    external_fetch_enabled: bool = False
    real_data_trust_claim: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    audit_notes: list[str] = Field(default_factory=list)

    @field_validator("provenance_display_id", "provenance_reference_placeholder", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact provenance display placeholder text fields")

    @field_validator("audit_notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def provenance_display_must_fail_closed(self) -> ResearchArtifactProvenanceDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("provenance display must remain descriptive only")
        dangerous_flags = {
            "source validation claim": self.source_validation_claim,
            "external fetch": self.external_fetch_enabled,
            "real data trust claim": self.real_data_trust_claim,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"provenance display placeholder cannot enable: {', '.join(enabled)}")
        return self


def default_research_artifact_provenance_display_placeholder() -> ResearchArtifactProvenanceDisplayPlaceholder:
    return ResearchArtifactProvenanceDisplayPlaceholder(
        provenance_display_id="research-artifact-provenance-display-placeholder-v1",
        audit_notes=["Descriptive display placeholder only; no source validation or trust claim."],
    )
