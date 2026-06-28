from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class StrategyResearchWorkspaceBoundaryStage(StrEnum):
    BOUNDARY_HARDENING = "BOUNDARY_HARDENING"
    AUDIT_ONLY = "AUDIT_ONLY"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class StrategyResearchForbiddenBehaviorKind(StrEnum):
    ACTIVE_UI = "ACTIVE_UI"
    FRONTEND_COMPONENT = "FRONTEND_COMPONENT"
    DESKTOP_COMPONENT = "DESKTOP_COMPONENT"
    PAPER_INGESTION = "PAPER_INGESTION"
    PAPER_PARSING = "PAPER_PARSING"
    ARXIV_INGESTION = "ARXIV_INGESTION"
    LLM_PAPER_ANALYSIS = "LLM_PAPER_ANALYSIS"
    METHOD_EXTRACTION = "METHOD_EXTRACTION"
    STRATEGY_EXTRACTION = "STRATEGY_EXTRACTION"
    STRATEGY_GENERATION = "STRATEGY_GENERATION"
    STRATEGY_CODE_GENERATION = "STRATEGY_CODE_GENERATION"
    SIGNAL_GENERATION = "SIGNAL_GENERATION"
    FACTOR_GENERATION = "FACTOR_GENERATION"
    ALPHA_GENERATION = "ALPHA_GENERATION"
    BACKTESTING = "BACKTESTING"
    OPTIMIZATION = "OPTIMIZATION"
    PARAMETER_SEARCH = "PARAMETER_SEARCH"
    WALK_FORWARD_ANALYSIS = "WALK_FORWARD_ANALYSIS"
    PERFORMANCE_CLAIMS = "PERFORMANCE_CLAIMS"
    RECOMMENDATION_GENERATION = "RECOMMENDATION_GENERATION"
    ACTION_GENERATION = "ACTION_GENERATION"
    CONFIDENCE_SCORING = "CONFIDENCE_SCORING"
    DECISION_OBJECT_GENERATION = "DECISION_OBJECT_GENERATION"
    READINESS_TO_TRADE = "READINESS_TO_TRADE"
    BROKER_CONTROL = "BROKER_CONTROL"
    ORDER_BUTTON = "ORDER_BUTTON"
    EXECUTION = "EXECUTION"
    APPROVAL_CONTROL = "APPROVAL_CONTROL"
    OVERRIDE_CONTROL = "OVERRIDE_CONTROL"
    LIVE_DATA_DISPLAY = "LIVE_DATA_DISPLAY"
    EXTERNAL_CALL = "EXTERNAL_CALL"
    SECRET_OR_CREDENTIAL = "SECRET_OR_CREDENTIAL"
    PROVIDER_SDK = "PROVIDER_SDK"
    SCRAPING = "SCRAPING"
    UNKNOWN = "UNKNOWN"


class StrategyResearchBoundarySeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"
    UNKNOWN = "UNKNOWN"


class StrategyResearchBoundarySafetyLabel(StrEnum):
    BOUNDARY_HARDENING_ONLY = "BOUNDARY_HARDENING_ONLY"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
    NOT_A_PAPER_PARSER = "NOT_A_PAPER_PARSER"
    NOT_A_STRATEGY = "NOT_A_STRATEGY"
    NOT_A_BACKTEST = "NOT_A_BACKTEST"
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


def sanitize_strategy_research_boundary_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


