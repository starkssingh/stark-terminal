from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


SENSITIVE_ANALYTICS_NOTE_TERMS = (
    "password",
    "secret",
    "token",
    "api_key",
    "apikey",
    "credential",
    "broker",
    "order placement",
    "live trading",
)


class AnalyticsStage(StrEnum):
    CONTRACTS_ONLY = "CONTRACTS_ONLY"
    NUMERICAL_CORE_PLANNED = "NUMERICAL_CORE_PLANNED"
    RETURNS_ANALYTICS_PLANNED = "RETURNS_ANALYTICS_PLANNED"
    VOLATILITY_ANALYTICS_PLANNED = "VOLATILITY_ANALYTICS_PLANNED"
    DRAWDOWN_ANALYTICS_PLANNED = "DRAWDOWN_ANALYTICS_PLANNED"
    CORRELATION_ANALYTICS_PLANNED = "CORRELATION_ANALYTICS_PLANNED"
    REGIME_ANALYTICS_PLANNED = "REGIME_ANALYTICS_PLANNED"
    BACKTESTING_PLANNED = "BACKTESTING_PLANNED"
    UNKNOWN = "UNKNOWN"


class AnalyticsOutputKind(StrEnum):
    DESCRIPTIVE_STATISTIC = "DESCRIPTIVE_STATISTIC"
    TIME_SERIES_METRIC = "TIME_SERIES_METRIC"
    RISK_METRIC = "RISK_METRIC"
    DIAGNOSTIC = "DIAGNOSTIC"
    RESEARCH_ARTIFACT = "RESEARCH_ARTIFACT"
    UNKNOWN = "UNKNOWN"


class AnalyticsSafetyLevel(StrEnum):
    SAFE_DESCRIPTIVE = "SAFE_DESCRIPTIVE"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    REQUIRES_VALIDATION = "REQUIRES_VALIDATION"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def sanitize_analytics_notes(notes: list[str]) -> list[str]:
    sanitized: list[str] = []
    for note in notes:
        normalized = note.strip()
        if not normalized:
            continue
        lowered = normalized.lower().replace("-", "_")
        if any(term in lowered for term in SENSITIVE_ANALYTICS_NOTE_TERMS):
            sanitized.append("[redacted]")
        else:
            sanitized.append(normalized[:240])
    return sanitized


class AnalyticsInputContract(BaseModel):
    contract_id: str
    name: str
    accepted_data_kinds: list[str]
    requires_validated_input: bool = True
    requires_source_reference: bool = True
    synthetic_allowed: bool = True
    real_data_allowed: bool = False
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "analytics input contract text fields")

    @field_validator("accepted_data_kinds")
    @classmethod
    def accepted_data_kinds_must_be_present(cls, value: list[str]) -> list[str]:
        normalized = [_non_empty_text(kind, "accepted_data_kinds") for kind in value]
        if not normalized:
            raise ValueError("accepted_data_kinds cannot be empty")
        return normalized

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def current_phase_cannot_allow_real_data(self) -> AnalyticsInputContract:
        if self.real_data_allowed:
            raise ValueError("analytics input contracts cannot allow real data in Prompt 26")
        if not self.requires_validated_input:
            raise ValueError("analytics input contracts must require validated inputs")
        if not self.requires_source_reference:
            raise ValueError("analytics input contracts must require source references")
        return self


class AnalyticsOutputContract(BaseModel):
    contract_id: str
    name: str
    output_kind: AnalyticsOutputKind
    safety_level: AnalyticsSafetyLevel
    descriptive_only: bool = True
    trade_signal: bool = False
    recommendation: bool = False
    execution_ready: bool = False
    requires_interpretation: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "analytics output contract text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def output_must_not_be_trade_actionable(self) -> AnalyticsOutputContract:
        if self.trade_signal:
            raise ValueError("analytics output contracts cannot be trade signals in Prompt 26")
        if self.recommendation:
            raise ValueError("analytics output contracts cannot be recommendations in Prompt 26")
        if self.execution_ready:
            raise ValueError("analytics output contracts cannot be execution-ready in Prompt 26")
        if not self.descriptive_only:
            raise ValueError("analytics output contracts must remain descriptive-only")
        return self


class AnalyticsModulePlan(BaseModel):
    module_id: str
    name: str
    stage: AnalyticsStage
    purpose: str
    planned_inputs: list[AnalyticsInputContract]
    planned_outputs: list[AnalyticsOutputContract]
    dependencies_required: list[str] = Field(default_factory=list)
    blocked_capabilities: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("module_id", "name", "purpose", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "analytics module plan text fields")

    @field_validator("planned_inputs")
    @classmethod
    def planned_inputs_must_be_present(
        cls,
        value: list[AnalyticsInputContract],
    ) -> list[AnalyticsInputContract]:
        if not value:
            raise ValueError("planned_inputs cannot be empty")
        return value

    @field_validator("planned_outputs")
    @classmethod
    def planned_outputs_must_be_present(
        cls,
        value: list[AnalyticsOutputContract],
    ) -> list[AnalyticsOutputContract]:
        if not value:
            raise ValueError("planned_outputs cannot be empty")
        return value

    @field_validator("dependencies_required", "blocked_capabilities", "notes")
    @classmethod
    def list_fields_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @model_validator(mode="after")
    def blocked_capabilities_must_include_safety_boundaries(self) -> AnalyticsModulePlan:
        normalized = {item.lower().replace("-", "_").replace(" ", "_") for item in self.blocked_capabilities}
        required = {"trade_signals", "recommendations", "execution", "decision_generation"}
        missing = sorted(required - normalized)
        if missing:
            raise ValueError(f"analytics module plans must block: {', '.join(missing)}")
        return self


