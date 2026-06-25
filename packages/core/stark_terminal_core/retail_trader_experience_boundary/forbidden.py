from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class RetailTraderExperienceBoundaryStage(StrEnum):
    BOUNDARY_HARDENING = "BOUNDARY_HARDENING"
    AUDIT_ONLY = "AUDIT_ONLY"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceForbiddenBehaviorKind(StrEnum):
    ACTIVE_UI = "ACTIVE_UI"
    FRONTEND_COMPONENT = "FRONTEND_COMPONENT"
    DESKTOP_COMPONENT = "DESKTOP_COMPONENT"
    RECOMMENDATION_CARD = "RECOMMENDATION_CARD"
    ACTION_BUTTON = "ACTION_BUTTON"
    CONFIDENCE_SCORE = "CONFIDENCE_SCORE"
    DECISION_OBJECT_DISPLAY = "DECISION_OBJECT_DISPLAY"
    READINESS_TO_TRADE = "READINESS_TO_TRADE"
    SUITABILITY_PROFILING = "SUITABILITY_PROFILING"
    TRADING_PERMISSION_PROFILE = "TRADING_PERMISSION_PROFILE"
    PERSONA_TO_SUITABILITY_PROFILE = "PERSONA_TO_SUITABILITY_PROFILE"
    JOURNEY_TO_TRADING_ADVICE = "JOURNEY_TO_TRADING_ADVICE"
    BROKER_CONTROL = "BROKER_CONTROL"
    ORDER_BUTTON = "ORDER_BUTTON"
    EXECUTION = "EXECUTION"
    APPROVAL_CONTROL = "APPROVAL_CONTROL"
    OVERRIDE_CONTROL = "OVERRIDE_CONTROL"
    REAL_DATA_DISPLAY = "REAL_DATA_DISPLAY"
    EXTERNAL_CALL = "EXTERNAL_CALL"
    SECRET_OR_CREDENTIAL = "SECRET_OR_CREDENTIAL"
    PROVIDER_SDK = "PROVIDER_SDK"
    SCRAPING = "SCRAPING"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceBoundarySeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceBoundarySafetyLabel(StrEnum):
    BOUNDARY_HARDENING_ONLY = "BOUNDARY_HARDENING_ONLY"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    NO_BROKER_CONTROL = "NO_BROKER_CONTROL"
    NO_EXECUTION = "NO_EXECUTION"
    NOT_SUITABILITY_PROFILING = "NOT_SUITABILITY_PROFILING"
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


def sanitize_retail_trader_experience_boundary_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


REQUIRED_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_BEHAVIORS = {
    RetailTraderExperienceForbiddenBehaviorKind.ACTIVE_UI,
    RetailTraderExperienceForbiddenBehaviorKind.FRONTEND_COMPONENT,
    RetailTraderExperienceForbiddenBehaviorKind.DESKTOP_COMPONENT,
    RetailTraderExperienceForbiddenBehaviorKind.RECOMMENDATION_CARD,
    RetailTraderExperienceForbiddenBehaviorKind.ACTION_BUTTON,
    RetailTraderExperienceForbiddenBehaviorKind.CONFIDENCE_SCORE,
    RetailTraderExperienceForbiddenBehaviorKind.DECISION_OBJECT_DISPLAY,
    RetailTraderExperienceForbiddenBehaviorKind.READINESS_TO_TRADE,
    RetailTraderExperienceForbiddenBehaviorKind.SUITABILITY_PROFILING,
    RetailTraderExperienceForbiddenBehaviorKind.TRADING_PERMISSION_PROFILE,
    RetailTraderExperienceForbiddenBehaviorKind.PERSONA_TO_SUITABILITY_PROFILE,
    RetailTraderExperienceForbiddenBehaviorKind.JOURNEY_TO_TRADING_ADVICE,
    RetailTraderExperienceForbiddenBehaviorKind.BROKER_CONTROL,
    RetailTraderExperienceForbiddenBehaviorKind.ORDER_BUTTON,
    RetailTraderExperienceForbiddenBehaviorKind.EXECUTION,
    RetailTraderExperienceForbiddenBehaviorKind.APPROVAL_CONTROL,
    RetailTraderExperienceForbiddenBehaviorKind.OVERRIDE_CONTROL,
    RetailTraderExperienceForbiddenBehaviorKind.REAL_DATA_DISPLAY,
}


