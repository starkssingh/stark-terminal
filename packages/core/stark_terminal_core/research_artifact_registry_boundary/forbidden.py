from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class ResearchArtifactRegistryBoundaryStage(StrEnum):
    BOUNDARY_HARDENING = "BOUNDARY_HARDENING"
    AUDIT_ONLY = "AUDIT_ONLY"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactForbiddenBehaviorKind(StrEnum):
    ACTIVE_INGESTION = "ACTIVE_INGESTION"
    PERSISTENT_STORAGE = "PERSISTENT_STORAGE"
    FILE_UPLOAD = "FILE_UPLOAD"
    FILE_DOWNLOAD = "FILE_DOWNLOAD"
    FILE_PREVIEW = "FILE_PREVIEW"
    ACTIVE_UI = "ACTIVE_UI"
    FRONTEND_COMPONENT = "FRONTEND_COMPONENT"
    DESKTOP_COMPONENT = "DESKTOP_COMPONENT"
    PAPER_INGESTION = "PAPER_INGESTION"
    PAPER_PARSING = "PAPER_PARSING"
    PDF_PARSING = "PDF_PARSING"
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
    EXTERNAL_CALL = "EXTERNAL_CALL"
    SECRET_OR_CREDENTIAL = "SECRET_OR_CREDENTIAL"
    PROVIDER_SDK = "PROVIDER_SDK"
    SCRAPING = "SCRAPING"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactBoundarySeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactBoundarySafetyLabel(StrEnum):
    BOUNDARY_HARDENING_ONLY = "BOUNDARY_HARDENING_ONLY"
    NOT_ACTIVE_INGESTION = "NOT_ACTIVE_INGESTION"
    NOT_PERSISTENT_STORAGE = "NOT_PERSISTENT_STORAGE"
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


def sanitize_research_artifact_boundary_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


REQUIRED_RESEARCH_ARTIFACT_FORBIDDEN_BEHAVIORS = {
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
    ResearchArtifactForbiddenBehaviorKind.PROVIDER_SDK,
    ResearchArtifactForbiddenBehaviorKind.SCRAPING,
}


