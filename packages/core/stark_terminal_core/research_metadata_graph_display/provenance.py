from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_metadata_graph.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class GraphProvenanceDisplayPlaceholder(BaseModel):
    placeholder_id: str
    provenance_kind: str
    display_label: str
    descriptive_only: bool = True
    source_truth_validation_enabled: bool = False
    external_fetch_enabled: bool = False
    local_file_read_enabled: bool = False
    trusted_research_status_implied: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("placeholder_id", "provenance_kind", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph provenance display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def provenance_display_must_remain_descriptive(self) -> GraphProvenanceDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Metadata Graph provenance display placeholders must be descriptive only")
        dangerous_flags = {
            "source truth validation": self.source_truth_validation_enabled,
            "external fetch": self.external_fetch_enabled,
            "local file read": self.local_file_read_enabled,
            "trusted research status": self.trusted_research_status_implied,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(
                "Research Metadata Graph provenance display placeholder cannot enable: " + ", ".join(enabled)
            )
        return self


class GraphSourceDisplayPlaceholder(GraphProvenanceDisplayPlaceholder):
    provenance_kind: str = "GRAPH_SOURCE_DISPLAY_PLACEHOLDER"


class GraphAuditDisplayPlaceholder(GraphProvenanceDisplayPlaceholder):
    provenance_kind: str = "GRAPH_AUDIT_DISPLAY_PLACEHOLDER"


def default_graph_provenance_display_placeholder() -> GraphProvenanceDisplayPlaceholder:
    return GraphProvenanceDisplayPlaceholder(
        placeholder_id="research-metadata-graph-provenance-display-placeholder-v1",
        provenance_kind="GRAPH_PROVENANCE_DISPLAY_PLACEHOLDER",
        display_label="Graph provenance display placeholder",
        notes=["Descriptive provenance display only; no source truth validation or external fetch."],
    )


def default_graph_source_display_placeholder() -> GraphSourceDisplayPlaceholder:
    return GraphSourceDisplayPlaceholder(
        placeholder_id="research-metadata-graph-source-display-placeholder-v1",
        display_label="Graph source display placeholder",
    )


def default_graph_audit_display_placeholder() -> GraphAuditDisplayPlaceholder:
    return GraphAuditDisplayPlaceholder(
        placeholder_id="research-metadata-graph-audit-display-placeholder-v1",
        display_label="Graph audit display placeholder",
    )
