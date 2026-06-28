from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class KnowledgeMapEvidenceDisplayPlaceholder(BaseModel):
    evidence_display_id: str
    display_label: str
    descriptive_only: bool = True
    truth_validation_enabled: bool = False
    research_approval_enabled: bool = False
    trade_readiness_enabled: bool = False
    decision_generation_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("evidence_display_id", "display_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map evidence display placeholder text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def evidence_display_must_not_approve_or_decide(self) -> KnowledgeMapEvidenceDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("Research Knowledge Map evidence display placeholders must be descriptive only")
        dangerous_flags = {
            "truth validation": self.truth_validation_enabled,
            "research approval": self.research_approval_enabled,
            "trade readiness": self.trade_readiness_enabled,
            "decision generation": self.decision_generation_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Research Knowledge Map evidence display cannot enable: " + ", ".join(enabled))
        return self


class KnowledgeMapEvidenceReferenceDisplayPlaceholder(KnowledgeMapEvidenceDisplayPlaceholder):
    reference_only: bool = True


def default_knowledge_map_evidence_display_placeholder() -> KnowledgeMapEvidenceDisplayPlaceholder:
    return KnowledgeMapEvidenceDisplayPlaceholder(
        evidence_display_id="research-knowledge-map-evidence-display-placeholder-v1",
        display_label="Knowledge map evidence display placeholder",
        notes=["Evidence display is descriptive only; no truth validation, approval, decision, or trade readiness."],
    )


def default_knowledge_map_evidence_reference_display_placeholder() -> KnowledgeMapEvidenceReferenceDisplayPlaceholder:
    return KnowledgeMapEvidenceReferenceDisplayPlaceholder(
        evidence_display_id="research-knowledge-map-evidence-reference-display-placeholder-v1",
        display_label="Knowledge map evidence reference display placeholder",
        notes=["Evidence reference display is descriptive only and does not validate truth."],
    )
