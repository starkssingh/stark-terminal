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


DEFAULT_STRATEGY_RESEARCH_FORBIDDEN_MODULE_BEHAVIORS = [
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
]


class StrategyResearchModuleBoundaryPolicy(BaseModel):
    policy_id: str
    module_family: str
    allowed_purpose: str
    forbidden_behaviors: list[StrategyResearchForbiddenBehaviorKind]
    may_create_active_ui: bool = False
    may_create_frontend_components: bool = False
    may_create_desktop_components: bool = False
    may_ingest_papers: bool = False
    may_parse_papers: bool = False
    may_generate_strategies: bool = False
    may_generate_strategy_code: bool = False
    may_run_backtests: bool = False
    may_optimize: bool = False
    may_generate_recommendations: bool = False
    may_generate_actions: bool = False
    may_score_confidence: bool = False
    may_generate_decision_objects: bool = False
    may_generate_readiness_to_trade: bool = False
    may_expose_broker_controls: bool = False
    may_execute: bool = False
    may_grant_approval: bool = False
    may_grant_override: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("policy_id", "module_family", "allowed_purpose", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research module boundary policy text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def module_policy_must_fail_closed(self) -> StrategyResearchModuleBoundaryPolicy:
        if not self.forbidden_behaviors:
            raise ValueError("strategy research module boundary policy requires forbidden behaviors")
        if StrategyResearchForbiddenBehaviorKind.UNKNOWN in self.forbidden_behaviors:
            raise ValueError("UNKNOWN strategy research forbidden behavior is not allowed")
        if self.may_create_active_ui:
            raise ValueError("strategy research modules may not create active UI in Prompt 68")
        if self.may_create_frontend_components:
            raise ValueError("strategy research modules may not create frontend components in Prompt 68")
        if self.may_create_desktop_components:
            raise ValueError("strategy research modules may not create desktop components in Prompt 68")
        if self.may_ingest_papers:
            raise ValueError("strategy research modules may not ingest papers in Prompt 68")
        if self.may_parse_papers:
            raise ValueError("strategy research modules may not parse papers in Prompt 68")
        if self.may_generate_strategies:
            raise ValueError("strategy research modules may not generate strategies in Prompt 68")
        if self.may_generate_strategy_code:
            raise ValueError("strategy research modules may not generate strategy code in Prompt 68")
        if self.may_run_backtests:
            raise ValueError("strategy research modules may not run backtests in Prompt 68")
        if self.may_optimize:
            raise ValueError("strategy research modules may not optimize in Prompt 68")
        if self.may_generate_recommendations:
            raise ValueError("strategy research modules may not generate recommendations in Prompt 68")
        if self.may_generate_actions:
            raise ValueError("strategy research modules may not generate actions in Prompt 68")
        if self.may_score_confidence:
            raise ValueError("strategy research modules may not score confidence in Prompt 68")
        if self.may_generate_decision_objects:
            raise ValueError("strategy research modules may not generate DecisionObjects in Prompt 68")
        if self.may_generate_readiness_to_trade:
            raise ValueError("strategy research modules may not generate readiness-to-trade in Prompt 68")
        if self.may_expose_broker_controls:
            raise ValueError("strategy research modules may not expose broker controls in Prompt 68")
        if self.may_execute:
            raise ValueError("strategy research modules may not execute in Prompt 68")
        if self.may_grant_approval:
            raise ValueError("strategy research modules may not grant approval in Prompt 68")
        if self.may_grant_override:
            raise ValueError("strategy research modules may not grant override in Prompt 68")
        return self


def _module_policy(module_family: str, allowed_purpose: str) -> StrategyResearchModuleBoundaryPolicy:
    return StrategyResearchModuleBoundaryPolicy(
        policy_id=f"{module_family.replace('_', '-')}-boundary-policy-v1",
        module_family=module_family,
        allowed_purpose=allowed_purpose,
        forbidden_behaviors=list(DEFAULT_STRATEGY_RESEARCH_FORBIDDEN_MODULE_BEHAVIORS),
    )


def default_strategy_research_module_boundary_policies() -> list[
    StrategyResearchModuleBoundaryPolicy
]:
    return [
        _module_policy("strategy_research_workspace", "planning and guardrail placeholders only"),
        _module_policy("strategy_research_workspace_api", "API contract skeleton placeholders only"),
        _module_policy("strategy_research_workspace_display", "display contract skeleton placeholders only"),
        _module_policy(
            "strategy_research_workspace_boundary",
            "boundary-hardening contracts and invariant helpers only",
        ),
    ]


def evaluate_strategy_research_module_boundary_policies(
    policies: list[StrategyResearchModuleBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_strategy_research_module_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if policy.may_create_active_ui:
            blockers.append(f"{policy.module_family}: may create active UI")
        if policy.may_create_frontend_components:
            blockers.append(f"{policy.module_family}: may create frontend components")
        if policy.may_create_desktop_components:
            blockers.append(f"{policy.module_family}: may create desktop components")
        if policy.may_ingest_papers:
            blockers.append(f"{policy.module_family}: may ingest papers")
        if policy.may_parse_papers:
            blockers.append(f"{policy.module_family}: may parse papers")
        if policy.may_generate_strategies:
            blockers.append(f"{policy.module_family}: may generate strategies")
        if policy.may_generate_strategy_code:
            blockers.append(f"{policy.module_family}: may generate strategy code")
        if policy.may_run_backtests:
            blockers.append(f"{policy.module_family}: may run backtests")
        if policy.may_optimize:
            blockers.append(f"{policy.module_family}: may optimize")
        if policy.may_generate_recommendations:
            blockers.append(f"{policy.module_family}: may generate recommendations")
        if policy.may_generate_actions:
            blockers.append(f"{policy.module_family}: may generate actions")
        if policy.may_score_confidence:
            blockers.append(f"{policy.module_family}: may score confidence")
        if policy.may_generate_decision_objects:
            blockers.append(f"{policy.module_family}: may generate DecisionObjects")
        if policy.may_generate_readiness_to_trade:
            blockers.append(f"{policy.module_family}: may generate readiness-to-trade")
        if policy.may_expose_broker_controls:
            blockers.append(f"{policy.module_family}: may expose broker controls")
        if policy.may_execute:
            blockers.append(f"{policy.module_family}: may execute")
        if policy.may_grant_approval:
            blockers.append(f"{policy.module_family}: may grant approval")
        if policy.may_grant_override:
            blockers.append(f"{policy.module_family}: may grant override")
    return blockers
