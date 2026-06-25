from __future__ import annotations

from datetime import datetime
from typing import Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplayContractMetadata,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_display_notes,
)
from stark_terminal_core.retail_trader_experience_display.journeys import (
    RetailTraderExperienceDisplayJourneyPlaceholder,
)
from stark_terminal_core.retail_trader_experience_display.personas import (
    RetailTraderExperienceDisplayPersonaPlaceholder,
)
from stark_terminal_core.retail_trader_experience_display.widgets import (
    RetailTraderExperienceDisplayWidgetPlaceholder,
)


class RetailTraderExperienceDisplaySafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_active_ui: bool = False
    allow_frontend_components: bool = False
    allow_desktop_components: bool = False
    allow_recommendations: bool = False
    allow_action_generation: bool = False
    allow_confidence_scoring: bool = False
    allow_decision_object_generation: bool = False
    allow_readiness_to_trade: bool = False
    allow_broker_controls: bool = False
    allow_execution: bool = False
    allow_approval: bool = False
    allow_override: bool = False
    allow_suitability_profiling: bool = False
    require_display_contract_only: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience display safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_display_notes(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> RetailTraderExperienceDisplaySafetyPolicy:
        if (
            self.allow_active_ui
            or self.allow_frontend_components
            or self.allow_desktop_components
            or self.allow_recommendations
            or self.allow_action_generation
            or self.allow_confidence_scoring
            or self.allow_decision_object_generation
            or self.allow_readiness_to_trade
            or self.allow_broker_controls
            or self.allow_execution
            or self.allow_approval
            or self.allow_override
            or self.allow_suitability_profiling
        ):
            raise ValueError("Retail Trader Experience Display safety policy dangerous flags must be false")
        if not self.require_display_contract_only:
            raise ValueError("Retail Trader Experience Display safety policy must require display-contract-only")
        return self


class RetailTraderExperienceDisplaySafetyResult(BaseModel):
    result_id: str
    policy_id: str
    safe: bool
    reasons: list[str]
    display_contract_only: bool = True
    active_ui_allowed: bool = False
    recommendations_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    suitability_profiling_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience display safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_non_empty(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_retail_trader_experience_display_notes(value)
        if not sanitized:
            raise ValueError("Retail Trader Experience Display safety result requires reasons")
        return sanitized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def result_must_fail_closed(self) -> RetailTraderExperienceDisplaySafetyResult:
        if not self.display_contract_only:
            raise ValueError("Retail Trader Experience Display safety result must remain display-contract-only")
        if (
            self.active_ui_allowed
            or self.recommendations_allowed
            or self.broker_controls_allowed
            or self.execution_allowed
            or self.suitability_profiling_allowed
        ):
            raise ValueError("Retail Trader Experience Display safety result dangerous flags must be false")
        return self


def default_retail_trader_experience_display_safety_policy(
    settings: Settings | None = None,
) -> RetailTraderExperienceDisplaySafetyPolicy:
    notes = [
        "Prompt 58 permits display contract skeleton metadata only.",
        "No active UI, recommendations, broker controls, suitability profiling, or execution are allowed.",
    ]
    if settings is not None:
        notes.append(f"Settings stage: {settings.retail_trader_experience_display_stage}")
    return RetailTraderExperienceDisplaySafetyPolicy(
        policy_id="retail-trader-experience-display-safety-policy-v1",
        name="Retail Trader Experience Display Contract Safety Policy",
        notes=notes,
    )


def _safe_result(policy: RetailTraderExperienceDisplaySafetyPolicy, result_id: str, reasons: list[str]) -> (
    RetailTraderExperienceDisplaySafetyResult
):
    return RetailTraderExperienceDisplaySafetyResult(
        result_id=result_id,
        policy_id=policy.policy_id,
        safe=True,
        reasons=reasons,
    )


def _blocked_result(policy: RetailTraderExperienceDisplaySafetyPolicy, result_id: str, reasons: list[str]) -> (
    RetailTraderExperienceDisplaySafetyResult
):
    return RetailTraderExperienceDisplaySafetyResult(
        result_id=result_id,
        policy_id=policy.policy_id,
        safe=False,
        reasons=reasons,
    )


def evaluate_retail_trader_experience_display_contract_safety(
    contract: RetailTraderExperienceDisplayContractMetadata,
    policy: RetailTraderExperienceDisplaySafetyPolicy,
) -> RetailTraderExperienceDisplaySafetyResult:
    blockers: list[str] = []
    if not contract.returns_unavailable_by_default:
        blockers.append("Display contract must return unavailable by default.")
    if (
        contract.active_ui_allowed
        or contract.frontend_components_allowed
        or contract.desktop_components_allowed
        or contract.recommendations_allowed
        or contract.action_generation_allowed
        or contract.confidence_scoring_allowed
        or contract.decision_object_generation_allowed
        or contract.readiness_to_trade_allowed
        or contract.broker_controls_allowed
        or contract.execution_allowed
        or contract.approval_allowed
        or contract.override_allowed
        or contract.suitability_profiling_allowed
    ):
        blockers.append("Display contract contains forbidden active UI/recommendation/execution/suitability flags.")
    if blockers:
        return _blocked_result(policy, "retail-trader-experience-display-contract-safety-blocked", blockers)
    return _safe_result(
        policy,
        "retail-trader-experience-display-contract-safety-safe",
        ["Display contract remains display-contract-only and fail-closed."],
    )


def evaluate_retail_trader_experience_display_personas_safety(
    personas: Iterable[RetailTraderExperienceDisplayPersonaPlaceholder],
    policy: RetailTraderExperienceDisplaySafetyPolicy,
) -> RetailTraderExperienceDisplaySafetyResult:
    blockers = [
        f"Persona placeholder {persona.persona_id} violates display safety boundaries."
        for persona in personas
        if (
            not persona.display_contract_only
            or persona.active_ui
            or persona.rendered_now
            or persona.suitability_profile
            or persona.trading_permission_profile
            or persona.recommendations_allowed
            or persona.action_generation_allowed
            or persona.confidence_scoring_allowed
            or persona.decision_object_generation_allowed
            or persona.readiness_to_trade_allowed
            or persona.broker_controls_allowed
            or persona.execution_allowed
        )
    ]
    if blockers:
        return _blocked_result(policy, "retail-trader-experience-display-personas-safety-blocked", blockers)
    return _safe_result(
        policy,
        "retail-trader-experience-display-personas-safety-safe",
        ["Persona visual placeholders remain display-contract-only and not suitability profiling."],
    )


def evaluate_retail_trader_experience_display_journeys_safety(
    journeys: Iterable[RetailTraderExperienceDisplayJourneyPlaceholder],
    policy: RetailTraderExperienceDisplaySafetyPolicy,
) -> RetailTraderExperienceDisplaySafetyResult:
    blockers = [
        f"Journey placeholder {journey.journey_id} violates display safety boundaries."
        for journey in journeys
        if (
            not journey.display_contract_only
            or journey.active_ui
            or journey.rendered_now
            or not journey.unavailable
            or journey.recommendation_journey
            or journey.trading_advice_journey
            or journey.broker_control_journey
            or journey.execution_journey
            or journey.readiness_to_trade_journey
            or journey.approval_journey
            or journey.override_journey
        )
    ]
    if blockers:
        return _blocked_result(policy, "retail-trader-experience-display-journeys-safety-blocked", blockers)
    return _safe_result(
        policy,
        "retail-trader-experience-display-journeys-safety-safe",
        ["Journey visual placeholders remain unavailable and not trading advice."],
    )


def evaluate_retail_trader_experience_display_widgets_safety(
    widgets: Iterable[RetailTraderExperienceDisplayWidgetPlaceholder],
    policy: RetailTraderExperienceDisplaySafetyPolicy,
) -> RetailTraderExperienceDisplaySafetyResult:
    blockers = [
        f"Widget placeholder {widget.widget_id} violates display safety boundaries."
        for widget in widgets
        if (
            not widget.display_contract_only
            or widget.active_ui
            or widget.rendered_now
            or not widget.unavailable
            or widget.recommendation_widget
            or widget.action_widget
            or widget.confidence_widget
            or widget.decision_object_widget
            or widget.readiness_to_trade_widget
            or widget.broker_control_widget
            or widget.execution_widget
            or widget.approval_widget
            or widget.override_widget
            or widget.suitability_profile_widget
        )
    ]
    if blockers:
        return _blocked_result(policy, "retail-trader-experience-display-widgets-safety-blocked", blockers)
    return _safe_result(
        policy,
        "retail-trader-experience-display-widgets-safety-safe",
        ["Widget placeholders remain unavailable and generate no output."],
    )


def reject_display_as_active_ui(
    policy: RetailTraderExperienceDisplaySafetyPolicy | None = None,
) -> RetailTraderExperienceDisplaySafetyResult:
    resolved = policy or default_retail_trader_experience_display_safety_policy()
    return _blocked_result(
        resolved,
        "retail-trader-experience-display-active-ui-rejected",
        ["Retail Trader Experience Display is not active UI in Prompt 58."],
    )


def reject_display_as_recommendation(
    policy: RetailTraderExperienceDisplaySafetyPolicy | None = None,
) -> RetailTraderExperienceDisplaySafetyResult:
    resolved = policy or default_retail_trader_experience_display_safety_policy()
    return _blocked_result(
        resolved,
        "retail-trader-experience-display-recommendation-rejected",
        ["Retail Trader Experience Display cannot be interpreted as a recommendation."],
    )


def reject_display_as_execution_surface(
    policy: RetailTraderExperienceDisplaySafetyPolicy | None = None,
) -> RetailTraderExperienceDisplaySafetyResult:
    resolved = policy or default_retail_trader_experience_display_safety_policy()
    return _blocked_result(
        resolved,
        "retail-trader-experience-display-execution-rejected",
        ["Retail Trader Experience Display cannot expose broker controls or execution APIs."],
    )


def reject_display_as_suitability_profile(
    policy: RetailTraderExperienceDisplaySafetyPolicy | None = None,
) -> RetailTraderExperienceDisplaySafetyResult:
    resolved = policy or default_retail_trader_experience_display_safety_policy()
    return _blocked_result(
        resolved,
        "retail-trader-experience-display-suitability-rejected",
        ["Retail Trader Experience Display cannot create suitability profiling."],
    )
