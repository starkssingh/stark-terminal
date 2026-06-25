from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace.planning import (
    StrategyResearchForbiddenInteractionKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_notes,
)


class StrategyResearchForbiddenInteraction(BaseModel):
    interaction_id: str
    kind: StrategyResearchForbiddenInteractionKind
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
        return _non_empty_text(value, "strategy research forbidden interaction text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def interaction_must_remain_forbidden(self) -> StrategyResearchForbiddenInteraction:
        if self.kind == StrategyResearchForbiddenInteractionKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research forbidden interaction kind is not allowed")
        if not self.forbidden_now:
            raise ValueError("Strategy Research forbidden interaction cannot be unlocked in Prompt 63")
        if not self.requires_future_prompt:
            raise ValueError("Strategy Research forbidden interaction requires a future prompt")
        if not self.requires_audit_before_unlock:
            raise ValueError("Strategy Research forbidden interaction requires audit before unlock")
        return self


def default_strategy_research_forbidden_interactions() -> list[StrategyResearchForbiddenInteraction]:
    return [
        StrategyResearchForbiddenInteraction(
            interaction_id=f"strategy-research-forbidden-{kind.value.lower().replace('_', '-')}-v1",
            kind=kind,
            name=kind.value.replace("_", " ").title(),
            description=f"{kind.value.replace('_', ' ').lower()} is forbidden in Strategy Research Workspace Prompt 63.",
            notes=["Future prompt and audit-before-unlock are required before this behavior can be reconsidered."],
        )
        for kind in StrategyResearchForbiddenInteractionKind
        if kind != StrategyResearchForbiddenInteractionKind.UNKNOWN
    ]