REQUIRED_STRATEGY_RESEARCH_FORBIDDEN_BEHAVIORS = {
    StrategyResearchForbiddenBehaviorKind.ACTIVE_UI,
    StrategyResearchForbiddenBehaviorKind.FRONTEND_COMPONENT,
    StrategyResearchForbiddenBehaviorKind.DESKTOP_COMPONENT,
    StrategyResearchForbiddenBehaviorKind.PAPER_INGESTION,
    StrategyResearchForbiddenBehaviorKind.PAPER_PARSING,
    StrategyResearchForbiddenBehaviorKind.ARXIV_INGESTION,
    StrategyResearchForbiddenBehaviorKind.LLM_PAPER_ANALYSIS,
    StrategyResearchForbiddenBehaviorKind.METHOD_EXTRACTION,
    StrategyResearchForbiddenBehaviorKind.STRATEGY_EXTRACTION,
    StrategyResearchForbiddenBehaviorKind.STRATEGY_GENERATION,
    StrategyResearchForbiddenBehaviorKind.STRATEGY_CODE_GENERATION,
    StrategyResearchForbiddenBehaviorKind.SIGNAL_GENERATION,
    StrategyResearchForbiddenBehaviorKind.FACTOR_GENERATION,
    StrategyResearchForbiddenBehaviorKind.ALPHA_GENERATION,
    StrategyResearchForbiddenBehaviorKind.BACKTESTING,
    StrategyResearchForbiddenBehaviorKind.OPTIMIZATION,
    StrategyResearchForbiddenBehaviorKind.PARAMETER_SEARCH,
    StrategyResearchForbiddenBehaviorKind.WALK_FORWARD_ANALYSIS,
    StrategyResearchForbiddenBehaviorKind.PERFORMANCE_CLAIMS,
    StrategyResearchForbiddenBehaviorKind.RECOMMENDATION_GENERATION,
    StrategyResearchForbiddenBehaviorKind.ACTION_GENERATION,
    StrategyResearchForbiddenBehaviorKind.CONFIDENCE_SCORING,
    StrategyResearchForbiddenBehaviorKind.DECISION_OBJECT_GENERATION,
    StrategyResearchForbiddenBehaviorKind.READINESS_TO_TRADE,
    StrategyResearchForbiddenBehaviorKind.BROKER_CONTROL,
    StrategyResearchForbiddenBehaviorKind.ORDER_BUTTON,
    StrategyResearchForbiddenBehaviorKind.EXECUTION,
    StrategyResearchForbiddenBehaviorKind.APPROVAL_CONTROL,
    StrategyResearchForbiddenBehaviorKind.OVERRIDE_CONTROL,
    StrategyResearchForbiddenBehaviorKind.LIVE_DATA_DISPLAY,
    StrategyResearchForbiddenBehaviorKind.EXTERNAL_CALL,
    StrategyResearchForbiddenBehaviorKind.SECRET_OR_CREDENTIAL,
    StrategyResearchForbiddenBehaviorKind.PROVIDER_SDK,
    StrategyResearchForbiddenBehaviorKind.SCRAPING,
}


