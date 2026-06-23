from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_api.requests import (
    DecisionAPIRequestKind,
    DecisionAPIStage,
    DecisionAPIUnavailableReason,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
)


class DecisionDeskAPIContractMetadata(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-decision-desk-api"
    stage: DecisionAPIStage = DecisionAPIStage.CONTRACT_SKELETON
    request_kinds: list[DecisionAPIRequestKind]
    unavailable_reasons: list[DecisionAPIUnavailableReason]
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
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
        return _non_empty_text(value, "decision desk API contract metadata text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def contract_metadata_must_fail_closed(self) -> DecisionDeskAPIContractMetadata:
        if self.stage == DecisionAPIStage.UNKNOWN:
            raise ValueError("UNKNOWN Decision Desk API stage is not allowed")
        if not self.request_kinds:
            raise ValueError("decision API contract metadata requires request kinds")
        if DecisionAPIRequestKind.UNKNOWN in self.request_kinds:
            raise ValueError("UNKNOWN request kind is not allowed")
        if not self.unavailable_reasons:
            raise ValueError("decision API contract metadata requires unavailable reasons")
        if DecisionAPIUnavailableReason.UNKNOWN in self.unavailable_reasons:
            raise ValueError("UNKNOWN unavailable reason is not allowed")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 40")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 40")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 40")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 40")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 40")
        if self.approval_allowed:
            raise ValueError("approval is forbidden in Prompt 40")
        if self.override_allowed:
            raise ValueError("override is forbidden in Prompt 40")
        if not self.returns_unavailable_by_default:
            raise ValueError("Decision Desk API skeleton must return unavailable by default")
        required_terms = [
            "recommendation",
            "action",
            "confidence",
            "decisionobject",
            "approval",
            "override",
            "execution",
        ]
        normalized_outputs = " ".join(self.forbidden_outputs).lower()
        missing = [term for term in required_terms if term not in normalized_outputs]
        if missing:
            raise ValueError(f"forbidden outputs missing required concepts: {', '.join(missing)}")
        return self


def default_decision_desk_api_contract_metadata() -> DecisionDeskAPIContractMetadata:
    return DecisionDeskAPIContractMetadata(
        contract_id="decision-desk-api-contract-metadata-v1",
        request_kinds=[
            DecisionAPIRequestKind.SNAPSHOT_REQUEST,
            DecisionAPIRequestKind.INSTRUMENT_CONTEXT_REQUEST,
            DecisionAPIRequestKind.EVIDENCE_REFERENCE_REQUEST,
            DecisionAPIRequestKind.READINESS_REQUEST,
        ],
        unavailable_reasons=[
            DecisionAPIUnavailableReason.RECOMMENDATIONS_DISABLED,
            DecisionAPIUnavailableReason.ACTION_GENERATION_DISABLED,
            DecisionAPIUnavailableReason.CONFIDENCE_SCORING_DISABLED,
            DecisionAPIUnavailableReason.DECISION_OBJECT_GENERATION_DISABLED,
            DecisionAPIUnavailableReason.EXECUTION_DISABLED,
            DecisionAPIUnavailableReason.HUMAN_REVIEW_REQUIRED,
            DecisionAPIUnavailableReason.EVIDENCE_BUNDLE_REQUIRED,
            DecisionAPIUnavailableReason.CONTRACT_SKELETON_ONLY,
        ],
        forbidden_outputs=[
            "recommendation_generation",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "approval_workflow",
            "override_workflow",
            "execution_apis",
            "broker_orders",
            "market_state_decisions",
        ],
    )

