from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_api.requests import (
    RetailDashboardAPIRequestKind,
    RetailDashboardAPIStage,
    RetailDashboardAPIUnavailableReason,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
)


class RetailDashboardAPIContractMetadata(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-retail-dashboard-api"
    stage: RetailDashboardAPIStage = RetailDashboardAPIStage.API_CONTRACT_SKELETON
    request_kinds: list[RetailDashboardAPIRequestKind]
    unavailable_reasons: list[RetailDashboardAPIUnavailableReason]
    active_ui_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    returns_unavailable_by_default: bool = True
    forbidden_outputs: list[str]
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "service_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard API contract metadata text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def contract_metadata_must_fail_closed(self) -> RetailDashboardAPIContractMetadata:
        if self.stage == RetailDashboardAPIStage.UNKNOWN:
            raise ValueError("UNKNOWN Retail Dashboard API stage is not allowed")
        if not self.request_kinds:
            raise ValueError("Retail Dashboard API metadata requires request kinds")
        if RetailDashboardAPIRequestKind.UNKNOWN in self.request_kinds:
            raise ValueError("UNKNOWN Retail Dashboard API request kind is not allowed")
        if not self.unavailable_reasons:
            raise ValueError("Retail Dashboard API metadata requires unavailable reasons")
        if RetailDashboardAPIUnavailableReason.UNKNOWN in self.unavailable_reasons:
            raise ValueError("UNKNOWN Retail Dashboard API unavailable reason is not allowed")
        if self.active_ui_allowed:
            raise ValueError("Retail Dashboard API active UI is forbidden in Prompt 50")
        if self.recommendations_allowed:
            raise ValueError("Retail Dashboard API recommendations are forbidden in Prompt 50")
        if self.action_generation_allowed:
            raise ValueError("Retail Dashboard API action generation is forbidden in Prompt 50")
        if self.confidence_scoring_allowed:
            raise ValueError("Retail Dashboard API confidence scoring is forbidden in Prompt 50")
        if self.decision_object_generation_allowed:
            raise ValueError("Retail Dashboard API DecisionObject generation is forbidden in Prompt 50")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Dashboard API readiness-to-trade is forbidden in Prompt 50")
        if self.broker_controls_allowed:
            raise ValueError("Retail Dashboard API broker controls are forbidden in Prompt 50")
        if self.execution_allowed:
            raise ValueError("Retail Dashboard API execution is forbidden in Prompt 50")
        if self.approval_allowed:
            raise ValueError("Retail Dashboard API approval is forbidden in Prompt 50")
        if self.override_allowed:
            raise ValueError("Retail Dashboard API override is forbidden in Prompt 50")
        if not self.returns_unavailable_by_default:
            raise ValueError("Retail Dashboard API skeleton must return unavailable by default")
        required_terms = [
            "active ui",
            "recommendation",
            "action",
            "confidence",
            "decisionobject",
            "readiness-to-trade",
            "broker",
            "execution",
            "approval",
            "override",
        ]
        normalized_outputs = " ".join(self.forbidden_outputs).lower().replace("_", " ")
        missing = [term for term in required_terms if term not in normalized_outputs]
        if missing:
            raise ValueError(f"forbidden outputs missing required concepts: {', '.join(missing)}")
        return self


def default_retail_dashboard_api_contract_metadata() -> RetailDashboardAPIContractMetadata:
    return RetailDashboardAPIContractMetadata(
        contract_id="retail-dashboard-api-contract-metadata-v1",
        request_kinds=[
            RetailDashboardAPIRequestKind.DASHBOARD_OVERVIEW_REQUEST,
            RetailDashboardAPIRequestKind.DASHBOARD_LAYOUT_REQUEST,
            RetailDashboardAPIRequestKind.DASHBOARD_SECTION_REQUEST,
            RetailDashboardAPIRequestKind.DASHBOARD_CARD_REQUEST,
            RetailDashboardAPIRequestKind.DASHBOARD_REFERENCE_REQUEST,
            RetailDashboardAPIRequestKind.DASHBOARD_READINESS_REQUEST,
        ],
        unavailable_reasons=[
            RetailDashboardAPIUnavailableReason.ACTIVE_UI_DISABLED,
            RetailDashboardAPIUnavailableReason.RECOMMENDATIONS_DISABLED,
            RetailDashboardAPIUnavailableReason.ACTION_GENERATION_DISABLED,
            RetailDashboardAPIUnavailableReason.CONFIDENCE_SCORING_DISABLED,
            RetailDashboardAPIUnavailableReason.DECISION_OBJECT_GENERATION_DISABLED,
            RetailDashboardAPIUnavailableReason.READINESS_TO_TRADE_DISABLED,
            RetailDashboardAPIUnavailableReason.BROKER_CONTROLS_DISABLED,
            RetailDashboardAPIUnavailableReason.EXECUTION_DISABLED,
            RetailDashboardAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
        ],
        forbidden_outputs=[
            "active UI",
            "recommendation_cards",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation_or_display",
            "readiness-to-trade",
            "broker_controls",
            "execution_apis",
            "approval_controls",
            "override_controls",
        ],
    )
