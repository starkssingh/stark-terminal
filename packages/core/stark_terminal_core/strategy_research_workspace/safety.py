from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace.artifacts import StrategyResearchArtifactPlaceholder
from stark_terminal_core.strategy_research_workspace.experiments import StrategyResearchExperimentPlaceholder
from stark_terminal_core.strategy_research_workspace.papers import StrategyResearchPaperReferencePlaceholder
from stark_terminal_core.strategy_research_workspace.planning import (
    StrategyResearchWorkspacePlanningContract,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_notes,
)
from stark_terminal_core.strategy_research_workspace.strategies import StrategyResearchHypothesisPlaceholder
from stark_terminal_core.strategy_research_workspace.workspaces import StrategyResearchWorkspacePlaceholder


class StrategyResearchSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_active_ui: bool = False
    allow_frontend_components: bool = False
    allow_desktop_components: bool = False
    allow_paper_ingestion: bool = False
    allow_paper_parsing: bool = False
    allow_strategy_generation: bool = False
    allow_strategy_code_generation: bool = False
    allow_backtesting: bool = False
    allow_optimization: bool = False
    allow_recommendations: bool = False
    allow_action_generation: bool = False
    allow_confidence_scoring: bool = False
    allow_decision_object_generation: bool = False
    allow_readiness_to_trade: bool = False
    allow_broker_controls: bool = False
    allow_execution: bool = False
    allow_approval: bool = False
    allow_override: bool = False
    require_planning_only: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_notes(value)

    @model_validator(mode="after")
    def safety_policy_must_fail_closed(self) -> StrategyResearchSafetyPolicy:
        dangerous_flags = {
            "active UI": self.allow_active_ui,
            "frontend components": self.allow_frontend_components,
            "desktop components": self.allow_desktop_components,
            "paper ingestion": self.allow_paper_ingestion,
            "paper parsing": self.allow_paper_parsing,
            "strategy generation": self.allow_strategy_generation,
            "strategy code generation": self.allow_strategy_code_generation,
            "backtesting": self.allow_backtesting,
            "optimization": self.allow_optimization,
            "recommendations": self.allow_recommendations,
            "action generation": self.allow_action_generation,
            "confidence scoring": self.allow_confidence_scoring,
            "DecisionObject generation": self.allow_decision_object_generation,
            "readiness-to-trade": self.allow_readiness_to_trade,
            "broker controls": self.allow_broker_controls,
            "execution": self.allow_execution,
            "approval": self.allow_approval,
            "override": self.allow_override,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Strategy Research safety policy cannot allow: " + ", ".join(enabled))
        if not self.require_planning_only:
            raise ValueError("Strategy Research Workspace must require planning-only behavior in Prompt 63")
        return self


class StrategyResearchSafetyResult(BaseModel):
    result_id: str
    policy_id: str
    safe: bool
    reasons: list[str]
    planning_only: bool = True
    active_ui_allowed: bool = False
    strategy_generation_allowed: bool = False
    backtesting_allowed: bool = False
    recommendations_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_strategy_research_notes(value)
        if not sanitized:
            raise ValueError("Strategy Research safety result reasons cannot be empty")
        return sanitized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def safety_result_must_fail_closed(self) -> StrategyResearchSafetyResult:
        if not self.planning_only:
            raise ValueError("Strategy Research safety result must remain planning-only")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "strategy generation": self.strategy_generation_allowed,
            "backtesting": self.backtesting_allowed,
            "recommendations": self.recommendations_allowed,
            "broker controls": self.broker_controls_allowed,
            "execution": self.execution_allowed,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("Strategy Research safety result cannot allow: " + ", ".join(enabled))
        return self


def default_strategy_research_safety_policy(settings: Any | None = None) -> StrategyResearchSafetyPolicy:
    notes = ["Prompt 63 permits Strategy Research Workspace planning and guardrails only."]
    if settings is not None:
        notes.append(f"stage={settings.strategy_research_workspace_stage}")
    return StrategyResearchSafetyPolicy(
        policy_id="strategy-research-workspace-safety-policy-v1",
        name="Strategy Research Workspace Safety Policy",
        notes=notes,
    )


def _safety_result(result_id: str, policy_id: str, reasons: list[str], safe: bool) -> StrategyResearchSafetyResult:
    return StrategyResearchSafetyResult(result_id=result_id, policy_id=policy_id, safe=safe, reasons=reasons)


def _unsafe_policy_reasons(policy: StrategyResearchSafetyPolicy) -> list[str]:
    reasons: list[str] = []
    if policy.allow_active_ui:
        reasons.append("Strategy Research Workspace policy cannot allow active UI")
    if policy.allow_frontend_components:
        reasons.append("Strategy Research Workspace policy cannot allow frontend components")
    if policy.allow_desktop_components:
        reasons.append("Strategy Research Workspace policy cannot allow desktop components")
    if policy.allow_paper_ingestion:
        reasons.append("Strategy Research Workspace policy cannot allow paper ingestion")
    if policy.allow_paper_parsing:
        reasons.append("Strategy Research Workspace policy cannot allow paper parsing")
    if policy.allow_strategy_generation:
        reasons.append("Strategy Research Workspace policy cannot allow strategy generation")
    if policy.allow_strategy_code_generation:
        reasons.append("Strategy Research Workspace policy cannot allow strategy code generation")
    if policy.allow_backtesting:
        reasons.append("Strategy Research Workspace policy cannot allow backtesting")
    if policy.allow_optimization:
        reasons.append("Strategy Research Workspace policy cannot allow optimization")
    if policy.allow_recommendations:
        reasons.append("Strategy Research Workspace policy cannot allow recommendations")
    if policy.allow_action_generation:
        reasons.append("Strategy Research Workspace policy cannot allow action generation")
    if policy.allow_confidence_scoring:
        reasons.append("Strategy Research Workspace policy cannot allow confidence scoring")
    if policy.allow_decision_object_generation:
        reasons.append("Strategy Research Workspace policy cannot allow DecisionObject generation")
    if policy.allow_readiness_to_trade:
        reasons.append("Strategy Research Workspace policy cannot allow readiness-to-trade")
    if policy.allow_broker_controls:
        reasons.append("Strategy Research Workspace policy cannot allow broker controls")
    if policy.allow_execution:
        reasons.append("Strategy Research Workspace policy cannot allow execution")
    if policy.allow_approval:
        reasons.append("Strategy Research Workspace policy cannot allow approvals")
    if policy.allow_override:
        reasons.append("Strategy Research Workspace policy cannot allow overrides")
    if not policy.require_planning_only:
        reasons.append("Strategy Research Workspace policy must require planning-only behavior")
    return reasons


def evaluate_strategy_research_plan_safety(
    plan: StrategyResearchWorkspacePlanningContract,
    policy: StrategyResearchSafetyPolicy,
) -> StrategyResearchSafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    if plan.active_ui_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow active UI")
    if plan.frontend_components_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow frontend components")
    if plan.desktop_components_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow desktop components")
    if plan.paper_ingestion_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow paper ingestion")
    if plan.paper_parsing_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow paper parsing")
    if plan.strategy_generation_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow strategy generation")
    if plan.strategy_code_generation_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow strategy code generation")
    if plan.backtesting_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow backtesting")
    if plan.optimization_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow optimization")
    if plan.recommendations_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow recommendations")
    if plan.action_generation_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow action generation")
    if plan.confidence_scoring_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow confidence scoring")
    if plan.decision_object_generation_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow DecisionObject generation")
    if plan.readiness_to_trade_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow readiness-to-trade")
    if plan.broker_controls_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow broker controls")
    if plan.execution_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow execution")
    if plan.approval_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow approvals")
    if plan.override_allowed:
        reasons.append("Strategy Research Workspace plan cannot allow overrides")
    if not plan.returns_unavailable_by_default:
        reasons.append("Strategy Research Workspace plan must return unavailable by default")
    if reasons:
        return _safety_result("strategy-research-plan-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-plan-safety-safe",
        policy.policy_id,
        ["Strategy Research Workspace plan remains planning-only with no strategy generation, backtesting, recommendations, broker controls, or execution"],
        True,
    )


def evaluate_strategy_research_workspace_safety(
    workspaces: Iterable[StrategyResearchWorkspacePlaceholder],
    policy: StrategyResearchSafetyPolicy,
) -> StrategyResearchSafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    workspace_list = list(workspaces)
    if not workspace_list:
        reasons.append("Strategy Research Workspace placeholders are required")
    for workspace in workspace_list:
        if not workspace.planning_only or workspace.active_ui or not workspace.unavailable:
            reasons.append(f"{workspace.workspace_id} must remain planning-only unavailable metadata")
        if workspace.paper_ingestion_allowed or workspace.paper_parsing_allowed:
            reasons.append(f"{workspace.workspace_id} cannot allow paper ingestion or paper parsing")
        if workspace.strategy_generation_allowed or workspace.backtesting_allowed:
            reasons.append(f"{workspace.workspace_id} cannot allow strategy generation or backtesting")
        if workspace.recommendations_allowed or workspace.execution_allowed:
            reasons.append(f"{workspace.workspace_id} cannot allow recommendations or execution")
    if reasons:
        return _safety_result("strategy-research-workspace-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-workspace-safety-safe",
        policy.policy_id,
        ["Strategy Research Workspace placeholders remain planning-only and unavailable"],
        True,
    )


def evaluate_strategy_research_artifact_safety(
    artifacts: Iterable[StrategyResearchArtifactPlaceholder],
    policy: StrategyResearchSafetyPolicy,
) -> StrategyResearchSafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    artifact_list = list(artifacts)
    if not artifact_list:
        reasons.append("Strategy Research artifact placeholders are required")
    for artifact in artifact_list:
        if not artifact.planning_only:
            reasons.append(f"{artifact.artifact_id} must remain planning-only")
        if artifact.validated or artifact.strategy_ready or artifact.recommendation_ready or artifact.execution_ready:
            reasons.append(f"{artifact.artifact_id} cannot be validated, strategy-ready, recommendation-ready, or execution-ready")
        if artifact.paper_parsed or artifact.backtest_ready:
            reasons.append(f"{artifact.artifact_id} cannot be paper-parsed or backtest-ready")
    if reasons:
        return _safety_result("strategy-research-artifact-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-artifact-safety-safe",
        policy.policy_id,
        ["Strategy Research artifact placeholders remain unvalidated planning metadata"],
        True,
    )


def evaluate_strategy_research_paper_reference_safety(
    papers: Iterable[StrategyResearchPaperReferencePlaceholder],
    policy: StrategyResearchSafetyPolicy,
) -> StrategyResearchSafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    paper_list = list(papers)
    if not paper_list:
        reasons.append("Strategy Research paper reference placeholders are required")
    for paper in paper_list:
        if not paper.planning_only:
            reasons.append(f"{paper.paper_reference_id} must remain planning-only")
        if paper.paper_ingested or paper.paper_parsed or paper.method_extracted or paper.strategy_extracted:
            reasons.append(f"{paper.paper_reference_id} cannot be ingested, parsed, or extracted")
        if paper.code_generated or paper.backtest_generated or paper.recommendation_generated:
            reasons.append(f"{paper.paper_reference_id} cannot generate code, backtests, or recommendations")
    if reasons:
        return _safety_result("strategy-research-paper-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-paper-safety-safe",
        policy.policy_id,
        ["Strategy Research paper references remain placeholders with no ingestion or parsing"],
        True,
    )


def evaluate_strategy_research_hypothesis_safety(
    hypotheses: Iterable[StrategyResearchHypothesisPlaceholder],
    policy: StrategyResearchSafetyPolicy,
) -> StrategyResearchSafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    hypothesis_list = list(hypotheses)
    if not hypothesis_list:
        reasons.append("Strategy Research hypothesis placeholders are required")
    for hypothesis in hypothesis_list:
        if not hypothesis.planning_only:
            reasons.append(f"{hypothesis.hypothesis_id} must remain planning-only")
        if hypothesis.generated_strategy or hypothesis.generated_signal or hypothesis.generated_factor:
            reasons.append(f"{hypothesis.hypothesis_id} cannot generate strategy, signal, or factor")
        if hypothesis.generated_code or hypothesis.backtest_ready or hypothesis.recommendation_ready or hypothesis.execution_ready:
            reasons.append(f"{hypothesis.hypothesis_id} cannot be generated-code, backtest-ready, recommendation-ready, or execution-ready")
    if reasons:
        return _safety_result("strategy-research-hypothesis-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-hypothesis-safety-safe",
        policy.policy_id,
        ["Strategy Research hypotheses remain planning placeholders"],
        True,
    )


def evaluate_strategy_research_experiment_safety(
    experiments: Iterable[StrategyResearchExperimentPlaceholder],
    policy: StrategyResearchSafetyPolicy,
) -> StrategyResearchSafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    experiment_list = list(experiments)
    if not experiment_list:
        reasons.append("Strategy Research experiment placeholders are required")
    for experiment in experiment_list:
        if not experiment.planning_only:
            reasons.append(f"{experiment.experiment_id} must remain planning-only")
        if experiment.executable or experiment.backtest_executable or experiment.optimization_executable:
            reasons.append(f"{experiment.experiment_id} cannot be executable, backtest executable, or optimization executable")
        if experiment.strategy_executable or experiment.live_ready or experiment.recommendation_ready or experiment.execution_ready:
            reasons.append(f"{experiment.experiment_id} cannot be strategy executable, live-ready, recommendation-ready, or execution-ready")
    if reasons:
        return _safety_result("strategy-research-experiment-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-experiment-safety-safe",
        policy.policy_id,
        ["Strategy Research experiments remain planning placeholders"],
        True,
    )


def reject_research_as_active_ui(reason: str = "Strategy Research Workspace active UI is forbidden") -> StrategyResearchSafetyResult:
    return _safety_result("strategy-research-active-ui-rejected", "strategy-research-workspace-safety-policy-v1", [reason], False)


def reject_research_as_strategy_generation(
    reason: str = "Strategy Research Workspace strategy generation is forbidden",
) -> StrategyResearchSafetyResult:
    return _safety_result("strategy-research-strategy-generation-rejected", "strategy-research-workspace-safety-policy-v1", [reason], False)


def reject_research_as_backtest(reason: str = "Strategy Research Workspace backtesting is forbidden") -> StrategyResearchSafetyResult:
    return _safety_result("strategy-research-backtest-rejected", "strategy-research-workspace-safety-policy-v1", [reason], False)


def reject_research_as_recommendation(
    reason: str = "Strategy Research Workspace recommendations are forbidden",
) -> StrategyResearchSafetyResult:
    return _safety_result("strategy-research-recommendation-rejected", "strategy-research-workspace-safety-policy-v1", [reason], False)


def reject_research_as_execution_surface(
    reason: str = "Strategy Research Workspace execution surfaces are forbidden",
) -> StrategyResearchSafetyResult:
    return _safety_result("strategy-research-execution-surface-rejected", "strategy-research-workspace-safety-policy-v1", [reason], False)
