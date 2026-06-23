from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class DecisionBoundaryStage(StrEnum):
    BOUNDARY_HARDENING = "BOUNDARY_HARDENING"
    AUDIT_ONLY = "AUDIT_ONLY"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionForbiddenBehaviorKind(StrEnum):
    RECOMMENDATION = "RECOMMENDATION"
    ACTION_GENERATION = "ACTION_GENERATION"
    CONFIDENCE_SCORING = "CONFIDENCE_SCORING"
    DECISION_OBJECT_GENERATION = "DECISION_OBJECT_GENERATION"
    EXECUTION = "EXECUTION"
    APPROVAL = "APPROVAL"
    OVERRIDE = "OVERRIDE"
    ACTIVE_UI = "ACTIVE_UI"
    ACTIVE_WORKFLOW = "ACTIVE_WORKFLOW"
    TASK_ASSIGNMENT = "TASK_ASSIGNMENT"
    REVIEWER_AUTH = "REVIEWER_AUTH"
    NOTIFICATION = "NOTIFICATION"
    READINESS_TO_TRADE = "READINESS_TO_TRADE"
    BROKER_BEHAVIOR = "BROKER_BEHAVIOR"
    REAL_INGESTION = "REAL_INGESTION"
    EXTERNAL_CALL = "EXTERNAL_CALL"
    SECRET_OR_CREDENTIAL = "SECRET_OR_CREDENTIAL"
    PROVIDER_SDK = "PROVIDER_SDK"
    SCRAPING = "SCRAPING"
    UNKNOWN = "UNKNOWN"


class DecisionBoundarySeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"
    UNKNOWN = "UNKNOWN"


class DecisionBoundarySafetyLabel(StrEnum):
    BOUNDARY_HARDENING_ONLY = "BOUNDARY_HARDENING_ONLY"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_APPROVAL = "NOT_APPROVAL"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
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


def sanitize_decision_boundary_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


class DecisionForbiddenBehavior(BaseModel):
    behavior_id: str
    kind: DecisionForbiddenBehaviorKind
    name: str
    description: str
    severity: DecisionBoundarySeverity = DecisionBoundarySeverity.BLOCKER
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("behavior_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision forbidden behavior text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_boundary_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def behavior_must_be_forbidden(self) -> DecisionForbiddenBehavior:
        if self.kind == DecisionForbiddenBehaviorKind.UNKNOWN:
            raise ValueError("UNKNOWN forbidden behavior kind is not allowed")
        if self.severity == DecisionBoundarySeverity.UNKNOWN:
            raise ValueError("UNKNOWN boundary severity is not allowed")
        if not self.forbidden_now:
            raise ValueError("forbidden behavior registry cannot unlock behavior in Prompt 47")
        if not self.requires_future_prompt:
            raise ValueError("forbidden behavior requires a future prompt before unlock")
        if not self.requires_audit_before_unlock:
            raise ValueError("forbidden behavior requires audit before unlock")
        return self


class DecisionForbiddenBehaviorRegistry(BaseModel):
    registry_id: str
    behaviors: list[DecisionForbiddenBehavior]
    complete: bool = True
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    active_ui_allowed: bool = False
    active_workflow_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("registry_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision forbidden behavior registry text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def registry_must_cover_required_behaviors(self) -> DecisionForbiddenBehaviorRegistry:
        if not self.behaviors:
            raise ValueError("forbidden behavior registry requires behaviors")
        if not self.complete:
            raise ValueError("forbidden behavior registry must be marked complete")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 47")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 47")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 47")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 47")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 47")
        if self.approval_allowed:
            raise ValueError("approval is forbidden in Prompt 47")
        if self.override_allowed:
            raise ValueError("override is forbidden in Prompt 47")
        if self.active_ui_allowed:
            raise ValueError("active UI is forbidden in Prompt 47")
        if self.active_workflow_allowed:
            raise ValueError("active workflow is forbidden in Prompt 47")
        if self.readiness_to_trade_allowed:
            raise ValueError("readiness-to-trade is forbidden in Prompt 47")
        required = {
            DecisionForbiddenBehaviorKind.RECOMMENDATION,
            DecisionForbiddenBehaviorKind.ACTION_GENERATION,
            DecisionForbiddenBehaviorKind.CONFIDENCE_SCORING,
            DecisionForbiddenBehaviorKind.DECISION_OBJECT_GENERATION,
            DecisionForbiddenBehaviorKind.EXECUTION,
            DecisionForbiddenBehaviorKind.APPROVAL,
            DecisionForbiddenBehaviorKind.OVERRIDE,
            DecisionForbiddenBehaviorKind.ACTIVE_UI,
            DecisionForbiddenBehaviorKind.ACTIVE_WORKFLOW,
            DecisionForbiddenBehaviorKind.READINESS_TO_TRADE,
        }
        present = {behavior.kind for behavior in self.behaviors}
        missing = sorted(kind.value for kind in required - present)
        if missing:
            raise ValueError(f"forbidden behavior registry missing required kinds: {', '.join(missing)}")
        return self


