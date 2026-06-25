from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_display_notes,
)


class RetailTraderExperienceDisplayUnavailableResponse(BaseModel):
    response_id: str
    unavailable: bool = True
    message: str
    display_contract_only: bool = True
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    suitability_profiling_allowed: bool = False
    safety_label: RetailTraderExperienceDisplaySafetyLabel = (
        RetailTraderExperienceDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience display unavailable response text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> RetailTraderExperienceDisplayUnavailableResponse:
        if not self.unavailable:
            raise ValueError("Retail Trader Experience Display responses must remain unavailable")
        if not self.display_contract_only:
            raise ValueError("Retail Trader Experience Display responses must remain display-contract-only")
        if self.active_ui_allowed:
            raise ValueError("Retail Trader Experience Display active UI is forbidden in Prompt 58")
        if self.frontend_components_allowed:
            raise ValueError("Retail Trader Experience Display frontend components are forbidden in Prompt 58")
        if self.desktop_components_allowed:
            raise ValueError("Retail Trader Experience Display desktop components are forbidden in Prompt 58")
        if self.recommendations_allowed:
            raise ValueError("Retail Trader Experience Display recommendations are forbidden in Prompt 58")
        if self.action_generation_allowed:
            raise ValueError("Retail Trader Experience Display action generation is forbidden in Prompt 58")
        if self.confidence_scoring_allowed:
            raise ValueError("Retail Trader Experience Display confidence scoring is forbidden in Prompt 58")
        if self.decision_object_generation_allowed:
            raise ValueError("Retail Trader Experience Display DecisionObject generation is forbidden in Prompt 58")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Trader Experience Display readiness-to-trade is forbidden in Prompt 58")
        if self.broker_controls_allowed:
            raise ValueError("Retail Trader Experience Display broker controls are forbidden in Prompt 58")
        if self.execution_allowed:
            raise ValueError("Retail Trader Experience Display execution is forbidden in Prompt 58")
        if self.approval_granted:
            raise ValueError("Retail Trader Experience Display approval cannot be granted in Prompt 58")
        if self.override_granted:
            raise ValueError("Retail Trader Experience Display override cannot be granted in Prompt 58")
        if self.suitability_profiling_allowed:
            raise ValueError("Retail Trader Experience Display suitability profiling is forbidden in Prompt 58")
        if self.safety_label == RetailTraderExperienceDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Retail Trader Experience Display safety label cannot be UNKNOWN")
        return self


def default_retail_trader_experience_display_unavailable_response() -> (
    RetailTraderExperienceDisplayUnavailableResponse
):
    return RetailTraderExperienceDisplayUnavailableResponse(
        response_id="retail-trader-experience-display-unavailable-response-v1",
        message=(
            "Retail Trader Experience Display is a display contract skeleton only and returns unavailable "
            "responses in Prompt 58."
        ),
        notes=[
            (
                "Unavailable by default; not active UI, not a recommendation, not suitability profiling, "
                "not readiness-to-trade, and not execution."
            ),
        ],
    )