def create_default_analytics_input_contract(
    contract_id: str,
    name: str,
    accepted_data_kinds: list[str] | None = None,
) -> AnalyticsInputContract:
    return AnalyticsInputContract(
        contract_id=contract_id,
        name=name,
        accepted_data_kinds=accepted_data_kinds or ["validated_ohlcv_bars", "dataset_manifest_metadata"],
        notes=[
            "Planning contract only; future analytics must use validated input data and source references.",
            "Synthetic/local test data is allowed; real data remains unavailable in Prompt 26.",
        ],
    )


def create_default_descriptive_output_contract(
    contract_id: str,
    name: str,
    output_kind: AnalyticsOutputKind = AnalyticsOutputKind.DESCRIPTIVE_STATISTIC,
    safety_level: AnalyticsSafetyLevel = AnalyticsSafetyLevel.RESEARCH_ONLY,
) -> AnalyticsOutputContract:
    return AnalyticsOutputContract(
        contract_id=contract_id,
        name=name,
        output_kind=output_kind,
        safety_level=safety_level,
        notes=[
            "Descriptive/research-only output contract.",
            "No signals, recommendations, decisions, backtests, or execution readiness.",
        ],
    )


def _plan(
    module_id: str,
    name: str,
    stage: AnalyticsStage,
    purpose: str,
    output_kind: AnalyticsOutputKind = AnalyticsOutputKind.TIME_SERIES_METRIC,
) -> AnalyticsModulePlan:
    return AnalyticsModulePlan(
        module_id=module_id,
        name=name,
        stage=stage,
        purpose=purpose,
        planned_inputs=[
            create_default_analytics_input_contract(
                contract_id=f"{module_id}_input_v1",
                name=f"{name} input contract",
            )
        ],
        planned_outputs=[
            create_default_descriptive_output_contract(
                contract_id=f"{module_id}_output_v1",
                name=f"{name} descriptive output contract",
                output_kind=output_kind,
            )
        ],
        dependencies_required=[],
        blocked_capabilities=[
            "trade_signals",
            "recommendations",
            "execution",
            "decision_generation",
            "broker_integration",
        ],
        notes=["Plan only; no analytics calculations are implemented in Prompt 26."],
    )


def default_analytics_module_plans() -> list[AnalyticsModulePlan]:
    return [
        _plan(
            "numerical_core",
            "Numerical Core",
            AnalyticsStage.NUMERICAL_CORE_PLANNED,
            "Plan safe array/table contracts and deterministic numerical helpers in a future prompt.",
            AnalyticsOutputKind.DIAGNOSTIC,
        ),
        _plan(
            "returns_analytics",
            "Returns Analytics",
            AnalyticsStage.RETURNS_ANALYTICS_PLANNED,
            "Plan future descriptive return calculations without signals or recommendations.",
        ),
        _plan(
            "rolling_window_analytics",
            "Rolling Window Analytics",
            AnalyticsStage.RETURNS_ANALYTICS_PLANNED,
            "Plan future rolling descriptive windows with validation gates and source references.",
        ),
        _plan(
            "volatility_analytics",
            "Volatility Analytics",
            AnalyticsStage.VOLATILITY_ANALYTICS_PLANNED,
            "Plan future descriptive volatility calculations without model authority.",
            AnalyticsOutputKind.RISK_METRIC,
        ),
        _plan(
            "drawdown_analytics",
            "Drawdown Analytics",
            AnalyticsStage.DRAWDOWN_ANALYTICS_PLANNED,
            "Plan future descriptive drawdown and risk metrics without trade calls.",
            AnalyticsOutputKind.RISK_METRIC,
        ),
        _plan(
            "correlation_beta_analytics",
            "Correlation and Beta Analytics",
            AnalyticsStage.CORRELATION_ANALYTICS_PLANNED,
            "Plan future correlation and beta metrics as descriptive research artifacts.",
        ),
        _plan(
            "time_series_diagnostics",
            "Time-Series Diagnostics",
            AnalyticsStage.CONTRACTS_ONLY,
            "Plan future diagnostics for input quality and statistical assumptions.",
            AnalyticsOutputKind.DIAGNOSTIC,
        ),
        _plan(
            "regime_analytics_planned",
            "Regime Analytics Planned",
            AnalyticsStage.REGIME_ANALYTICS_PLANNED,
            "Plan future regime analytics guardrails without classification outputs in Prompt 26.",
            AnalyticsOutputKind.RESEARCH_ARTIFACT,
        ),
        _plan(
            "backtesting_planned",
            "Backtesting Planned",
            AnalyticsStage.BACKTESTING_PLANNED,
            "Plan future backtesting boundaries; no backtest engine exists in Prompt 26.",
            AnalyticsOutputKind.RESEARCH_ARTIFACT,
        ),
    ]
