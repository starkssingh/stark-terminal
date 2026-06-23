from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class RetailDashboardBoundaryStage(StrEnum):
    BOUNDARY_HARDENING = "BOUNDARY_HARDENING"
    AUDIT_ONLY = "AUDIT_ONLY"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RetailDashboardForbiddenBehaviorKind(StrEnum):
    ACTIVE_UI = "ACTIVE_UI"
    FRONTEND_COMPONENT = "FRONTEND_COMPONENT"
    DESKTOP_COMPONENT = "DESKTOP_COMPONENT"
    RECOMMENDATION_CARD = "RECOMMENDATION_CARD"
    ACTION_BUTTON = "ACTION_BUTTON"
    CONFIDENCE_SCORE = "CONFIDENCE_SCORE"
    DECISION_OBJECT_DISPLAY = "DECISION_OBJECT_DISPLAY"
    READINESS_TO_TRADE = "READINESS_TO_TRADE"
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


class RetailDashboardBoundarySeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"
    UNKNOWN = "UNKNOWN"


class RetailDashboardBoundarySafetyLabel(StrEnum):
    BOUNDARY_HARDENING_ONLY = "BOUNDARY_HARDENING_ONLY"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    NO_BROKER_CONTROL = "NO_BROKER_CONTROL"
    NO_EXECUTION = "NO_EXECUTION"
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


def sanitize_retail_dashboard_boundary_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


REQUIRED_RETAIL_DASHBOARD_FORBIDDEN_BEHAVIORS = {
    RetailDashboardForbiddenBehaviorKind.ACTIVE_UI,
    RetailDashboardForbiddenBehaviorKind.FRONTEND_COMPONENT,
    RetailDashboardForbiddenBehaviorKind.DESKTOP_COMPONENT,
    RetailDashboardForbiddenBehaviorKind.RECOMMENDATION_CARD,
    RetailDashboardForbiddenBehaviorKind.ACTION_BUTTON,
    RetailDashboardForbiddenBehaviorKind.CONFIDENCE_SCORE,
    RetailDashboardForbiddenBehaviorKind.DECISION_OBJECT_DISPLAY,
    RetailDashboardForbiddenBehaviorKind.READINESS_TO_TRADE,
    RetailDashboardForbiddenBehaviorKind.BROKER_CONTROL,
    RetailDashboardForbiddenBehaviorKind.ORDER_BUTTON,
    RetailDashboardForbiddenBehaviorKind.EXECUTION,
    RetailDashboardForbiddenBehaviorKind.APPROVAL_CONTROL,
    RetailDashboardForbiddenBehaviorKind.OVERRIDE_CONTROL,
    RetailDashboardForbiddenBehaviorKind.REAL_DATA_DISPLAY,
}