class StrategyResearchForbiddenBehavior(BaseModel):
    behavior_id: str
    kind: StrategyResearchForbiddenBehaviorKind
    name: str
    description: str
    severity: StrategyResearchBoundarySeverity = StrategyResearchBoundarySeverity.BLOCKER
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("behavior_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research forbidden behavior text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_boundary_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def behavior_must_remain_forbidden(self) -> StrategyResearchForbiddenBehavior:
        if self.kind == StrategyResearchForbiddenBehaviorKind.UNKNOWN:
            raise ValueError("UNKNOWN strategy research forbidden behavior kind is not allowed")
        if self.severity == StrategyResearchBoundarySeverity.UNKNOWN:
            raise ValueError("UNKNOWN strategy research boundary severity is not allowed")
        if not self.forbidden_now:
            raise ValueError("strategy research forbidden behavior cannot be unlocked in Prompt 68")
        if not self.requires_future_prompt:
            raise ValueError("strategy research forbidden behavior requires a future prompt before unlock")
        if not self.requires_audit_before_unlock:
            raise ValueError("strategy research forbidden behavior requires audit before unlock")
        return self


class StrategyResearchForbiddenBehaviorRegistry(BaseModel):
    registry_id: str
    behaviors: list[StrategyResearchForbiddenBehavior]
    complete: bool = True
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    paper_ingestion_allowed: bool = False
    paper_parsing_allowed: bool = False
    strategy_generation_allowed: bool = False
    strategy_code_generation_allowed: bool = False
    backtesting_allowed: bool = False
    optimization_allowed: bool = False
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
        return _non_empty_text(value, "strategy research forbidden behavior registry text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def registry_must_cover_required_behaviors(self) -> StrategyResearchForbiddenBehaviorRegistry:
        if not self.behaviors:
            raise ValueError("strategy research forbidden behavior registry requires behaviors")
        if not self.complete:
            raise ValueError("strategy research forbidden behavior registry must be complete")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "paper ingestion": self.paper_ingestion_allowed,
            "paper parsing": self.paper_parsing_allowed,
            "strategy generation": self.strategy_generation_allowed,
            "strategy code generation": self.strategy_code_generation_allowed,
            "backtesting": self.backtesting_allowed,
            "optimization": self.optimization_allowed,
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
            raise ValueError(f"strategy research boundary cannot allow: {', '.join(enabled)}")
        present = {behavior.kind for behavior in self.behaviors}
        missing = sorted(kind.value for kind in REQUIRED_STRATEGY_RESEARCH_FORBIDDEN_BEHAVIORS - present)
        if missing:
            raise ValueError(
                "strategy research forbidden registry missing required kinds: "
                + ", ".join(missing)
            )
        return self


def default_strategy_research_forbidden_behaviors() -> list[StrategyResearchForbiddenBehavior]:
    behavior_specs = [
        (StrategyResearchForbiddenBehaviorKind.ACTIVE_UI, "Active Strategy Research Workspace UI"),
        (StrategyResearchForbiddenBehaviorKind.FRONTEND_COMPONENT, "Frontend research component"),
        (StrategyResearchForbiddenBehaviorKind.DESKTOP_COMPONENT, "Desktop research component"),
        (StrategyResearchForbiddenBehaviorKind.PAPER_INGESTION, "Paper ingestion"),
        (StrategyResearchForbiddenBehaviorKind.PAPER_PARSING, "Paper parsing"),
        (StrategyResearchForbiddenBehaviorKind.ARXIV_INGESTION, "arXiv ingestion"),
        (StrategyResearchForbiddenBehaviorKind.LLM_PAPER_ANALYSIS, "LLM paper analysis"),
        (StrategyResearchForbiddenBehaviorKind.METHOD_EXTRACTION, "Method extraction"),
        (StrategyResearchForbiddenBehaviorKind.STRATEGY_EXTRACTION, "Strategy extraction"),
        (StrategyResearchForbiddenBehaviorKind.STRATEGY_GENERATION, "Strategy generation"),
        (StrategyResearchForbiddenBehaviorKind.STRATEGY_CODE_GENERATION, "Strategy code generation"),
        (StrategyResearchForbiddenBehaviorKind.SIGNAL_GENERATION, "Signal generation"),
        (StrategyResearchForbiddenBehaviorKind.FACTOR_GENERATION, "Factor generation"),
        (StrategyResearchForbiddenBehaviorKind.ALPHA_GENERATION, "Alpha generation"),
        (StrategyResearchForbiddenBehaviorKind.BACKTESTING, "Backtesting"),
        (StrategyResearchForbiddenBehaviorKind.OPTIMIZATION, "Optimization"),
        (StrategyResearchForbiddenBehaviorKind.PARAMETER_SEARCH, "Parameter search"),
        (StrategyResearchForbiddenBehaviorKind.WALK_FORWARD_ANALYSIS, "Walk-forward analysis"),
        (StrategyResearchForbiddenBehaviorKind.PERFORMANCE_CLAIMS, "Performance claims"),
        (StrategyResearchForbiddenBehaviorKind.RECOMMENDATION_GENERATION, "Recommendation generation"),
        (StrategyResearchForbiddenBehaviorKind.ACTION_GENERATION, "Action generation"),
        (StrategyResearchForbiddenBehaviorKind.CONFIDENCE_SCORING, "Confidence scoring"),
        (StrategyResearchForbiddenBehaviorKind.DECISION_OBJECT_GENERATION, "DecisionObject generation"),
        (StrategyResearchForbiddenBehaviorKind.READINESS_TO_TRADE, "Readiness-to-trade"),
        (StrategyResearchForbiddenBehaviorKind.BROKER_CONTROL, "Broker control"),
        (StrategyResearchForbiddenBehaviorKind.ORDER_BUTTON, "Order button"),
        (StrategyResearchForbiddenBehaviorKind.EXECUTION, "Execution behavior"),
        (StrategyResearchForbiddenBehaviorKind.APPROVAL_CONTROL, "Approval control"),
        (StrategyResearchForbiddenBehaviorKind.OVERRIDE_CONTROL, "Override control"),
        (StrategyResearchForbiddenBehaviorKind.LIVE_DATA_DISPLAY, "Live data display"),
        (StrategyResearchForbiddenBehaviorKind.EXTERNAL_CALL, "External call"),
        (StrategyResearchForbiddenBehaviorKind.SECRET_OR_CREDENTIAL, "Secret or credential"),
        (StrategyResearchForbiddenBehaviorKind.PROVIDER_SDK, "Provider SDK"),
        (StrategyResearchForbiddenBehaviorKind.SCRAPING, "Scraping behavior"),
    ]
    return [
        StrategyResearchForbiddenBehavior(
            behavior_id=f"strategy-research-{kind.value.lower().replace('_', '-')}-forbidden-v1",
            kind=kind,
            name=name,
            description=f"{name} remains forbidden by the Prompt 68 boundary-hardening layer.",
            notes=[
                "boundary-hardening-only",
                "requires future prompt",
                "requires audit before unlock",
            ],
        )
        for kind, name in behavior_specs
    ]


def default_strategy_research_forbidden_behavior_registry() -> StrategyResearchForbiddenBehaviorRegistry:
    return StrategyResearchForbiddenBehaviorRegistry(
        registry_id="strategy-research-forbidden-behavior-registry-v1",
        behaviors=default_strategy_research_forbidden_behaviors(),
    )
