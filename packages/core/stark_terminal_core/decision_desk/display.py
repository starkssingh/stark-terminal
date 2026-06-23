from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_desk.planning import (
    _non_empty_text,
    default_forbidden_decision_desk_outputs,
    sanitize_decision_notes,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class RetailDisplayBoundaryContract(BaseModel):
    contract_id: str
    surface_name: str
    allowed_sections: list[str]
    forbidden_sections: list[str]
    planning_only: bool = True
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "surface_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail display boundary text fields")

    @field_validator("allowed_sections")
    @classmethod
    def allowed_sections_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_notes(value)
        if not sanitized:
            raise ValueError("allowed_sections cannot be empty")
        return sanitized

    @field_validator("forbidden_sections")
    @classmethod
    def forbidden_sections_must_cover_safety_boundary(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_notes(value)
        joined = " ".join(sanitized).lower()
        required_concepts = ("recommendation", "action", "confidence", "decisionobject", "execution")
        missing = [concept for concept in required_concepts if concept not in joined]
        if missing:
            raise ValueError("forbidden_sections must include recommendation/action/confidence/DecisionObject/execution")
        return sanitized

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def display_boundary_must_remain_planning_only(self) -> RetailDisplayBoundaryContract:
        if not self.planning_only:
            raise ValueError("retail display boundary must remain planning-only in Prompt 36")
        if self.recommendations_allowed:
            raise ValueError("recommendation display is forbidden in Prompt 36")
        if self.action_generation_allowed:
            raise ValueError("action generation display is forbidden in Prompt 36")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring display is forbidden in Prompt 36")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject display is forbidden in Prompt 36")
        if self.execution_allowed:
            raise ValueError("execution display is forbidden in Prompt 36")
        return self


def default_retail_display_boundary_contract() -> RetailDisplayBoundaryContract:
    return RetailDisplayBoundaryContract(
        contract_id="retail-decision-desk-display-boundary-v1",
        surface_name="Retail Decision Desk Planning Surface",
        allowed_sections=[
            "instrument_context_placeholder",
            "evidence_requirements_summary",
            "data_quality_boundary",
            "risk_context_placeholder",
            "human_review_status",
            "safety_boundary",
        ],
        forbidden_sections=[
            *default_forbidden_decision_desk_outputs(),
            "active_recommendation_cards",
            "generated_action_labels",
            "confidence_score",
            "broker_linkage",
            "execution_buttons",
        ],
        notes=[
            "Prompt 36 implements no retail UI.",
            "Allowed sections are planning-level display boundaries, not rendered recommendations.",
        ],
    )
