from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class KnowledgeMapProvenanceDisplayPlaceholder(BaseModel):
    provenance_display_id: str
    display_label: str
    descriptive_only: bool = True
    external_fetch_enabled: bool = False
    local_file_read_enabled: bool = False
    source_validation_enabled: bool = False
    trusted_research_status_implied: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("provenance_display_id", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map provenance display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def provenance_display_must_remain_descriptive(self) -> KnowledgeMapProvenanceDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Knowledge Map provenance display placeholders must be descriptive only")
        dangerous_flags = {
            "external fetch": self.external_fetch_enabled,
            "local file read": self.local_file_read_enabled,
            "source validation": self.source_validation_enabled,
            "trusted research status": self.trusted_research_status_implied,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Knowledge Map provenance display cannot enable: " + ", ".join(enabled))
        return self


class KnowledgeMapSourceDisplayPlaceholder(KnowledgeMapProvenanceDisplayPlaceholder):
    source_display_only: bool = True


class KnowledgeMapAuditDisplayPlaceholder(KnowledgeMapProvenanceDisplayPlaceholder):
    audit_display_only: bool = True


def default_knowledge_map_provenance_display_placeholder() -> KnowledgeMapProvenanceDisplayPlaceholder:
    return KnowledgeMapProvenanceDisplayPlaceholder(
        provenance_display_id="research-knowledge-map-provenance-display-placeholder-v1",
        display_label="Knowledge map provenance display placeholder",
        notes=["Provenance display is descriptive only; no external fetch, file read, or source validation."],
    )


def default_knowledge_map_source_display_placeholder() -> KnowledgeMapSourceDisplayPlaceholder:
    return KnowledgeMapSourceDisplayPlaceholder(
        provenance_display_id="research-knowledge-map-source-display-placeholder-v1",
        display_label="Knowledge map source display placeholder",
        notes=["Source display does not imply trusted research status."],
    )


def default_knowledge_map_audit_display_placeholder() -> KnowledgeMapAuditDisplayPlaceholder:
    return KnowledgeMapAuditDisplayPlaceholder(
        provenance_display_id="research-knowledge-map-audit-display-placeholder-v1",
        display_label="Knowledge map audit display placeholder",
        notes=["Audit display is reference metadata only and does not approve research."],
    )
