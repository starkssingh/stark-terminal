from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_display.artifacts import (
    StrategyResearchWorkspaceDisplayArtifactPlaceholder,
)
from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayContractMetadata,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_display_notes,
)
from stark_terminal_core.strategy_research_workspace_display.experiments import (
    StrategyResearchWorkspaceDisplayExperimentPlaceholder,
)
from stark_terminal_core.strategy_research_workspace_display.hypotheses import (
    StrategyResearchWorkspaceDisplayHypothesisPlaceholder,
)
from stark_terminal_core.strategy_research_workspace_display.papers import (
    StrategyResearchWorkspaceDisplayPaperPlaceholder,
)
from stark_terminal_core.strategy_research_workspace_display.workspaces import (
    StrategyResearchWorkspaceDisplayWorkspacePlaceholder,
)


class StrategyResearchWorkspaceDisplaySafetyPolicy(BaseModel):
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
    require_display_contract_only: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace display safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_display_notes(value)

    @model_validator(mode="after")
    def safety_policy_must_fail_closed(self) -> StrategyResearchWorkspaceDisplaySafetyPolicy:
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
            raise ValueError("Strategy Research Workspace Display safety policy cannot allow: " + ", ".join(enabled))
        if not self.require_display_contract_only:
            raise ValueError("Strategy Research Workspace Display must require display-contract-only behavior")
        return self


