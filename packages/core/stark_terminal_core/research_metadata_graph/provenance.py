from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class GraphProvenanceReferencePlaceholder(BaseModel):
    reference_id: str
    label: str
    description: str
    descriptive_only: bool = True
    validates_source_truth: bool = False
    external_fetch_enabled: bool = False
    local_file_read_enabled: bool = False
    trusted_research_status: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("reference_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph provenance text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def provenance_must_remain_descriptive(self) -> GraphProvenanceReferencePlaceholder:
        if not self.descriptive_only:
            raise ValueError("graph provenance placeholders must remain descriptive only")
        dangerous_flags = {
            "source truth validation": self.validates_source_truth,
            "external fetch": self.external_fetch_enabled,
            "local file read": self.local_file_read_enabled,
            "trusted research status": self.trusted_research_status,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("graph provenance placeholder cannot enable: " + ", ".join(enabled))
        return self


class GraphSourceReferencePlaceholder(GraphProvenanceReferencePlaceholder):
    pass


class GraphAuditReferencePlaceholder(GraphProvenanceReferencePlaceholder):
    pass


def default_graph_provenance_reference_placeholders() -> list[GraphProvenanceReferencePlaceholder]:
    return [
        GraphSourceReferencePlaceholder(
            reference_id="research-metadata-graph-source-reference-placeholder",
            label="Graph source reference placeholder",
            description="Descriptive source reference only; no external fetch or trust claim.",
        ),
        GraphAuditReferencePlaceholder(
            reference_id="research-metadata-graph-audit-reference-placeholder",
            label="Graph audit reference placeholder",
            description="Descriptive audit reference only; no validation or persistence behavior.",
        ),
    ]