def default_decision_forbidden_behaviors() -> list[DecisionForbiddenBehavior]:
    behavior_specs = [
        (DecisionForbiddenBehaviorKind.RECOMMENDATION, "Recommendation generation"),
        (DecisionForbiddenBehaviorKind.ACTION_GENERATION, "Action-state generation"),
        (DecisionForbiddenBehaviorKind.CONFIDENCE_SCORING, "Confidence scoring"),
        (DecisionForbiddenBehaviorKind.DECISION_OBJECT_GENERATION, "Active DecisionObject generation"),
        (DecisionForbiddenBehaviorKind.EXECUTION, "Execution APIs and trade execution"),
        (DecisionForbiddenBehaviorKind.APPROVAL, "Active approvals"),
        (DecisionForbiddenBehaviorKind.OVERRIDE, "Override workflows"),
        (DecisionForbiddenBehaviorKind.ACTIVE_UI, "Active Decision Desk UI"),
        (DecisionForbiddenBehaviorKind.ACTIVE_WORKFLOW, "Active human-review workflow"),
        (DecisionForbiddenBehaviorKind.TASK_ASSIGNMENT, "Review task assignment"),
        (DecisionForbiddenBehaviorKind.REVIEWER_AUTH, "Reviewer authentication"),
        (DecisionForbiddenBehaviorKind.NOTIFICATION, "Review notifications"),
        (DecisionForbiddenBehaviorKind.READINESS_TO_TRADE, "Readiness-to-trade generation"),
        (DecisionForbiddenBehaviorKind.BROKER_BEHAVIOR, "Broker behavior"),
        (DecisionForbiddenBehaviorKind.REAL_INGESTION, "Real market ingestion"),
        (DecisionForbiddenBehaviorKind.EXTERNAL_CALL, "External calls"),
        (DecisionForbiddenBehaviorKind.SECRET_OR_CREDENTIAL, "Secrets or credentials"),
        (DecisionForbiddenBehaviorKind.PROVIDER_SDK, "Provider SDK integration"),
        (DecisionForbiddenBehaviorKind.SCRAPING, "Scraping"),
    ]
    return [
        DecisionForbiddenBehavior(
            behavior_id=f"decision-boundary-{kind.value.lower().replace('_', '-')}",
            kind=kind,
            name=name,
            description=f"{name} is forbidden in Prompt 47 and requires a future prompt plus audit.",
            notes=[
                "Boundary-hardening registry does not enable this behavior.",
                "Any unlock requires explicit future scope and audit-before-unlock.",
            ],
        )
        for kind, name in behavior_specs
    ]


def default_decision_forbidden_behavior_registry() -> DecisionForbiddenBehaviorRegistry:
    return DecisionForbiddenBehaviorRegistry(
        registry_id="decision-forbidden-behavior-registry-v1",
        behaviors=default_decision_forbidden_behaviors(),
    )
