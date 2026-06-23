from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_readiness_api.requests import (
    DecisionReadinessAPIStage,
    DecisionReadinessRequestKind,
    DecisionReadinessUnavailableReason,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
)


class DecisionReadinessAPIContractMetadata(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-decision-readiness-api"
    stage: DecisionReadinessAPIStage = DecisionReadinessAPIStage.READINESS_CONTRACT_SKELETON
    request_kinds: list[DecisionReadinessRequestKind]
    unavailable_reasons: list[DecisionReadinessUnavailableReason]
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    returns_unavailable_by_default: bool = True
    readiness_status_generation_allowed: bool = False
    forbidden_outputs: list[str]
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "service_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision readiness API contract metadata text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def contract_metadata_must_fail_closed(self) -> DecisionReadinessAPIContractMetadata:
        if self.stage == DecisionReadinessAPIStage.UNKNOWN:
            raise ValueError("UNKNOWN Decision Readiness API stage is not allowed")
        if not self.request_kinds:
            raise ValueError("decision readiness API contract metadata requires request kinds")
        if DecisionReadinessRequestKind.UNKNOWN in self.request_kinds:
            raise ValueError("UNKNOWN readiness request kind is not allowed")
        if not self.unavailable_reasons:
            raise ValueError("decision readiness API contract metadata requires unavailable reasons")
        if DecisionReadinessUnavailableReason.UNKNOWN in self.unavailable_reasons:
            raise ValueError("UNKNOWN unavailable reason is not allowed")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 42")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 42")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 42")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 42")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 42")
        if self.approval_allowed:
            raise ValueError("approval is forbidden in Prompt 42")
        if self.override_allowed:
            raise ValueError("override is forbidden in Prompt 42")
        if not self.returns_unavailable_by_default:
            raise ValueError("Decision readiness API skeleton must return unavailable by default")
        if self.readiness_status_generation_allowed:
            raise ValueError("readiness status generation is forbidden in Prompt 42")
        required_terms = [
            "readiness-as-recommendation",
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


def default_decision_readiness_api_contract_metadata() -> DecisionReadinessAPIContractMetadata:
    return DecisionReadinessAPIContractMetadata(
        contract_id="decision-readiness-api-contract-metadata-v1",
        request_kinds=[
            DecisionReadinessRequestKind.READINESS_STATUS_REQUEST,
            DecisionReadinessRequestKind.EVIDENCE_READINESS_REQUEST,
            DecisionReadinessRequestKind.SAFETY_READINESS_REQUEST,
            DecisionReadinessRequestKind.HUMAN_REVIEW_READINESS_REQUEST,
            DecisionReadinessRequestKind.BLOCKED_OUTPUT_READINESS_REQUEST,
        ],
        unavailable_reasons=[
            DecisionReadinessUnavailableReason.RECOMMENDATIONS_DISABLED,
            DecisionReadinessUnavailableReason.ACTION_GENERATION_DISABLED,
            DecisionReadinessUnavailableReason.CONFIDENCE_SCORING_DISABLED,
            DecisionReadinessUnavailableReason.DECISION_OBJECT_GENERATION_DISABLED,
            DecisionReadinessUnavailableReason.EXECUTION_DISABLED,
            DecisionReadinessUnavailableReason.APPROVAL_DISABLED,
            DecisionReadinessUnavailableReason.OVERRIDE_DISABLED,
            DecisionReadinessUnavailableReason.HUMAN_REVIEW_REQUIRED,
            DecisionReadinessUnavailableReason.EVIDENCE_BUNDLE_REQUIRED,
            DecisionReadinessUnavailableReason.SAFETY_GUARDRAILS_REQUIRED,
            DecisionReadinessUnavailableReason.CONTRACT_SKELETON_ONLY,
        ],
        forbidden_outputs=[
            "readiness-as-recommendation",
            "recommendation_generation",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "approval_workflow",
            "override_workflow",
            "execution_apis",
            "readiness_to_trade",
            "broker_orders",
            "market_state_decisions",
        ],
    )
