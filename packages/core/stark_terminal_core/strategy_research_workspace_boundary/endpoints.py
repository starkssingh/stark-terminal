from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_boundary.forbidden import (
    StrategyResearchForbiddenBehaviorKind,
    _non_empty_text,
    _utc_datetime,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


DEFAULT_STRATEGY_RESEARCH_FORBIDDEN_ENDPOINT_OUTPUTS = [
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
]


class StrategyResearchEndpointBoundaryPolicy(BaseModel):
    policy_id: str
    endpoint_family: str
    allowed_methods: list[str]
    forbidden_methods: list[str]
    forbidden_outputs: list[StrategyResearchForbiddenBehaviorKind]
    read_only: bool = True
    unavailable_by_default: bool = True
    accepts_paper_input: bool = False
    accepts_market_data_for_research_decision: bool = False
    generates_active_ui: bool = False
    ingests_paper: bool = False
    parses_paper: bool = False
    generates_strategy: bool = False
    generates_backtest: bool = False
    generates_recommendation: bool = False
    generates_decision_object: bool = False
    exposes_broker_controls: bool = False
    executes_trade: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("policy_id", "endpoint_family", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research endpoint boundary policy text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def endpoint_policy_must_fail_closed(self) -> StrategyResearchEndpointBoundaryPolicy:
        if not self.allowed_methods:
            raise ValueError("strategy research endpoint boundary policy requires allowed methods")
        if any(not method.strip() for method in self.allowed_methods):
            raise ValueError("strategy research endpoint allowed methods cannot be empty")
        if not self.forbidden_outputs:
            raise ValueError("strategy research endpoint boundary policy requires forbidden outputs")
        if StrategyResearchForbiddenBehaviorKind.UNKNOWN in self.forbidden_outputs:
            raise ValueError("UNKNOWN strategy research forbidden endpoint output is not allowed")
        if not self.read_only:
            raise ValueError("strategy research endpoint boundary policies must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("strategy research endpoint boundary policies must be unavailable by default")
        if self.accepts_paper_input:
            raise ValueError("paper/PDF/arXiv input endpoints are forbidden")
        if self.accepts_market_data_for_research_decision:
            raise ValueError("market-data-to-research-decision endpoints are forbidden")
        if self.generates_active_ui:
            raise ValueError("strategy research active UI endpoints are forbidden")
        if self.ingests_paper:
            raise ValueError("strategy research paper ingestion endpoints are forbidden")
        if self.parses_paper:
            raise ValueError("strategy research paper parsing endpoints are forbidden")
        if self.generates_strategy:
            raise ValueError("strategy research strategy generation endpoints are forbidden")
        if self.generates_backtest:
            raise ValueError("strategy research backtesting endpoints are forbidden")
        if self.generates_recommendation:
            raise ValueError("strategy research recommendation endpoints are forbidden")
        if self.generates_decision_object:
            raise ValueError("strategy research DecisionObject endpoints are forbidden")
        if self.exposes_broker_controls:
            raise ValueError("strategy research broker-control endpoints are forbidden")
        if self.executes_trade:
            raise ValueError("strategy research execution endpoints are forbidden")
        return self


def _endpoint_policy(endpoint_family: str) -> StrategyResearchEndpointBoundaryPolicy:
    return StrategyResearchEndpointBoundaryPolicy(
        policy_id=f"{endpoint_family}-boundary-policy-v1",
        endpoint_family=endpoint_family,
        allowed_methods=["GET"],
        forbidden_methods=["POST", "PUT", "PATCH", "DELETE"],
        forbidden_outputs=list(DEFAULT_STRATEGY_RESEARCH_FORBIDDEN_ENDPOINT_OUTPUTS),
    )


def default_strategy_research_endpoint_boundary_policies() -> list[
    StrategyResearchEndpointBoundaryPolicy
]:
    return [
        _endpoint_policy("strategy-research-workspace"),
        _endpoint_policy("strategy-research-workspace-api"),
        _endpoint_policy("strategy-research-workspace-display"),
        _endpoint_policy("strategy-research-workspace-boundary"),
    ]


def evaluate_strategy_research_endpoint_boundary_policies(
    policies: list[StrategyResearchEndpointBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_strategy_research_endpoint_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if not policy.read_only:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not read-only")
        if not policy.unavailable_by_default:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not unavailable by default")
        if policy.accepts_paper_input:
            blockers.append(f"{policy.endpoint_family}: accepts paper/PDF/arXiv input")
        if policy.accepts_market_data_for_research_decision:
            blockers.append(f"{policy.endpoint_family}: accepts market data for research decision")
        if policy.generates_active_ui:
            blockers.append(f"{policy.endpoint_family}: generates active UI")
        if policy.ingests_paper:
            blockers.append(f"{policy.endpoint_family}: ingests papers")
        if policy.parses_paper:
            blockers.append(f"{policy.endpoint_family}: parses papers")
        if policy.generates_strategy:
            blockers.append(f"{policy.endpoint_family}: generates strategies")
        if policy.generates_backtest:
            blockers.append(f"{policy.endpoint_family}: generates backtests")
        if policy.generates_recommendation:
            blockers.append(f"{policy.endpoint_family}: generates recommendations")
        if policy.generates_decision_object:
            blockers.append(f"{policy.endpoint_family}: generates DecisionObjects")
        if policy.exposes_broker_controls:
            blockers.append(f"{policy.endpoint_family}: exposes broker controls")
        if policy.executes_trade:
            blockers.append(f"{policy.endpoint_family}: executes trade")
    return blockers