class RetailTraderExperienceForbiddenBehavior(BaseModel):
    behavior_id: str
    kind: RetailTraderExperienceForbiddenBehaviorKind
    name: str
    description: str
    severity: RetailTraderExperienceBoundarySeverity = RetailTraderExperienceBoundarySeverity.BLOCKER
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("behavior_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience forbidden behavior text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_boundary_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def behavior_must_remain_forbidden(self) -> RetailTraderExperienceForbiddenBehavior:
        if self.kind == RetailTraderExperienceForbiddenBehaviorKind.UNKNOWN:
            raise ValueError("UNKNOWN retail trader experience forbidden behavior kind is not allowed")
        if self.severity == RetailTraderExperienceBoundarySeverity.UNKNOWN:
            raise ValueError("UNKNOWN retail trader experience boundary severity is not allowed")
        if not self.forbidden_now:
            raise ValueError("retail trader experience forbidden behavior cannot be unlocked in Prompt 61")
        if not self.requires_future_prompt:
            raise ValueError("retail trader experience forbidden behavior requires a future prompt before unlock")
        if not self.requires_audit_before_unlock:
            raise ValueError("retail trader experience forbidden behavior requires audit before unlock")
        return self


class RetailTraderExperienceForbiddenBehaviorRegistry(BaseModel):
    registry_id: str
    behaviors: list[RetailTraderExperienceForbiddenBehavior]
    complete: bool = True
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    suitability_profiling_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("registry_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience forbidden behavior registry text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def registry_must_cover_required_behaviors(self) -> RetailTraderExperienceForbiddenBehaviorRegistry:
        if not self.behaviors:
            raise ValueError("retail trader experience forbidden behavior registry requires behaviors")
        if not self.complete:
            raise ValueError("retail trader experience forbidden behavior registry must be complete")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "recommendations": self.recommendations_allowed,
            "action generation": self.action_generation_allowed,
            "confidence scoring": self.confidence_scoring_allowed,
            "DecisionObject generation": self.decision_object_generation_allowed,
            "readiness-to-trade": self.readiness_to_trade_allowed,
            "suitability profiling": self.suitability_profiling_allowed,
            "broker controls": self.broker_controls_allowed,
            "execution": self.execution_allowed,
            "approval": self.approval_allowed,
            "override": self.override_allowed,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"retail trader experience boundary cannot allow: {', '.join(enabled)}")
        present = {behavior.kind for behavior in self.behaviors}
        missing = sorted(kind.value for kind in REQUIRED_RETAIL_TRADER_EXPERIENCE_FORBIDDEN_BEHAVIORS - present)
        if missing:
            raise ValueError(
                "retail trader experience forbidden registry missing required kinds: "
                + ", ".join(missing)
            )
        return self


def default_retail_trader_experience_forbidden_behaviors() -> list[RetailTraderExperienceForbiddenBehavior]:
    behavior_specs = [
        (RetailTraderExperienceForbiddenBehaviorKind.ACTIVE_UI, "Active Retail Trader Experience UI"),
        (RetailTraderExperienceForbiddenBehaviorKind.FRONTEND_COMPONENT, "Frontend trader experience component"),
        (RetailTraderExperienceForbiddenBehaviorKind.DESKTOP_COMPONENT, "Desktop trader experience component"),
        (RetailTraderExperienceForbiddenBehaviorKind.RECOMMENDATION_CARD, "Recommendation card"),
        (RetailTraderExperienceForbiddenBehaviorKind.ACTION_BUTTON, "Action button"),
        (RetailTraderExperienceForbiddenBehaviorKind.CONFIDENCE_SCORE, "Confidence score widget"),
        (RetailTraderExperienceForbiddenBehaviorKind.DECISION_OBJECT_DISPLAY, "Active DecisionObject display"),
        (RetailTraderExperienceForbiddenBehaviorKind.READINESS_TO_TRADE, "Readiness-to-trade badge"),
        (RetailTraderExperienceForbiddenBehaviorKind.SUITABILITY_PROFILING, "Suitability profiling"),
        (RetailTraderExperienceForbiddenBehaviorKind.TRADING_PERMISSION_PROFILE, "Trading permission profile"),
        (
            RetailTraderExperienceForbiddenBehaviorKind.PERSONA_TO_SUITABILITY_PROFILE,
            "Persona-to-suitability-profile path",
        ),
        (
            RetailTraderExperienceForbiddenBehaviorKind.JOURNEY_TO_TRADING_ADVICE,
            "Journey-to-trading-advice path",
        ),
        (RetailTraderExperienceForbiddenBehaviorKind.BROKER_CONTROL, "Broker control"),
        (RetailTraderExperienceForbiddenBehaviorKind.ORDER_BUTTON, "Order button"),
        (RetailTraderExperienceForbiddenBehaviorKind.EXECUTION, "Execution behavior"),
        (RetailTraderExperienceForbiddenBehaviorKind.APPROVAL_CONTROL, "Approval control"),
        (RetailTraderExperienceForbiddenBehaviorKind.OVERRIDE_CONTROL, "Override control"),
        (RetailTraderExperienceForbiddenBehaviorKind.REAL_DATA_DISPLAY, "Real or live market data display"),
        (RetailTraderExperienceForbiddenBehaviorKind.EXTERNAL_CALL, "External calls"),
        (RetailTraderExperienceForbiddenBehaviorKind.SECRET_OR_CREDENTIAL, "Secrets or credentials"),
        (RetailTraderExperienceForbiddenBehaviorKind.PROVIDER_SDK, "Provider SDK dependency"),
        (RetailTraderExperienceForbiddenBehaviorKind.SCRAPING, "Scraping behavior"),
    ]
    return [
        RetailTraderExperienceForbiddenBehavior(
            behavior_id=f"retail-trader-experience-{kind.value.lower().replace('_', '-')}-forbidden-v1",
            kind=kind,
            name=name,
            description=f"{name} remains forbidden by the Prompt 61 boundary-hardening layer.",
            notes=[
                "boundary-hardening-only",
                "requires future prompt",
                "requires audit before unlock",
            ],
        )
        for kind, name in behavior_specs
    ]


def default_retail_trader_experience_forbidden_behavior_registry() -> (
    RetailTraderExperienceForbiddenBehaviorRegistry
):
    return RetailTraderExperienceForbiddenBehaviorRegistry(
        registry_id="retail-trader-experience-forbidden-behavior-registry-v1",
        behaviors=default_retail_trader_experience_forbidden_behaviors(),
    )
