from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class DecisionDisplayStage(StrEnum):
    DISPLAY_CONTRACT_SKELETON = "DISPLAY_CONTRACT_SKELETON"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    CARD_PLACEHOLDERS = "CARD_PLACEHOLDERS"
    SECTION_PLACEHOLDERS = "SECTION_PLACEHOLDERS"
    FRONTEND_UI_PLANNED = "FRONTEND_UI_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionDisplaySectionKind(StrEnum):
    HEADER = "HEADER"
    EVIDENCE_SUMMARY = "EVIDENCE_SUMMARY"
    RISK_SUMMARY = "RISK_SUMMARY"
    DATA_QUALITY = "DATA_QUALITY"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    SAFETY_STATUS = "SAFETY_STATUS"
    UNAVAILABLE_NOTICE = "UNAVAILABLE_NOTICE"
    UNKNOWN = "UNKNOWN"


class DecisionDisplayCardKind(StrEnum):
    PLACEHOLDER = "PLACEHOLDER"
    EVIDENCE_PLACEHOLDER = "EVIDENCE_PLACEHOLDER"
    RISK_PLACEHOLDER = "RISK_PLACEHOLDER"
    SAFETY_PLACEHOLDER = "SAFETY_PLACEHOLDER"
    HUMAN_REVIEW_PLACEHOLDER = "HUMAN_REVIEW_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class DecisionDisplayBadgeKind(StrEnum):
    UNAVAILABLE = "UNAVAILABLE"
    PLANNING_ONLY = "PLANNING_ONLY"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    SAFETY_GATED = "SAFETY_GATED"
    UNKNOWN = "UNKNOWN"


class DecisionDisplaySafetyLabel(StrEnum):
    DISPLAY_CONTRACT_SKELETON_ONLY = "DISPLAY_CONTRACT_SKELETON_ONLY"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_APPROVAL = "NOT_APPROVAL"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def sanitize_decision_display_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


class DecisionDisplayContractMetadata(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-decision-display"
    stage: DecisionDisplayStage = DecisionDisplayStage.DISPLAY_CONTRACT_SKELETON
    supported_section_kinds: list[DecisionDisplaySectionKind]
    supported_card_kinds: list[DecisionDisplayCardKind]
    supported_badge_kinds: list[DecisionDisplayBadgeKind]
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    returns_unavailable_by_default: bool = True
    forbidden_outputs: list[str]
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "service_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision display contract metadata text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def contract_metadata_must_fail_closed(self) -> DecisionDisplayContractMetadata:
        if self.stage == DecisionDisplayStage.UNKNOWN:
            raise ValueError("UNKNOWN Decision Display stage is not allowed")
        if not self.supported_section_kinds:
            raise ValueError("decision display contract metadata requires section kinds")
        if DecisionDisplaySectionKind.UNKNOWN in self.supported_section_kinds:
            raise ValueError("UNKNOWN section kind is not allowed")
        if not self.supported_card_kinds:
            raise ValueError("decision display contract metadata requires card kinds")
        if DecisionDisplayCardKind.UNKNOWN in self.supported_card_kinds:
            raise ValueError("UNKNOWN card kind is not allowed")
        if not self.supported_badge_kinds:
            raise ValueError("decision display contract metadata requires badge kinds")
        if DecisionDisplayBadgeKind.UNKNOWN in self.supported_badge_kinds:
            raise ValueError("UNKNOWN badge kind is not allowed")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 43")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 43")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 43")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 43")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 43")
        if self.approval_allowed:
            raise ValueError("approval is forbidden in Prompt 43")
        if self.override_allowed:
            raise ValueError("override is forbidden in Prompt 43")
        if self.readiness_to_trade_allowed:
            raise ValueError("readiness-to-trade is forbidden in Prompt 43")
        if not self.returns_unavailable_by_default:
            raise ValueError("Decision display skeleton must return unavailable by default")
        required_terms = [
            "recommendation",
            "action",
            "confidence",
            "decisionobject",
            "approval",
            "override",
            "readiness-to-trade",
            "execution",
        ]
        normalized_outputs = " ".join(self.forbidden_outputs).lower()
        missing = [term for term in required_terms if term not in normalized_outputs]
        if missing:
            raise ValueError(f"forbidden outputs missing required concepts: {', '.join(missing)}")
        return self


def default_decision_display_contract_metadata() -> DecisionDisplayContractMetadata:
    return DecisionDisplayContractMetadata(
        contract_id="decision-display-contract-metadata-v1",
        supported_section_kinds=[
            DecisionDisplaySectionKind.HEADER,
            DecisionDisplaySectionKind.EVIDENCE_SUMMARY,
            DecisionDisplaySectionKind.RISK_SUMMARY,
            DecisionDisplaySectionKind.DATA_QUALITY,
            DecisionDisplaySectionKind.HUMAN_REVIEW,
            DecisionDisplaySectionKind.SAFETY_STATUS,
            DecisionDisplaySectionKind.UNAVAILABLE_NOTICE,
        ],
        supported_card_kinds=[
            DecisionDisplayCardKind.PLACEHOLDER,
            DecisionDisplayCardKind.EVIDENCE_PLACEHOLDER,
            DecisionDisplayCardKind.RISK_PLACEHOLDER,
            DecisionDisplayCardKind.SAFETY_PLACEHOLDER,
            DecisionDisplayCardKind.HUMAN_REVIEW_PLACEHOLDER,
            DecisionDisplayCardKind.UNAVAILABLE,
        ],
        supported_badge_kinds=[
            DecisionDisplayBadgeKind.UNAVAILABLE,
            DecisionDisplayBadgeKind.PLANNING_ONLY,
            DecisionDisplayBadgeKind.NOT_A_RECOMMENDATION,
            DecisionDisplayBadgeKind.HUMAN_REVIEW_REQUIRED,
            DecisionDisplayBadgeKind.SAFETY_GATED,
        ],
        forbidden_outputs=[
            "recommendation_generation",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "approval_workflow",
            "override_workflow",
            "readiness-to-trade",
            "execution_apis",
            "broker_controls",
            "active_frontend_ui",
        ],
    )