class RetailDashboardForbiddenBehavior(BaseModel):
    behavior_id: str
    kind: RetailDashboardForbiddenBehaviorKind
    name: str
    description: str
    severity: RetailDashboardBoundarySeverity = RetailDashboardBoundarySeverity.BLOCKER
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("behavior_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard forbidden behavior text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_boundary_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def behavior_must_remain_forbidden(self) -> RetailDashboardForbiddenBehavior:
        if self.kind == RetailDashboardForbiddenBehaviorKind.UNKNOWN:
            raise ValueError("UNKNOWN retail dashboard forbidden behavior kind is not allowed")
        if self.severity == RetailDashboardBoundarySeverity.UNKNOWN:
            raise ValueError("UNKNOWN retail dashboard boundary severity is not allowed")
        if not self.forbidden_now:
            raise ValueError("retail dashboard forbidden behavior cannot be unlocked in Prompt 54")
        if not self.requires_future_prompt:
            raise ValueError("retail dashboard forbidden behavior requires a future prompt before unlock")
        if not self.requires_audit_before_unlock:
            raise ValueError("retail dashboard forbidden behavior requires audit before unlock")
        return self


class RetailDashboardForbiddenBehaviorRegistry(BaseModel):
    registry_id: str
    behaviors: list[RetailDashboardForbiddenBehavior]
    complete: bool = True
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
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("registry_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard forbidden behavior registry text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def registry_must_cover_required_behaviors(self) -> RetailDashboardForbiddenBehaviorRegistry:
        if not self.behaviors:
            raise ValueError("retail dashboard forbidden behavior registry requires behaviors")
        if not self.complete:
            raise ValueError("retail dashboard forbidden behavior registry must be complete")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "recommendations": self.recommendations_allowed,
            "action generation": self.action_generation_allowed,
            "confidence scoring": self.confidence_scoring_allowed,
            "DecisionObject generation": self.decision_object_generation_allowed,
            "readiness-to-trade": self.readiness_to_trade_allowed,
            "broker controls": self.broker_controls_allowed,
            "execution": self.execution_allowed,
            "approval": self.approval_allowed,
            "override": self.override_allowed,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"retail dashboard boundary cannot allow: {', '.join(enabled)}")
        present = {behavior.kind for behavior in self.behaviors}
        missing = sorted(kind.value for kind in REQUIRED_RETAIL_DASHBOARD_FORBIDDEN_BEHAVIORS - present)
        if missing:
            raise ValueError(f"retail dashboard forbidden registry missing required kinds: {', '.join(missing)}")
        return self


def default_retail_dashboard_forbidden_behaviors() -> list[RetailDashboardForbiddenBehavior]:
    behavior_specs = [
        (RetailDashboardForbiddenBehaviorKind.ACTIVE_UI, "Active Retail Dashboard UI"),
        (RetailDashboardForbiddenBehaviorKind.FRONTEND_COMPONENT, "Frontend dashboard component"),
        (RetailDashboardForbiddenBehaviorKind.DESKTOP_COMPONENT, "Desktop dashboard component"),
        (RetailDashboardForbiddenBehaviorKind.RECOMMENDATION_CARD, "Recommendation card"),
        (RetailDashboardForbiddenBehaviorKind.ACTION_BUTTON, "Action button"),
        (RetailDashboardForbiddenBehaviorKind.CONFIDENCE_SCORE, "Confidence score widget"),
        (RetailDashboardForbiddenBehaviorKind.DECISION_OBJECT_DISPLAY, "Active DecisionObject display"),
        (RetailDashboardForbiddenBehaviorKind.READINESS_TO_TRADE, "Readiness-to-trade badge"),
        (RetailDashboardForbiddenBehaviorKind.BROKER_CONTROL, "Broker control"),
        (RetailDashboardForbiddenBehaviorKind.ORDER_BUTTON, "Order button"),
        (RetailDashboardForbiddenBehaviorKind.EXECUTION, "Execution behavior"),
        (RetailDashboardForbiddenBehaviorKind.APPROVAL_CONTROL, "Approval control"),
        (RetailDashboardForbiddenBehaviorKind.OVERRIDE_CONTROL, "Override control"),
        (RetailDashboardForbiddenBehaviorKind.REAL_DATA_DISPLAY, "Real or live market data display"),
        (RetailDashboardForbiddenBehaviorKind.EXTERNAL_CALL, "External calls"),
        (RetailDashboardForbiddenBehaviorKind.SECRET_OR_CREDENTIAL, "Secrets or credentials"),
        (RetailDashboardForbiddenBehaviorKind.PROVIDER_SDK, "Provider SDK integration"),
        (RetailDashboardForbiddenBehaviorKind.SCRAPING, "Scraping"),
    ]
    return [
        RetailDashboardForbiddenBehavior(
            behavior_id=f"retail-dashboard-boundary-{kind.value.lower().replace('_', '-')}",
            kind=kind,
            name=name,
            description=f"{name} is forbidden in Prompt 54 and requires a future prompt plus audit.",
            notes=[
                "Boundary-hardening registry is contract metadata only and enables no dashboard capability.",
                "Any unlock requires explicit future scope and audit-before-unlock.",
            ],
        )
        for kind, name in behavior_specs
    ]


def default_retail_dashboard_forbidden_behavior_registry() -> RetailDashboardForbiddenBehaviorRegistry:
    return RetailDashboardForbiddenBehaviorRegistry(
        registry_id="retail-dashboard-forbidden-behavior-registry-v1",
        behaviors=default_retail_dashboard_forbidden_behaviors(),
    )
