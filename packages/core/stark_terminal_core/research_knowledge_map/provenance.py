from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class KnowledgeMapProvenancePlaceholder(BaseModel):
    provenance_id: str
    label: str
    description: str
    descriptive_only: bool = True
    external_fetch_enabled: bool = False
    local_file_read_enabled: bool = False
    source_validation_enabled: bool = False
    trusted_research_status: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("provenance_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map provenance text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def provenance_must_remain_descriptive(self) -> KnowledgeMapProvenancePlaceholder:
        if not self.descriptive_only:
            raise ValueError("research knowledge map provenance placeholders must remain descriptive only")
        dangerous_flags = {
            "external fetch": self.external_fetch_enabled,
            "local file read": self.local_file_read_enabled,
            "source validation": self.source_validation_enabled,
            "trusted research status": self.trusted_research_status,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research knowledge map provenance placeholder cannot enable: " + ", ".join(enabled))
        return self


class KnowledgeMapSourcePlaceholder(KnowledgeMapProvenancePlaceholder):
    pass


class KnowledgeMapAuditPlaceholder(KnowledgeMapProvenancePlaceholder):
    pass


def default_research_knowledge_map_provenance_placeholders() -> list[KnowledgeMapProvenancePlaceholder]:
    return [
        KnowledgeMapSourcePlaceholder(
            provenance_id="research-knowledge-map-source-placeholder",
            label="Knowledge map source placeholder",
            description="Descriptive source placeholder only; no fetch, file read, validation, or trust claim.",
        ),
        KnowledgeMapAuditPlaceholder(
            provenance_id="research-knowledge-map-audit-placeholder",
            label="Knowledge map audit placeholder",
            description="Descriptive audit placeholder only; no approval or source-truth validation.",
        ),
    ]
