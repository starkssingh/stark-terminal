from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_knowledge_map.planning import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class KnowledgeMapEvidencePlaceholder(BaseModel):
    evidence_id: str
    label: str
    description: str
    descriptive_only: bool = True
    validates_truth: bool = False
    approves_research: bool = False
    creates_trade_readiness: bool = False
    decision_generation_enabled: bool = False
    recommendation_enabled: bool = False
    execution_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("evidence_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map evidence text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def evidence_must_remain_descriptive(self) -> KnowledgeMapEvidencePlaceholder:
        if not self.descriptive_only:
            raise ValueError("research knowledge map evidence placeholders must remain descriptive only")
        dangerous_flags = {
            "truth validation": self.validates_truth,
            "research approval": self.approves_research,
            "trade readiness": self.creates_trade_readiness,
            "decision generation": self.decision_generation_enabled,
            "recommendation": self.recommendation_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research knowledge map evidence placeholder cannot enable: " + ", ".join(enabled))
        return self


class KnowledgeMapEvidenceReferencePlaceholder(KnowledgeMapEvidencePlaceholder):
    pass


def default_research_knowledge_map_evidence_placeholders() -> list[KnowledgeMapEvidencePlaceholder]:
    return [
        KnowledgeMapEvidencePlaceholder(
            evidence_id="research-knowledge-map-evidence-placeholder",
            label="Knowledge map evidence placeholder",
            description="Descriptive evidence placeholder only; no truth validation, approval, recommendation, or decision.",
        ),
        KnowledgeMapEvidenceReferencePlaceholder(
            evidence_id="research-knowledge-map-evidence-reference-placeholder",
            label="Knowledge map evidence reference placeholder",
            description="Descriptive evidence reference only; no trade readiness or execution path.",
        ),
    ]