class ResearchArtifactForbiddenBehavior(BaseModel):
    behavior_id: str
    kind: ResearchArtifactForbiddenBehaviorKind
    name: str
    description: str
    severity: ResearchArtifactBoundarySeverity = ResearchArtifactBoundarySeverity.BLOCKER
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("behavior_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "research artifact forbidden behavior text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_research_artifact_boundary_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def behavior_must_remain_forbidden(self) -> ResearchArtifactForbiddenBehavior:
        if self.kind == ResearchArtifactForbiddenBehaviorKind.UNKNOWN:
            raise ValueError("UNKNOWN research artifact forbidden behavior kind is not allowed")
        if self.severity == ResearchArtifactBoundarySeverity.UNKNOWN:
            raise ValueError("UNKNOWN research artifact boundary severity is not allowed")
        if not self.forbidden_now:
            raise ValueError("research artifact forbidden behavior cannot be unlocked in Prompt 75")
        if not self.requires_future_prompt:
            raise ValueError("research artifact forbidden behavior requires a future prompt before unlock")
        if not self.requires_audit_before_unlock:
            raise ValueError("research artifact forbidden behavior requires audit before unlock")
        return self


class ResearchArtifactForbiddenBehaviorRegistry(BaseModel):
    registry_id: str
    behaviors: list[ResearchArtifactForbiddenBehavior]
    complete: bool = True
    active_ingestion_allowed: bool = False
    persistent_storage_allowed: bool = False
    file_uploads_allowed: bool = False
    file_downloads_allowed: bool = False
    file_previews_allowed: bool = False
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    paper_parsing_allowed: bool = False
    pdf_parsing_allowed: bool = False
    arxiv_ingestion_allowed: bool = False
    llm_analysis_allowed: bool = False
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
        return _non_empty_text(value, "research artifact forbidden behavior registry text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def registry_must_cover_required_behaviors(self) -> ResearchArtifactForbiddenBehaviorRegistry:
        if not self.behaviors:
            raise ValueError("research artifact forbidden behavior registry requires behaviors")
        if not self.complete:
            raise ValueError("research artifact forbidden behavior registry must be complete")
        dangerous_flags = {
            "active ingestion": self.active_ingestion_allowed,
            "persistent storage": self.persistent_storage_allowed,
            "file uploads": self.file_uploads_allowed,
            "file downloads": self.file_downloads_allowed,
            "file previews": self.file_previews_allowed,
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "paper parsing": self.paper_parsing_allowed,
            "PDF parsing": self.pdf_parsing_allowed,
            "arXiv ingestion": self.arxiv_ingestion_allowed,
            "LLM analysis": self.llm_analysis_allowed,
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
            raise ValueError(f"research artifact boundary cannot allow: {', '.join(enabled)}")
        present = {behavior.kind for behavior in self.behaviors}
        missing = sorted(kind.value for kind in REQUIRED_RESEARCH_ARTIFACT_FORBIDDEN_BEHAVIORS - present)
        if missing:
            raise ValueError(
                "research artifact forbidden registry missing required kinds: " + ", ".join(missing)
            )
        return self


def default_research_artifact_forbidden_behaviors() -> list[ResearchArtifactForbiddenBehavior]:
    behavior_specs = [
        (ResearchArtifactForbiddenBehaviorKind.ACTIVE_INGESTION, "Active artifact ingestion"),
        (ResearchArtifactForbiddenBehaviorKind.PERSISTENT_STORAGE, "Persistent artifact storage"),
        (ResearchArtifactForbiddenBehaviorKind.FILE_UPLOAD, "File upload"),
        (ResearchArtifactForbiddenBehaviorKind.FILE_DOWNLOAD, "File download"),
        (ResearchArtifactForbiddenBehaviorKind.FILE_PREVIEW, "File preview"),
        (ResearchArtifactForbiddenBehaviorKind.ACTIVE_UI, "Active artifact registry UI"),
        (ResearchArtifactForbiddenBehaviorKind.FRONTEND_COMPONENT, "Frontend artifact component"),
        (ResearchArtifactForbiddenBehaviorKind.DESKTOP_COMPONENT, "Desktop artifact component"),
        (ResearchArtifactForbiddenBehaviorKind.PAPER_INGESTION, "Paper ingestion"),
        (ResearchArtifactForbiddenBehaviorKind.PAPER_PARSING, "Paper parsing"),
        (ResearchArtifactForbiddenBehaviorKind.PDF_PARSING, "PDF parsing"),
        (ResearchArtifactForbiddenBehaviorKind.ARXIV_INGESTION, "arXiv ingestion"),
        (ResearchArtifactForbiddenBehaviorKind.LLM_PAPER_ANALYSIS, "LLM paper analysis"),
        (ResearchArtifactForbiddenBehaviorKind.METHOD_EXTRACTION, "Method extraction"),
        (ResearchArtifactForbiddenBehaviorKind.STRATEGY_EXTRACTION, "Strategy extraction"),
        (ResearchArtifactForbiddenBehaviorKind.STRATEGY_GENERATION, "Strategy generation"),
        (ResearchArtifactForbiddenBehaviorKind.STRATEGY_CODE_GENERATION, "Strategy code generation"),
        (ResearchArtifactForbiddenBehaviorKind.SIGNAL_GENERATION, "Signal generation"),
        (ResearchArtifactForbiddenBehaviorKind.FACTOR_GENERATION, "Factor generation"),
        (ResearchArtifactForbiddenBehaviorKind.ALPHA_GENERATION, "Alpha generation"),
        (ResearchArtifactForbiddenBehaviorKind.BACKTESTING, "Backtesting"),
        (ResearchArtifactForbiddenBehaviorKind.OPTIMIZATION, "Optimization"),
        (ResearchArtifactForbiddenBehaviorKind.PARAMETER_SEARCH, "Parameter search"),
        (ResearchArtifactForbiddenBehaviorKind.WALK_FORWARD_ANALYSIS, "Walk-forward analysis"),
        (ResearchArtifactForbiddenBehaviorKind.PERFORMANCE_CLAIMS, "Performance claims"),
        (ResearchArtifactForbiddenBehaviorKind.RECOMMENDATION_GENERATION, "Recommendation generation"),
        (ResearchArtifactForbiddenBehaviorKind.ACTION_GENERATION, "Action generation"),
        (ResearchArtifactForbiddenBehaviorKind.CONFIDENCE_SCORING, "Confidence scoring"),
        (ResearchArtifactForbiddenBehaviorKind.DECISION_OBJECT_GENERATION, "DecisionObject generation"),
        (ResearchArtifactForbiddenBehaviorKind.READINESS_TO_TRADE, "Readiness-to-trade"),
        (ResearchArtifactForbiddenBehaviorKind.BROKER_CONTROL, "Broker control"),
        (ResearchArtifactForbiddenBehaviorKind.ORDER_BUTTON, "Order button"),
        (ResearchArtifactForbiddenBehaviorKind.EXECUTION, "Execution behavior"),
        (ResearchArtifactForbiddenBehaviorKind.APPROVAL_CONTROL, "Approval control"),
        (ResearchArtifactForbiddenBehaviorKind.OVERRIDE_CONTROL, "Override control"),
        (ResearchArtifactForbiddenBehaviorKind.EXTERNAL_CALL, "External call"),
        (ResearchArtifactForbiddenBehaviorKind.SECRET_OR_CREDENTIAL, "Secret or credential"),
        (ResearchArtifactForbiddenBehaviorKind.PROVIDER_SDK, "Provider SDK"),
        (ResearchArtifactForbiddenBehaviorKind.SCRAPING, "Scraping behavior"),
    ]
    return [
        ResearchArtifactForbiddenBehavior(
            behavior_id=f"research-artifact-{kind.value.lower().replace('_', '-')}-forbidden-v1",
            kind=kind,
            name=name,
            description=f"{name} remains forbidden by the Prompt 75 boundary-hardening layer.",
            notes=[
                "boundary-hardening-only",
                "requires future prompt",
                "requires audit before unlock",
            ],
        )
        for kind, name in behavior_specs
    ]


def default_research_artifact_forbidden_behavior_registry() -> ResearchArtifactForbiddenBehaviorRegistry:
    return ResearchArtifactForbiddenBehaviorRegistry(
        registry_id="research-artifact-forbidden-behavior-registry-v1",
        behaviors=default_research_artifact_forbidden_behaviors(),
    )
