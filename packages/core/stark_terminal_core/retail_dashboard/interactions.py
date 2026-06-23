from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard.planning import (
    RetailDashboardForbiddenInteractionKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_notes,
)


class RetailDashboardForbiddenInteraction(BaseModel):
    interaction_id: str
    kind: RetailDashboardForbiddenInteractionKind
    name: str
    description: str
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("interaction_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard forbidden interaction text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def forbidden_interaction_must_fail_closed(self) -> RetailDashboardForbiddenInteraction:
        if self.kind == RetailDashboardForbiddenInteractionKind.UNKNOWN:
            raise ValueError("UNKNOWN retail dashboard forbidden interaction kind is not allowed")
        if not self.forbidden_now:
            raise ValueError("retail dashboard forbidden interactions cannot be unlocked in Prompt 49")
        if not self.requires_future_prompt:
            raise ValueError("retail dashboard forbidden interactions require a future prompt before unlock")
        if not self.requires_audit_before_unlock:
            raise ValueError("retail dashboard forbidden interactions require audit before unlock")
        return self


def default_retail_dashboard_forbidden_interactions() -> list[RetailDashboardForbiddenInteraction]:
    specs = [
        (RetailDashboardForbiddenInteractionKind.RECOMMENDATION_CARD, "Recommendation card"),
        (RetailDashboardForbiddenInteractionKind.ACTION_BUTTON, "Action button"),
        (RetailDashboardForbiddenInteractionKind.CONFIDENCE_SCORE, "Confidence score"),
        (RetailDashboardForbiddenInteractionKind.DECISION_OBJECT_DISPLAY, "DecisionObject display"),
        (RetailDashboardForbiddenInteractionKind.READINESS_TO_TRADE_BADGE, "Readiness-to-trade badge"),
        (RetailDashboardForbiddenInteractionKind.BROKER_CONTROL, "Broker control"),
        (RetailDashboardForbiddenInteractionKind.ORDER_BUTTON, "Order button"),
        (RetailDashboardForbiddenInteractionKind.APPROVAL_CONTROL, "Approval control"),
        (RetailDashboardForbiddenInteractionKind.OVERRIDE_CONTROL, "Override control"),
        (RetailDashboardForbiddenInteractionKind.LIVE_DATA_CONTROL, "Live data control"),
    ]
    return [
        RetailDashboardForbiddenInteraction(
            interaction_id=f"retail-dashboard-forbidden-{kind.value.lower().replace('_', '-')}-v1",
            kind=kind,
            name=name,
            description=f"{name} is forbidden in Prompt 49 Retail Dashboard planning and guardrails.",
            notes=[
                "Requires a future prompt before unlock.",
                "Requires audit-before-unlock and does not enable active UI, recommendation, broker control, or execution.",
            ],
        )
        for kind, name in specs
    ]
