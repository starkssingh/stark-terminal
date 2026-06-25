from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplayJourneyKind,
    RetailTraderExperienceDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_display_notes,
)


class RetailTraderExperienceDisplayJourneyPlaceholder(BaseModel):
    journey_id: str
    journey_kind: RetailTraderExperienceDisplayJourneyKind
    title: str
    description: str
    display_contract_only: bool = True
    active_ui: bool = False
    rendered_now: bool = False
    unavailable: bool = True
    recommendation_journey: bool = False
    trading_advice_journey: bool = False
    broker_control_journey: bool = False
    execution_journey: bool = False
    readiness_to_trade_journey: bool = False
    approval_journey: bool = False
    override_journey: bool = False
    safety_label: RetailTraderExperienceDisplaySafetyLabel = (
        RetailTraderExperienceDisplaySafetyLabel.NOT_A_RECOMMENDATION
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("journey_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience display journey text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def journey_placeholder_must_fail_closed(self) -> RetailTraderExperienceDisplayJourneyPlaceholder:
        if self.journey_kind == RetailTraderExperienceDisplayJourneyKind.UNKNOWN:
            raise ValueError("UNKNOWN Retail Trader Experience Display journey kind is not allowed")
        if not self.display_contract_only:
            raise ValueError("Retail Trader Experience Display journey must remain display-contract-only")
        if self.active_ui or self.rendered_now:
            raise ValueError("Retail Trader Experience Display journey cannot be active or rendered")
        if not self.unavailable:
            raise ValueError("Retail Trader Experience Display journey must remain unavailable")
        if (
            self.recommendation_journey
            or self.trading_advice_journey
            or self.broker_control_journey
            or self.execution_journey
            or self.readiness_to_trade_journey
            or self.approval_journey
            or self.override_journey
        ):
            raise ValueError("Retail Trader Experience Display journey dangerous flags must be false")
        if self.safety_label == RetailTraderExperienceDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Retail Trader Experience Display journey safety label cannot be UNKNOWN")
        return self


def default_retail_trader_experience_display_journey_placeholders() -> list[
    RetailTraderExperienceDisplayJourneyPlaceholder
]:
    return [
        RetailTraderExperienceDisplayJourneyPlaceholder(
            journey_id="onboarding-visual-placeholder",
            journey_kind=RetailTraderExperienceDisplayJourneyKind.ONBOARDING_VISUAL_PLACEHOLDER,
            title="Onboarding visual placeholder",
            description="Display contract placeholder only; no active onboarding UI is rendered.",
        ),
        RetailTraderExperienceDisplayJourneyPlaceholder(
            journey_id="instrument-review-visual-placeholder",
            journey_kind=RetailTraderExperienceDisplayJourneyKind.INSTRUMENT_REVIEW_VISUAL_PLACEHOLDER,
            title="Instrument review visual placeholder",
            description="Placeholder only; not trading advice and not a recommendation journey.",
        ),
        RetailTraderExperienceDisplayJourneyPlaceholder(
            journey_id="dashboard-context-visual-placeholder",
            journey_kind=RetailTraderExperienceDisplayJourneyKind.DASHBOARD_CONTEXT_VISUAL_PLACEHOLDER,
            title="Dashboard context visual placeholder",
            description="Placeholder only; no active dashboard output or live market data display.",
        ),
        RetailTraderExperienceDisplayJourneyPlaceholder(
            journey_id="safety-context-visual-placeholder",
            journey_kind=RetailTraderExperienceDisplayJourneyKind.SAFETY_CONTEXT_VISUAL_PLACEHOLDER,
            title="Safety context visual placeholder",
            description="Placeholder only; no safety pass, approval, override, or readiness-to-trade.",
        ),
        RetailTraderExperienceDisplayJourneyPlaceholder(
            journey_id="evidence-review-visual-placeholder",
            journey_kind=RetailTraderExperienceDisplayJourneyKind.EVIDENCE_REVIEW_VISUAL_PLACEHOLDER,
            title="Evidence review visual placeholder",
            description="Placeholder only; no active DecisionObject or validated recommendation display.",
        ),
        RetailTraderExperienceDisplayJourneyPlaceholder(
            journey_id="human-review-visual-placeholder",
            journey_kind=RetailTraderExperienceDisplayJourneyKind.HUMAN_REVIEW_VISUAL_PLACEHOLDER,
            title="Human review visual placeholder",
            description="Placeholder only; no active workflow, approval, override, or task assignment.",
        ),
        RetailTraderExperienceDisplayJourneyPlaceholder(
            journey_id="unavailable-notice-visual-placeholder",
            journey_kind=RetailTraderExperienceDisplayJourneyKind.UNAVAILABLE_NOTICE,
            title="Unavailable notice visual placeholder",
            description="Fail-closed journey placeholder expected during Prompt 58.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY,
        ),
    ]
