from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry_boundary.forbidden import (
    ResearchArtifactForbiddenBehaviorKind,
    _non_empty_text,
    _utc_datetime,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


DEFAULT_RESEARCH_ARTIFACT_FORBIDDEN_ENDPOINT_OUTPUTS = [
    ResearchArtifactForbiddenBehaviorKind.ACTIVE_INGESTION,
    ResearchArtifactForbiddenBehaviorKind.PERSISTENT_STORAGE,
    ResearchArtifactForbiddenBehaviorKind.FILE_UPLOAD,
    ResearchArtifactForbiddenBehaviorKind.FILE_DOWNLOAD,
    ResearchArtifactForbiddenBehaviorKind.FILE_PREVIEW,
    ResearchArtifactForbiddenBehaviorKind.ACTIVE_UI,
    ResearchArtifactForbiddenBehaviorKind.FRONTEND_COMPONENT,
    ResearchArtifactForbiddenBehaviorKind.DESKTOP_COMPONENT,
    ResearchArtifactForbiddenBehaviorKind.PAPER_INGESTION,
    ResearchArtifactForbiddenBehaviorKind.PAPER_PARSING,
    ResearchArtifactForbiddenBehaviorKind.PDF_PARSING,
    ResearchArtifactForbiddenBehaviorKind.ARXIV_INGESTION,
    ResearchArtifactForbiddenBehaviorKind.LLM_PAPER_ANALYSIS,
    ResearchArtifactForbiddenBehaviorKind.METHOD_EXTRACTION,
    ResearchArtifactForbiddenBehaviorKind.STRATEGY_EXTRACTION,
    ResearchArtifactForbiddenBehaviorKind.STRATEGY_GENERATION,
    ResearchArtifactForbiddenBehaviorKind.STRATEGY_CODE_GENERATION,
    ResearchArtifactForbiddenBehaviorKind.SIGNAL_GENERATION,
    ResearchArtifactForbiddenBehaviorKind.FACTOR_GENERATION,
    ResearchArtifactForbiddenBehaviorKind.ALPHA_GENERATION,
    ResearchArtifactForbiddenBehaviorKind.BACKTESTING,
    ResearchArtifactForbiddenBehaviorKind.OPTIMIZATION,
    ResearchArtifactForbiddenBehaviorKind.PARAMETER_SEARCH,
    ResearchArtifactForbiddenBehaviorKind.WALK_FORWARD_ANALYSIS,
    ResearchArtifactForbiddenBehaviorKind.PERFORMANCE_CLAIMS,
    ResearchArtifactForbiddenBehaviorKind.RECOMMENDATION_GENERATION,
    ResearchArtifactForbiddenBehaviorKind.ACTION_GENERATION,
    ResearchArtifactForbiddenBehaviorKind.CONFIDENCE_SCORING,
    ResearchArtifactForbiddenBehaviorKind.DECISION_OBJECT_GENERATION,
    ResearchArtifactForbiddenBehaviorKind.READINESS_TO_TRADE,
    ResearchArtifactForbiddenBehaviorKind.BROKER_CONTROL,
    ResearchArtifactForbiddenBehaviorKind.ORDER_BUTTON,
    ResearchArtifactForbiddenBehaviorKind.EXECUTION,
    ResearchArtifactForbiddenBehaviorKind.APPROVAL_CONTROL,
    ResearchArtifactForbiddenBehaviorKind.OVERRIDE_CONTROL,
    ResearchArtifactForbiddenBehaviorKind.EXTERNAL_CALL,
    ResearchArtifactForbiddenBehaviorKind.SECRET_OR_CREDENTIAL,
]


class ResearchArtifactEndpointBoundaryPolicy(BaseModel):
    policy_id: str
    endpoint_family: str
    allowed_methods: list[str]
    forbidden_methods: list[str]
    forbidden_outputs: list[ResearchArtifactForbiddenBehaviorKind]
    read_only: bool = True
    unavailable_by_default: bool = True
    accepts_file_input: bool = False
    accepts_artifact_input_for_storage: bool = False
    accepts_paper_input: bool = False
    accepts_market_data_for_research_decision: bool = False
    generates_active_ui: bool = False
    ingests_artifact: bool = False
    stores_artifact: bool = False
    uploads_file: bool = False
    downloads_file: bool = False
    previews_file: bool = False
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
        return _non_empty_text(value, "research artifact endpoint boundary policy text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def endpoint_policy_must_fail_closed(self) -> ResearchArtifactEndpointBoundaryPolicy:
        if not self.allowed_methods:
            raise ValueError("research artifact endpoint boundary policy requires allowed methods")
        if any(not method.strip() for method in self.allowed_methods):
            raise ValueError("research artifact endpoint allowed methods cannot be empty")
        if not self.forbidden_outputs:
            raise ValueError("research artifact endpoint boundary policy requires forbidden outputs")
        if ResearchArtifactForbiddenBehaviorKind.UNKNOWN in self.forbidden_outputs:
            raise ValueError("UNKNOWN research artifact forbidden endpoint output is not allowed")
        if not self.read_only:
            raise ValueError("research artifact endpoint boundary policies must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("research artifact endpoint boundary policies must be unavailable by default")
        dangerous_flags = {
            "file input": self.accepts_file_input,
            "artifact input for storage": self.accepts_artifact_input_for_storage,
            "paper input": self.accepts_paper_input,
            "market data for research decision": self.accepts_market_data_for_research_decision,
            "active UI": self.generates_active_ui,
            "artifact ingestion": self.ingests_artifact,
            "artifact storage": self.stores_artifact,
            "file upload": self.uploads_file,
            "file download": self.downloads_file,
            "file preview": self.previews_file,
            "paper parsing": self.parses_paper,
            "strategy generation": self.generates_strategy,
            "backtesting": self.generates_backtest,
            "recommendation generation": self.generates_recommendation,
            "DecisionObject generation": self.generates_decision_object,
            "broker controls": self.exposes_broker_controls,
            "execution": self.executes_trade,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact endpoint boundary cannot allow: {', '.join(enabled)}")
        return self


def _endpoint_policy(endpoint_family: str) -> ResearchArtifactEndpointBoundaryPolicy:
    return ResearchArtifactEndpointBoundaryPolicy(
        policy_id=f"{endpoint_family}-boundary-policy-v1",
        endpoint_family=endpoint_family,
        allowed_methods=["GET"],
        forbidden_methods=["POST", "PUT", "PATCH", "DELETE"],
        forbidden_outputs=list(DEFAULT_RESEARCH_ARTIFACT_FORBIDDEN_ENDPOINT_OUTPUTS),
    )


def default_research_artifact_endpoint_boundary_policies() -> list[
    ResearchArtifactEndpointBoundaryPolicy
]:
    return [
        _endpoint_policy("research-artifact-registry"),
        _endpoint_policy("research-artifact-registry-api"),
        _endpoint_policy("research-artifact-registry-display"),
        _endpoint_policy("research-artifact-registry-boundary"),
    ]


def evaluate_research_artifact_endpoint_boundary_policies(
    policies: list[ResearchArtifactEndpointBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_research_artifact_endpoint_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if not policy.read_only:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not read-only")
        if not policy.unavailable_by_default:
            blockers.append(f"{policy.endpoint_family}: endpoint policy is not unavailable by default")
        if policy.accepts_file_input:
            blockers.append(f"{policy.endpoint_family}: accepts file input")
        if policy.accepts_artifact_input_for_storage:
            blockers.append(f"{policy.endpoint_family}: accepts artifact input for storage")
        if policy.accepts_paper_input:
            blockers.append(f"{policy.endpoint_family}: accepts paper input")
        if policy.accepts_market_data_for_research_decision:
            blockers.append(f"{policy.endpoint_family}: accepts market data for research decision")
        if policy.generates_active_ui:
            blockers.append(f"{policy.endpoint_family}: generates active UI")
        if policy.ingests_artifact:
            blockers.append(f"{policy.endpoint_family}: ingests artifacts")
        if policy.stores_artifact:
            blockers.append(f"{policy.endpoint_family}: stores artifacts")
        if policy.uploads_file:
            blockers.append(f"{policy.endpoint_family}: uploads files")
        if policy.downloads_file:
            blockers.append(f"{policy.endpoint_family}: downloads files")
        if policy.previews_file:
            blockers.append(f"{policy.endpoint_family}: previews files")
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
            blockers.append(f"{policy.endpoint_family}: executes trades")
    return blockers
