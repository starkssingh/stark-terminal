from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes


class RegimePlanningStage(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
    EVIDENCE_REQUIREMENTS = "EVIDENCE_REQUIREMENTS"
    FEATURE_PREPARATION_PLANNED = "FEATURE_PREPARATION_PLANNED"
    CLASSIFIER_PLANNED = "CLASSIFIER_PLANNED"
    VALIDATION_PLANNED = "VALIDATION_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RegimeLabelPlaceholder(StrEnum):
    TRENDING_UP = "TRENDING_UP"
    TRENDING_DOWN = "TRENDING_DOWN"
    RANGE_BOUND = "RANGE_BOUND"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    STRESS = "STRESS"
    RECOVERY = "RECOVERY"
    UNKNOWN = "UNKNOWN"
    UNCLASSIFIED = "UNCLASSIFIED"


class RegimeEvidenceKind(StrEnum):
    RETURNS = "RETURNS"
    VOLATILITY = "VOLATILITY"
    DRAWDOWN = "DRAWDOWN"
    CORRELATION = "CORRELATION"
    BETA = "BETA"
    TIME_SERIES_DIAGNOSTICS = "TIME_SERIES_DIAGNOSTICS"
    VOLUME = "VOLUME"
    LIQUIDITY = "LIQUIDITY"
    OPTIONS_CONTEXT = "OPTIONS_CONTEXT"
    MACRO_CONTEXT = "MACRO_CONTEXT"
    UNKNOWN = "UNKNOWN"


class RegimeSafetyLabel(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    NOT_A_SIGNAL = "NOT_A_SIGNAL"
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


REGIME_FORBIDDEN_OUTPUTS = [
    "trading_signals",
    "recommendations",
    "DecisionObject_generation",
    "execution_apis",
    "market_state_decisions",
    "broker_integration",
]


class RegimeLabelContract(BaseModel):
    label_id: str
    label: RegimeLabelPlaceholder
    display_name: str
    description: str
    planning_only: bool = True
    classification_allowed: bool = False
    trade_signal: bool = False
    recommendation: bool = False
    decision_object_generated: bool = False
    safety_label: RegimeSafetyLabel = RegimeSafetyLabel.PLANNING_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("label_id", "display_name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime label text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def label_must_remain_planning_only(self) -> RegimeLabelContract:
        if not self.planning_only:
            raise ValueError("regime labels must remain planning-only in Prompt 33")
        if self.classification_allowed:
            raise ValueError("regime label assignment is not allowed in Prompt 33")
        if self.trade_signal:
            raise ValueError("regime labels cannot be trade signals")
        if self.recommendation:
            raise ValueError("regime labels cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("regime labels cannot generate DecisionObjects")
        if self.safety_label == RegimeSafetyLabel.UNKNOWN:
            raise ValueError("regime label safety label cannot be UNKNOWN")
        return self


class RegimeAnalyticsPlan(BaseModel):
    plan_id: str
    name: str
    stage: RegimePlanningStage = RegimePlanningStage.PLANNING_ONLY
    planned_labels: list[RegimeLabelContract]
    required_evidence_kinds: list[RegimeEvidenceKind]
    forbidden_outputs: list[str]
    classification_allowed: bool = False
    real_data_allowed: bool = False
    requires_human_review: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("plan_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime plan text fields")

    @field_validator("planned_labels")
    @classmethod
    def planned_labels_must_be_present(cls, value: list[RegimeLabelContract]) -> list[RegimeLabelContract]:
        if not value:
            raise ValueError("regime plans must include planned label placeholders")
        return value

    @field_validator("required_evidence_kinds")
    @classmethod
    def evidence_kinds_must_be_present(cls, value: list[RegimeEvidenceKind]) -> list[RegimeEvidenceKind]:
        if not value:
            raise ValueError("regime plans must include required evidence kinds")
        if RegimeEvidenceKind.UNKNOWN in value:
            raise ValueError("UNKNOWN evidence kind is not allowed")
        return value

    @field_validator("forbidden_outputs")
    @classmethod
    def forbidden_outputs_must_cover_safety_boundary(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_analytics_notes(value)
        normalized = {item.lower() for item in sanitized}
        required = {
            "trading_signals",
            "recommendations",
            "decisionobject_generation",
            "execution_apis",
        }
        if not required.issubset(normalized):
            raise ValueError("regime plans must forbid signals, recommendations, DecisionObject generation, and execution")
        return sanitized

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def plan_must_remain_planning_only(self) -> RegimeAnalyticsPlan:
        if self.stage == RegimePlanningStage.UNKNOWN:
            raise ValueError("regime planning stage cannot be UNKNOWN")
        if self.classification_allowed:
            raise ValueError("regime classification is not allowed in Prompt 33")
        if self.real_data_allowed:
            raise ValueError("regime planning cannot allow real market data in Prompt 33")
        if not self.requires_human_review:
            raise ValueError("regime planning must require human review")
        return self


def create_regime_label_contract(
    label_id: str,
    label: RegimeLabelPlaceholder,
    display_name: str,
    description: str,
) -> RegimeLabelContract:
    return RegimeLabelContract(
        label_id=label_id,
        label=label,
        display_name=display_name,
        description=description,
    )


def default_regime_label_contracts() -> list[RegimeLabelContract]:
    return [
        create_regime_label_contract(
            "planned-trending-up",
            RegimeLabelPlaceholder.TRENDING_UP,
            "Trending Up",
            "Placeholder category for a future validated upward-trend state; not assigned in Prompt 33.",
        ),
        create_regime_label_contract(
            "planned-trending-down",
            RegimeLabelPlaceholder.TRENDING_DOWN,
            "Trending Down",
            "Placeholder category for a future validated downward-trend state; not assigned in Prompt 33.",
        ),
        create_regime_label_contract(
            "planned-range-bound",
            RegimeLabelPlaceholder.RANGE_BOUND,
            "Range Bound",
            "Placeholder category for a future validated range-bound state; not assigned in Prompt 33.",
        ),
        create_regime_label_contract(
            "planned-high-volatility",
            RegimeLabelPlaceholder.HIGH_VOLATILITY,
            "High Volatility",
            "Placeholder category for a future validated high-variability state; not assigned in Prompt 33.",
        ),
        create_regime_label_contract(
            "planned-low-volatility",
            RegimeLabelPlaceholder.LOW_VOLATILITY,
            "Low Volatility",
            "Placeholder category for a future validated low-variability state; not assigned in Prompt 33.",
        ),
        create_regime_label_contract(
            "planned-stress",
            RegimeLabelPlaceholder.STRESS,
            "Stress",
            "Placeholder category for a future validated stress state; not assigned in Prompt 33.",
        ),
        create_regime_label_contract(
            "planned-recovery",
            RegimeLabelPlaceholder.RECOVERY,
            "Recovery",
            "Placeholder category for a future validated recovery state; not assigned in Prompt 33.",
        ),
        create_regime_label_contract(
            "planned-unclassified",
            RegimeLabelPlaceholder.UNCLASSIFIED,
            "Unclassified",
            "Placeholder for unavailable or blocked future state output; not assigned in Prompt 33.",
        ),
    ]


def default_regime_analytics_plan() -> RegimeAnalyticsPlan:
    return RegimeAnalyticsPlan(
        plan_id="regime-analytics-planning-v1",
        name="Regime Analytics Planning and Guardrails",
        planned_labels=default_regime_label_contracts(),
        required_evidence_kinds=[
            RegimeEvidenceKind.RETURNS,
            RegimeEvidenceKind.VOLATILITY,
            RegimeEvidenceKind.DRAWDOWN,
            RegimeEvidenceKind.CORRELATION,
            RegimeEvidenceKind.BETA,
            RegimeEvidenceKind.TIME_SERIES_DIAGNOSTICS,
            RegimeEvidenceKind.VOLUME,
            RegimeEvidenceKind.LIQUIDITY,
            RegimeEvidenceKind.OPTIONS_CONTEXT,
            RegimeEvidenceKind.MACRO_CONTEXT,
        ],
        forbidden_outputs=REGIME_FORBIDDEN_OUTPUTS.copy(),
        notes=[
            "Prompt 33 is planning-only.",
            "No regime label assignment is implemented.",
            "Human review remains required before future feature preparation.",
        ],
    )
