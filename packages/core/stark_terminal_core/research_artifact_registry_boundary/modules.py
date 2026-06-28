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


DEFAULT_RESEARCH_ARTIFACT_FORBIDDEN_MODULE_BEHAVIORS = [
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
]


class ResearchArtifactModuleBoundaryPolicy(BaseModel):
    policy_id: str
    module_family: str
    allowed_purpose: str
    forbidden_behaviors: list[ResearchArtifactForbiddenBehaviorKind]
    may_ingest_artifacts: bool = False
    may_persist_artifacts: bool = False
    may_upload_files: bool = False
    may_download_files: bool = False
    may_preview_files: bool = False
    may_create_active_ui: bool = False
    may_create_frontend_components: bool = False
    may_create_desktop_components: bool = False
    may_parse_papers: bool = False
    may_parse_pdfs: bool = False
    may_ingest_arxiv: bool = False
    may_call_llm_analysis: bool = False
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
        return _non_empty_text(value, "research artifact module boundary policy text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def module_policy_must_fail_closed(self) -> ResearchArtifactModuleBoundaryPolicy:
        if not self.forbidden_behaviors:
            raise ValueError("research artifact module boundary policy requires forbidden behaviors")
        if ResearchArtifactForbiddenBehaviorKind.UNKNOWN in self.forbidden_behaviors:
            raise ValueError("UNKNOWN research artifact forbidden behavior is not allowed")
        dangerous_flags = {
            "artifact ingestion": self.may_ingest_artifacts,
            "artifact persistence": self.may_persist_artifacts,
            "file upload": self.may_upload_files,
            "file download": self.may_download_files,
            "file preview": self.may_preview_files,
            "active UI": self.may_create_active_ui,
            "frontend components": self.may_create_frontend_components,
            "desktop components": self.may_create_desktop_components,
            "paper parsing": self.may_parse_papers,
            "PDF parsing": self.may_parse_pdfs,
            "arXiv ingestion": self.may_ingest_arxiv,
            "LLM analysis": self.may_call_llm_analysis,
            "strategy generation": self.may_generate_strategies,
            "strategy code generation": self.may_generate_strategy_code,
            "backtesting": self.may_run_backtests,
            "optimization": self.may_optimize,
            "recommendations": self.may_generate_recommendations,
            "actions": self.may_generate_actions,
            "confidence scoring": self.may_score_confidence,
            "DecisionObjects": self.may_generate_decision_objects,
            "readiness-to-trade": self.may_generate_readiness_to_trade,
            "broker controls": self.may_expose_broker_controls,
            "execution": self.may_execute,
            "approval": self.may_grant_approval,
            "override": self.may_grant_override,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact modules may not allow: {', '.join(enabled)}")
        return self


def _module_policy(module_family: str, allowed_purpose: str) -> ResearchArtifactModuleBoundaryPolicy:
    return ResearchArtifactModuleBoundaryPolicy(
        policy_id=f"{module_family.replace('_', '-')}-boundary-policy-v1",
        module_family=module_family,
        allowed_purpose=allowed_purpose,
        forbidden_behaviors=list(DEFAULT_RESEARCH_ARTIFACT_FORBIDDEN_MODULE_BEHAVIORS),
    )


def default_research_artifact_module_boundary_policies() -> list[
    ResearchArtifactModuleBoundaryPolicy
]:
    return [
        _module_policy("research_artifact_registry", "planning and guardrail placeholders only"),
        _module_policy("research_artifact_registry_api", "API contract skeleton placeholders only"),
        _module_policy("research_artifact_registry_display", "display contract skeleton placeholders only"),
        _module_policy(
            "research_artifact_registry_boundary",
            "boundary-hardening contracts and invariant helpers only",
        ),
    ]


def evaluate_research_artifact_module_boundary_policies(
    policies: list[ResearchArtifactModuleBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_research_artifact_module_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if policy.may_ingest_artifacts:
            blockers.append(f"{policy.module_family}: may ingest artifacts")
        if policy.may_persist_artifacts:
            blockers.append(f"{policy.module_family}: may persist artifacts")
        if policy.may_upload_files:
            blockers.append(f"{policy.module_family}: may upload files")
        if policy.may_download_files:
            blockers.append(f"{policy.module_family}: may download files")
        if policy.may_preview_files:
            blockers.append(f"{policy.module_family}: may preview files")
        if policy.may_create_active_ui:
            blockers.append(f"{policy.module_family}: may create active UI")
        if policy.may_create_frontend_components:
            blockers.append(f"{policy.module_family}: may create frontend components")
        if policy.may_create_desktop_components:
            blockers.append(f"{policy.module_family}: may create desktop components")
        if policy.may_parse_papers:
            blockers.append(f"{policy.module_family}: may parse papers")
        if policy.may_parse_pdfs:
            blockers.append(f"{policy.module_family}: may parse PDFs")
        if policy.may_ingest_arxiv:
            blockers.append(f"{policy.module_family}: may ingest arXiv")
        if policy.may_call_llm_analysis:
            blockers.append(f"{policy.module_family}: may call LLM analysis")
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