class StrategyResearchWorkspaceDisplaySafetyResult(BaseModel):
    result_id: str
    policy_id: str
    safe: bool
    reasons: list[str]
    display_contract_only: bool = True
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
        return _non_empty_text(value, "strategy research workspace display safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_strategy_research_workspace_display_notes(value)
        if not sanitized:
            raise ValueError("Strategy Research Workspace Display safety result reasons cannot be empty")
        return sanitized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def safety_result_must_fail_closed(self) -> StrategyResearchWorkspaceDisplaySafetyResult:
        if not self.display_contract_only:
            raise ValueError("Strategy Research Workspace Display safety result must remain display-contract-only")
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
            raise ValueError("Strategy Research Workspace Display safety result cannot allow: " + ", ".join(enabled))
        return self


def default_strategy_research_workspace_display_safety_policy(
    settings: Any | None = None,
) -> StrategyResearchWorkspaceDisplaySafetyPolicy:
    notes = ["Prompt 65 permits Strategy Research Workspace Display contract skeleton only."]
    if settings is not None:
        notes.append(f"stage={settings.strategy_research_workspace_display_stage}")
    return StrategyResearchWorkspaceDisplaySafetyPolicy(
        policy_id="strategy-research-workspace-display-safety-policy-v1",
        name="Strategy Research Workspace Display Safety Policy",
        notes=notes,
    )


def _safety_result(
    result_id: str,
    policy_id: str,
    reasons: list[str],
    safe: bool,
) -> StrategyResearchWorkspaceDisplaySafetyResult:
    return StrategyResearchWorkspaceDisplaySafetyResult(
        result_id=result_id,
        policy_id=policy_id,
        reasons=reasons,
        safe=safe,
    )


def _unsafe_policy_reasons(policy: StrategyResearchWorkspaceDisplaySafetyPolicy) -> list[str]:
    reasons: list[str] = []
    for label, flag in [
        ("active UI", policy.allow_active_ui),
        ("frontend components", policy.allow_frontend_components),
        ("desktop components", policy.allow_desktop_components),
        ("paper ingestion", policy.allow_paper_ingestion),
        ("paper parsing", policy.allow_paper_parsing),
        ("strategy generation", policy.allow_strategy_generation),
        ("strategy code generation", policy.allow_strategy_code_generation),
        ("backtesting", policy.allow_backtesting),
        ("optimization", policy.allow_optimization),
        ("recommendations", policy.allow_recommendations),
        ("action generation", policy.allow_action_generation),
        ("confidence scoring", policy.allow_confidence_scoring),
        ("DecisionObject generation", policy.allow_decision_object_generation),
        ("readiness-to-trade", policy.allow_readiness_to_trade),
        ("broker controls", policy.allow_broker_controls),
        ("execution", policy.allow_execution),
        ("approval", policy.allow_approval),
        ("override", policy.allow_override),
    ]:
        if flag:
            reasons.append(f"Strategy Research Workspace Display policy cannot allow {label}")
    if not policy.require_display_contract_only:
        reasons.append("Strategy Research Workspace Display policy must require display-contract-only behavior")
    return reasons


def evaluate_strategy_research_display_contract_safety(
    contract: StrategyResearchWorkspaceDisplayContractMetadata,
    policy: StrategyResearchWorkspaceDisplaySafetyPolicy,
) -> StrategyResearchWorkspaceDisplaySafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    for label, flag in [
        ("active UI", getattr(contract, "active_ui_allowed", False)),
        ("frontend components", getattr(contract, "frontend_components_allowed", False)),
        ("desktop components", getattr(contract, "desktop_components_allowed", False)),
        ("paper ingestion", getattr(contract, "paper_ingestion_allowed", False)),
        ("paper parsing", getattr(contract, "paper_parsing_allowed", False)),
        ("strategy generation", getattr(contract, "strategy_generation_allowed", False)),
        ("strategy code generation", getattr(contract, "strategy_code_generation_allowed", False)),
        ("backtesting", getattr(contract, "backtesting_allowed", False)),
        ("optimization", getattr(contract, "optimization_allowed", False)),
        ("recommendations", getattr(contract, "recommendations_allowed", False)),
        ("action generation", getattr(contract, "action_generation_allowed", False)),
        ("confidence scoring", getattr(contract, "confidence_scoring_allowed", False)),
        ("DecisionObject generation", getattr(contract, "decision_object_generation_allowed", False)),
        ("readiness-to-trade", getattr(contract, "readiness_to_trade_allowed", False)),
        ("broker controls", getattr(contract, "broker_controls_allowed", False)),
        ("execution", getattr(contract, "execution_allowed", False)),
        ("approval", getattr(contract, "approval_allowed", False)),
        ("override", getattr(contract, "override_allowed", False)),
    ]:
        if flag:
            reasons.append(f"Strategy Research Workspace Display contract cannot allow {label}")
    if not getattr(contract, "returns_unavailable_by_default", False):
        reasons.append("Strategy Research Workspace Display contract must return unavailable by default")
    if reasons:
        return _safety_result("strategy-research-display-contract-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-display-contract-safety-safe",
        policy.policy_id,
        ["Strategy Research Workspace Display contract remains display-contract-only"],
        True,
    )


def evaluate_strategy_research_display_workspace_safety(
    workspaces: Iterable[StrategyResearchWorkspaceDisplayWorkspacePlaceholder],
    policy: StrategyResearchWorkspaceDisplaySafetyPolicy,
) -> StrategyResearchWorkspaceDisplaySafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    workspace_list = list(workspaces)
    if not workspace_list:
        reasons.append("Strategy Research Workspace Display workspace placeholders are required")
    for workspace in workspace_list:
        if not getattr(workspace, "display_contract_only", False):
            reasons.append(f"{workspace.workspace_id} must remain display-contract-only")
        if getattr(workspace, "active_ui", False) or getattr(workspace, "rendered_now", False):
            reasons.append(f"{workspace.workspace_id} cannot be active or rendered")
        if not getattr(workspace, "unavailable", False):
            reasons.append(f"{workspace.workspace_id} must remain unavailable")
        for label in [
            "paper_ingestion_allowed",
            "paper_parsing_allowed",
            "strategy_generation_allowed",
            "backtesting_allowed",
            "recommendations_allowed",
            "execution_allowed",
        ]:
            if getattr(workspace, label, False):
                reasons.append(f"{workspace.workspace_id} cannot enable {label}")
    if reasons:
        return _safety_result("strategy-research-display-workspace-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-display-workspace-safety-safe",
        policy.policy_id,
        ["Workspace visual placeholders remain unavailable display contracts"],
        True,
    )


def evaluate_strategy_research_display_artifact_safety(
    artifacts: Iterable[StrategyResearchWorkspaceDisplayArtifactPlaceholder],
    policy: StrategyResearchWorkspaceDisplaySafetyPolicy,
) -> StrategyResearchWorkspaceDisplaySafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    artifact_list = list(artifacts)
    if not artifact_list:
        reasons.append("Strategy Research Workspace Display artifact placeholders are required")
    for artifact in artifact_list:
        if not getattr(artifact, "display_contract_only", False):
            reasons.append(f"{artifact.artifact_id} must remain display-contract-only")
        for label in [
            "rendered_now",
            "validated",
            "strategy_ready",
            "recommendation_ready",
            "execution_ready",
            "paper_parsed",
            "backtest_ready",
        ]:
            if getattr(artifact, label, False):
                reasons.append(f"{artifact.artifact_id} cannot enable {label}")
    if reasons:
        return _safety_result("strategy-research-display-artifact-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-display-artifact-safety-safe",
        policy.policy_id,
        ["Artifact visual placeholders remain unavailable display contracts"],
        True,
    )


def evaluate_strategy_research_display_paper_safety(
    papers: Iterable[StrategyResearchWorkspaceDisplayPaperPlaceholder],
    policy: StrategyResearchWorkspaceDisplaySafetyPolicy,
) -> StrategyResearchWorkspaceDisplaySafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    paper_list = list(papers)
    if not paper_list:
        reasons.append("Strategy Research Workspace Display paper placeholders are required")
    for paper in paper_list:
        for label in [
            "rendered_now",
            "paper_ingested",
            "paper_parsed",
            "method_extracted",
            "strategy_extracted",
            "code_generated",
            "backtest_generated",
            "recommendation_generated",
        ]:
            if getattr(paper, label, False):
                reasons.append(f"{paper.paper_reference_id} cannot enable {label}")
    if reasons:
        return _safety_result("strategy-research-display-paper-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-display-paper-safety-safe",
        policy.policy_id,
        ["Paper visual placeholders remain unparsed display contracts"],
        True,
    )


def evaluate_strategy_research_display_hypothesis_safety(
    hypotheses: Iterable[StrategyResearchWorkspaceDisplayHypothesisPlaceholder],
    policy: StrategyResearchWorkspaceDisplaySafetyPolicy,
) -> StrategyResearchWorkspaceDisplaySafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    hypothesis_list = list(hypotheses)
    if not hypothesis_list:
        reasons.append("Strategy Research Workspace Display hypothesis placeholders are required")
    for hypothesis in hypothesis_list:
        for label in [
            "rendered_now",
            "generated_strategy",
            "generated_signal",
            "generated_factor",
            "generated_code",
            "backtest_ready",
            "recommendation_ready",
            "execution_ready",
        ]:
            if getattr(hypothesis, label, False):
                reasons.append(f"{hypothesis.hypothesis_id} cannot enable {label}")
    if reasons:
        return _safety_result("strategy-research-display-hypothesis-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-display-hypothesis-safety-safe",
        policy.policy_id,
        ["Hypothesis visual placeholders remain non-generated display contracts"],
        True,
    )


def evaluate_strategy_research_display_experiment_safety(
    experiments: Iterable[StrategyResearchWorkspaceDisplayExperimentPlaceholder],
    policy: StrategyResearchWorkspaceDisplaySafetyPolicy,
) -> StrategyResearchWorkspaceDisplaySafetyResult:
    reasons = _unsafe_policy_reasons(policy)
    experiment_list = list(experiments)
    if not experiment_list:
        reasons.append("Strategy Research Workspace Display experiment placeholders are required")
    for experiment in experiment_list:
        for label in [
            "rendered_now",
            "executable",
            "backtest_executable",
            "optimization_executable",
            "strategy_executable",
            "live_ready",
            "recommendation_ready",
            "execution_ready",
        ]:
            if getattr(experiment, label, False):
                reasons.append(f"{experiment.experiment_id} cannot enable {label}")
    if reasons:
        return _safety_result("strategy-research-display-experiment-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "strategy-research-display-experiment-safety-safe",
        policy.policy_id,
        ["Experiment visual placeholders remain non-executable display contracts"],
        True,
    )


def reject_display_as_active_ui() -> StrategyResearchWorkspaceDisplaySafetyResult:
    return _safety_result(
        "strategy-research-display-active-ui-rejected",
        "strategy-research-workspace-display-safety-policy-v1",
        ["Strategy Research Workspace Display cannot be treated as active UI in Prompt 65"],
        False,
    )


def reject_display_as_strategy_generation() -> StrategyResearchWorkspaceDisplaySafetyResult:
    return _safety_result(
        "strategy-research-display-strategy-generation-rejected",
        "strategy-research-workspace-display-safety-policy-v1",
        ["Strategy Research Workspace Display cannot generate strategies in Prompt 65"],
        False,
    )


def reject_display_as_backtest() -> StrategyResearchWorkspaceDisplaySafetyResult:
    return _safety_result(
        "strategy-research-display-backtest-rejected",
        "strategy-research-workspace-display-safety-policy-v1",
        ["Strategy Research Workspace Display cannot run or display active backtests in Prompt 65"],
        False,
    )


def reject_display_as_recommendation() -> StrategyResearchWorkspaceDisplaySafetyResult:
    return _safety_result(
        "strategy-research-display-recommendation-rejected",
        "strategy-research-workspace-display-safety-policy-v1",
        ["Strategy Research Workspace Display cannot be treated as a recommendation in Prompt 65"],
        False,
    )


def reject_display_as_execution_surface() -> StrategyResearchWorkspaceDisplaySafetyResult:
    return _safety_result(
        "strategy-research-display-execution-rejected",
        "strategy-research-workspace-display-safety-policy-v1",
        ["Strategy Research Workspace Display cannot be treated as execution, broker, approval, or override surface"],
        False,
    )
