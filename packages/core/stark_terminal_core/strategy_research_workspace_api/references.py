from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_api.requests import (
    _non_empty_text,
    _utc_datetime,
    _utc_now,
)


def _optional_trimmed(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


class StrategyResearchWorkspaceAPIWorkspaceReference(BaseModel):
    reference_id: str
    workspace_id: str | None = None
    required: bool = False
    active_workspace: bool = False
    active_ui: bool = False
    paper_ingestion_available: bool = False
    paper_parsing_available: bool = False
    strategy_generation_available: bool = False
    backtesting_available: bool = False
    recommendation_available: bool = False
    execution_available: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API workspace reference text fields")

    @field_validator("workspace_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def workspace_reference_must_fail_closed(self) -> StrategyResearchWorkspaceAPIWorkspaceReference:
        if self.active_workspace:
            raise ValueError("Strategy Research Workspace API workspace reference cannot be active")
        if self.active_ui:
            raise ValueError("Strategy Research Workspace API workspace reference cannot expose active UI")
        if self.paper_ingestion_available:
            raise ValueError("Strategy Research Workspace API workspace reference cannot expose paper ingestion")
        if self.paper_parsing_available:
            raise ValueError("Strategy Research Workspace API workspace reference cannot expose paper parsing")
        if self.strategy_generation_available:
            raise ValueError("Strategy Research Workspace API workspace reference cannot expose strategies")
        if self.backtesting_available:
            raise ValueError("Strategy Research Workspace API workspace reference cannot expose backtesting")
        if self.recommendation_available:
            raise ValueError("Strategy Research Workspace API workspace reference cannot expose recommendations")
        if self.execution_available:
            raise ValueError("Strategy Research Workspace API workspace reference cannot expose execution")
        if self.display_ready:
            raise ValueError("Strategy Research Workspace API workspace reference cannot be display-ready")
        return self


class StrategyResearchWorkspaceAPIArtifactReference(BaseModel):
    reference_id: str
    artifact_id: str | None = None
    required: bool = False
    validated_artifact: bool = False
    parsed_paper_artifact: bool = False
    strategy_ready_artifact: bool = False
    backtest_ready_artifact: bool = False
    recommendation_ready_artifact: bool = False
    execution_ready_artifact: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API artifact reference text fields")

    @field_validator("artifact_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def artifact_reference_must_fail_closed(self) -> StrategyResearchWorkspaceAPIArtifactReference:
        if self.validated_artifact:
            raise ValueError("Strategy Research Workspace API artifact reference cannot be validated")
        if self.parsed_paper_artifact:
            raise ValueError("Strategy Research Workspace API artifact reference cannot be a parsed paper")
        if self.strategy_ready_artifact:
            raise ValueError("Strategy Research Workspace API artifact reference cannot be strategy-ready")
        if self.backtest_ready_artifact:
            raise ValueError("Strategy Research Workspace API artifact reference cannot be backtest-ready")
        if self.recommendation_ready_artifact:
            raise ValueError("Strategy Research Workspace API artifact reference cannot be recommendation-ready")
        if self.execution_ready_artifact:
            raise ValueError("Strategy Research Workspace API artifact reference cannot be execution-ready")
        if self.display_ready:
            raise ValueError("Strategy Research Workspace API artifact reference cannot be display-ready")
        return self


class StrategyResearchWorkspaceAPIPaperReference(BaseModel):
    reference_id: str
    paper_reference_id: str | None = None
    required: bool = False
    paper_ingested: bool = False
    paper_parsed: bool = False
    method_extracted: bool = False
    strategy_extracted: bool = False
    code_generated: bool = False
    backtest_generated: bool = False
    recommendation_generated: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API paper reference text fields")

    @field_validator("paper_reference_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def paper_reference_must_fail_closed(self) -> StrategyResearchWorkspaceAPIPaperReference:
        if self.paper_ingested:
            raise ValueError("Strategy Research Workspace API paper reference cannot be ingested")
        if self.paper_parsed:
            raise ValueError("Strategy Research Workspace API paper reference cannot be parsed")
        if self.method_extracted:
            raise ValueError("Strategy Research Workspace API paper reference cannot extract methods")
        if self.strategy_extracted:
            raise ValueError("Strategy Research Workspace API paper reference cannot extract strategies")
        if self.code_generated:
            raise ValueError("Strategy Research Workspace API paper reference cannot generate code")
        if self.backtest_generated:
            raise ValueError("Strategy Research Workspace API paper reference cannot generate backtests")
        if self.recommendation_generated:
            raise ValueError("Strategy Research Workspace API paper reference cannot generate recommendations")
        if self.display_ready:
            raise ValueError("Strategy Research Workspace API paper reference cannot be display-ready")
        return self


class StrategyResearchWorkspaceAPIHypothesisReference(BaseModel):
    reference_id: str
    hypothesis_id: str | None = None
    required: bool = False
    generated_strategy: bool = False
    generated_signal: bool = False
    generated_factor: bool = False
    generated_code: bool = False
    backtest_ready: bool = False
    recommendation_ready: bool = False
    execution_ready: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API hypothesis reference text fields")

    @field_validator("hypothesis_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def hypothesis_reference_must_fail_closed(self) -> StrategyResearchWorkspaceAPIHypothesisReference:
        if self.generated_strategy:
            raise ValueError("Strategy Research Workspace API hypothesis reference cannot generate strategies")
        if self.generated_signal:
            raise ValueError("Strategy Research Workspace API hypothesis reference cannot generate signals")
        if self.generated_factor:
            raise ValueError("Strategy Research Workspace API hypothesis reference cannot generate factors")
        if self.generated_code:
            raise ValueError("Strategy Research Workspace API hypothesis reference cannot generate code")
        if self.backtest_ready:
            raise ValueError("Strategy Research Workspace API hypothesis reference cannot be backtest-ready")
        if self.recommendation_ready:
            raise ValueError("Strategy Research Workspace API hypothesis reference cannot be recommendation-ready")
        if self.execution_ready:
            raise ValueError("Strategy Research Workspace API hypothesis reference cannot be execution-ready")
        if self.display_ready:
            raise ValueError("Strategy Research Workspace API hypothesis reference cannot be display-ready")
        return self


class StrategyResearchWorkspaceAPIDatasetReference(BaseModel):
    reference_id: str
    dataset_reference_id: str | None = None
    required: bool = False
    real_market_data: bool = False
    live_data: bool = False
    validated_for_research: bool = False
    validated_for_backtest: bool = False
    validated_for_execution: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API dataset reference text fields")

    @field_validator("dataset_reference_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def dataset_reference_must_fail_closed(self) -> StrategyResearchWorkspaceAPIDatasetReference:
        if self.real_market_data:
            raise ValueError("Strategy Research Workspace API dataset reference cannot claim real market data")
        if self.live_data:
            raise ValueError("Strategy Research Workspace API dataset reference cannot claim live data")
        if self.validated_for_research:
            raise ValueError("Strategy Research Workspace API dataset reference cannot be research-validated")
        if self.validated_for_backtest:
            raise ValueError("Strategy Research Workspace API dataset reference cannot be backtest-validated")
        if self.validated_for_execution:
            raise ValueError("Strategy Research Workspace API dataset reference cannot be execution-validated")
        if self.display_ready:
            raise ValueError("Strategy Research Workspace API dataset reference cannot be display-ready")
        return self


class StrategyResearchWorkspaceAPIExperimentReference(BaseModel):
    reference_id: str
    experiment_id: str | None = None
    required: bool = False
    executable: bool = False
    backtest_executable: bool = False
    optimization_executable: bool = False
    strategy_executable: bool = False
    live_ready: bool = False
    recommendation_ready: bool = False
    execution_ready: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API experiment reference text fields")

    @field_validator("experiment_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def experiment_reference_must_fail_closed(self) -> StrategyResearchWorkspaceAPIExperimentReference:
        if self.executable:
            raise ValueError("Strategy Research Workspace API experiment reference cannot be executable")
        if self.backtest_executable:
            raise ValueError("Strategy Research Workspace API experiment reference cannot execute backtests")
        if self.optimization_executable:
            raise ValueError("Strategy Research Workspace API experiment reference cannot execute optimization")
        if self.strategy_executable:
            raise ValueError("Strategy Research Workspace API experiment reference cannot execute strategies")
        if self.live_ready:
            raise ValueError("Strategy Research Workspace API experiment reference cannot be live-ready")
        if self.recommendation_ready:
            raise ValueError("Strategy Research Workspace API experiment reference cannot be recommendation-ready")
        if self.execution_ready:
            raise ValueError("Strategy Research Workspace API experiment reference cannot be execution-ready")
        if self.display_ready:
            raise ValueError("Strategy Research Workspace API experiment reference cannot be display-ready")
        return self


class StrategyResearchWorkspaceAPISafetyReference(BaseModel):
    reference_id: str
    boundary_policy_id: str | None = None
    required: bool = True
    safety_passed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace API safety reference text fields")

    @field_validator("boundary_policy_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def safety_reference_must_fail_closed(self) -> StrategyResearchWorkspaceAPISafetyReference:
        if self.safety_passed:
            raise ValueError("Strategy Research Workspace API safety reference cannot pass in Prompt 64")
        if self.approval_granted:
            raise ValueError("Strategy Research Workspace API safety reference cannot grant approval")
        if self.override_granted:
            raise ValueError("Strategy Research Workspace API safety reference cannot grant override")
        if self.readiness_to_trade_allowed:
            raise ValueError("Strategy Research Workspace API safety reference cannot allow readiness-to-trade")
        if self.broker_controls_allowed:
            raise ValueError("Strategy Research Workspace API safety reference cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("Strategy Research Workspace API safety reference cannot allow execution")
        return self


def default_strategy_research_workspace_api_workspace_reference() -> (
    StrategyResearchWorkspaceAPIWorkspaceReference
):
    return StrategyResearchWorkspaceAPIWorkspaceReference(
        reference_id="strategy-research-workspace-api-workspace-reference-v1",
        workspace_id="strategy-research-workspace-placeholder-reference",
    )


def default_strategy_research_workspace_api_artifact_reference() -> (
    StrategyResearchWorkspaceAPIArtifactReference
):
    return StrategyResearchWorkspaceAPIArtifactReference(
        reference_id="strategy-research-workspace-api-artifact-reference-v1",
        artifact_id="strategy-research-artifact-placeholder-reference",
    )


def default_strategy_research_workspace_api_paper_reference() -> StrategyResearchWorkspaceAPIPaperReference:
    return StrategyResearchWorkspaceAPIPaperReference(
        reference_id="strategy-research-workspace-api-paper-reference-v1",
        paper_reference_id="strategy-research-paper-placeholder-reference",
    )


def default_strategy_research_workspace_api_hypothesis_reference() -> (
    StrategyResearchWorkspaceAPIHypothesisReference
):
    return StrategyResearchWorkspaceAPIHypothesisReference(
        reference_id="strategy-research-workspace-api-hypothesis-reference-v1",
        hypothesis_id="strategy-research-hypothesis-placeholder-reference",
    )


def default_strategy_research_workspace_api_dataset_reference() -> (
    StrategyResearchWorkspaceAPIDatasetReference
):
    return StrategyResearchWorkspaceAPIDatasetReference(
        reference_id="strategy-research-workspace-api-dataset-reference-v1",
        dataset_reference_id="strategy-research-dataset-placeholder-reference",
    )


def default_strategy_research_workspace_api_experiment_reference() -> (
    StrategyResearchWorkspaceAPIExperimentReference
):
    return StrategyResearchWorkspaceAPIExperimentReference(
        reference_id="strategy-research-workspace-api-experiment-reference-v1",
        experiment_id="strategy-research-experiment-placeholder-reference",
    )


def default_strategy_research_workspace_api_safety_reference() -> StrategyResearchWorkspaceAPISafetyReference:
    return StrategyResearchWorkspaceAPISafetyReference(
        reference_id="strategy-research-workspace-api-safety-reference-v1",
        boundary_policy_id="strategy-research-workspace-api-boundary-policy-v1",
    )
