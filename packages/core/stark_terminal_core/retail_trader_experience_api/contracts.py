from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_api.requests import (
    RetailTraderExperienceAPIRequestKind,
    RetailTraderExperienceAPIStage,
    RetailTraderExperienceAPIUnavailableReason,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
)


class RetailTraderExperienceAPIContractMetadata(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-retail-trader-experience-api"
    stage: RetailTraderExperienceAPIStage = RetailTraderExperienceAPIStage.API_CONTRACT_SKELETON
    request_kinds: list[RetailTraderExperienceAPIRequestKind]
    unavailable_reasons: list[RetailTraderExperienceAPIUnavailableReason]
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
    approval_allowed: bool = False
    override_allowed: bool = False
    suitability_profiling_allowed: bool = False
    returns_unavailable_by_default: bool = True
    forbidden_outputs: list[str]
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "service_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience API contract metadata text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def contract_metadata_must_fail_closed(self) -> RetailTraderExperienceAPIContractMetadata:
        if self.stage == RetailTraderExperienceAPIStage.UNKNOWN:
            raise ValueError("UNKNOWN Retail Trader Experience API stage is not allowed")
        if not self.request_kinds:
            raise ValueError("Retail Trader Experience API metadata requires request kinds")
        if RetailTraderExperienceAPIRequestKind.UNKNOWN in self.request_kinds:
            raise ValueError("UNKNOWN Retail Trader Experience API request kind is not allowed")
        if not self.unavailable_reasons:
            raise ValueError("Retail Trader Experience API metadata requires unavailable reasons")
        if RetailTraderExperienceAPIUnavailableReason.UNKNOWN in self.unavailable_reasons:
            raise ValueError("UNKNOWN Retail Trader Experience API unavailable reason is not allowed")
        if self.active_ui_allowed:
            raise ValueError("Retail Trader Experience API active UI is forbidden in Prompt 57")
        if self.frontend_components_allowed:
            raise ValueError("Retail Trader Experience API frontend components are forbidden in Prompt 57")
        if self.desktop_components_allowed:
            raise ValueError("Retail Trader Experience API desktop components are forbidden in Prompt 57")
        if self.recommendations_allowed:
            raise ValueError("Retail Trader Experience API recommendations are forbidden in Prompt 57")
        if self.action_generation_allowed:
            raise ValueError("Retail Trader Experience API action generation is forbidden in Prompt 57")
        if self.confidence_scoring_allowed:
            raise ValueError("Retail Trader Experience API confidence scoring is forbidden in Prompt 57")
        if self.decision_object_generation_allowed:
            raise ValueError("Retail Trader Experience API DecisionObject generation is forbidden in Prompt 57")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Trader Experience API readiness-to-trade is forbidden in Prompt 57")
        if self.broker_controls_allowed:
            raise ValueError("Retail Trader Experience API broker controls are forbidden in Prompt 57")
        if self.execution_allowed:
            raise ValueError("Retail Trader Experience API execution is forbidden in Prompt 57")
        if self.approval_allowed:
            raise ValueError("Retail Trader Experience API approval is forbidden in Prompt 57")
        if self.override_allowed:
            raise ValueError("Retail Trader Experience API override is forbidden in Prompt 57")
        if self.suitability_profiling_allowed:
            raise ValueError("Retail Trader Experience API suitability profiling is forbidden in Prompt 57")
        if not self.returns_unavailable_by_default:
            raise ValueError("Retail Trader Experience API skeleton must return unavailable by default")
        required_terms = [
            "active ui",
            "frontend",
            "desktop",
            "recommendation",
            "action",
            "confidence",
            "decisionobject",
            "readiness-to-trade",
            "broker",
            "execution",
            "approval",
            "override",
            "suitability",
        ]
        normalized_outputs = " ".join(self.forbidden_outputs).lower().replace("_", " ")
        missing = [term for term in required_terms if term not in normalized_outputs]
        if missing:
            raise ValueError(f"forbidden outputs missing required concepts: {', '.join(missing)}")
        return self


def default_retail_trader_experience_api_contract_metadata() -> RetailTraderExperienceAPIContractMetadata:
    return RetailTraderExperienceAPIContractMetadata(
        contract_id="retail-trader-experience-api-contract-metadata-v1",
        request_kinds=[
            RetailTraderExperienceAPIRequestKind.EXPERIENCE_OVERVIEW_REQUEST,
            RetailTraderExperienceAPIRequestKind.PERSONA_CONTEXT_REQUEST,
            RetailTraderExperienceAPIRequestKind.JOURNEY_CONTEXT_REQUEST,
            RetailTraderExperienceAPIRequestKind.SECTION_CONTEXT_REQUEST,
            RetailTraderExperienceAPIRequestKind.CARD_CONTEXT_REQUEST,
            RetailTraderExperienceAPIRequestKind.REFERENCE_CONTEXT_REQUEST,
            RetailTraderExperienceAPIRequestKind.READINESS_TEMPLATE_REQUEST,
        ],
        unavailable_reasons=[
            RetailTraderExperienceAPIUnavailableReason.ACTIVE_UI_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.FRONTEND_COMPONENTS_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.DESKTOP_COMPONENTS_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.RECOMMENDATIONS_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.ACTION_GENERATION_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.CONFIDENCE_SCORING_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.DECISION_OBJECT_GENERATION_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.READINESS_TO_TRADE_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.BROKER_CONTROLS_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.EXECUTION_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.SUITABILITY_PROFILING_DISABLED,
            RetailTraderExperienceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
        ],
        forbidden_outputs=[
            "active UI",
            "frontend_components",
            "desktop_components",
            "recommendation_cards",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation_or_display",
            "readiness-to-trade",
            "broker_controls",
            "execution_apis",
            "approval_controls",
            "override_controls",
            "suitability_profiling",
        ],
    )
