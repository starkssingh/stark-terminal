from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index_boundary.forbidden import (
    ResearchArtifactIndexForbiddenBehaviorKind,
    _non_empty_text,
    _utc_datetime,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


DEFAULT_INDEX_MODULE_FORBIDDEN_BEHAVIORS = [
    kind
    for kind in ResearchArtifactIndexForbiddenBehaviorKind
    if kind != ResearchArtifactIndexForbiddenBehaviorKind.UNKNOWN
]


class ResearchArtifactIndexModuleBoundaryPolicy(BaseModel):
    policy_id: str
    module_family: str
    allowed_purpose: str
    forbidden_behaviors: list[ResearchArtifactIndexForbiddenBehaviorKind]
    may_make_external_calls: bool = False
    may_write_persistent_state: bool = False
    may_create_active_ui: bool = False
    may_create_frontend_components: bool = False
    may_create_desktop_components: bool = False
    may_index_search_rank_retrieve: bool = False
    may_embed_or_use_vector_store: bool = False
    may_ingest_or_store: bool = False
    may_upload_download_preview: bool = False
    may_parse_papers: bool = False
    may_generate_strategy_or_backtest: bool = False
    may_generate_recommendations: bool = False
    may_generate_actions_or_confidence: bool = False
    may_generate_decision_objects: bool = False
    may_generate_readiness_to_trade: bool = False
    may_expose_broker_controls: bool = False
    may_approve_or_override: bool = False
    may_execute: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("policy_id", "module_family", "allowed_purpose", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "research artifact index module policy text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def module_policy_must_be_safe(self) -> ResearchArtifactIndexModuleBoundaryPolicy:
        if not self.forbidden_behaviors:
            raise ValueError("research artifact index module policy requires forbidden behaviors")
        if ResearchArtifactIndexForbiddenBehaviorKind.UNKNOWN in self.forbidden_behaviors:
            raise ValueError("UNKNOWN forbidden module behavior is not allowed")
        dangerous_flags = {
            "external calls": self.may_make_external_calls,
            "persistent writes": self.may_write_persistent_state,
            "active UI": self.may_create_active_ui,
            "frontend components": self.may_create_frontend_components,
            "desktop components": self.may_create_desktop_components,
            "indexing/search/ranking/retrieval": self.may_index_search_rank_retrieve,
            "embeddings/vector store": self.may_embed_or_use_vector_store,
            "ingestion/storage": self.may_ingest_or_store,
            "upload/download/preview": self.may_upload_download_preview,
            "paper parsing": self.may_parse_papers,
            "strategy/backtest": self.may_generate_strategy_or_backtest,
            "recommendations": self.may_generate_recommendations,
            "actions/confidence": self.may_generate_actions_or_confidence,
            "DecisionObjects": self.may_generate_decision_objects,
            "readiness-to-trade": self.may_generate_readiness_to_trade,
            "broker controls": self.may_expose_broker_controls,
            "approval/override": self.may_approve_or_override,
            "execution": self.may_execute,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research artifact index module boundary cannot allow: " + ", ".join(enabled))
        return self


def _module_policy(module_family: str, allowed_purpose: str) -> ResearchArtifactIndexModuleBoundaryPolicy:
    return ResearchArtifactIndexModuleBoundaryPolicy(
        policy_id=f"{module_family.replace('_', '-')}-boundary-policy-v1",
        module_family=module_family,
        allowed_purpose=allowed_purpose,
        forbidden_behaviors=list(DEFAULT_INDEX_MODULE_FORBIDDEN_BEHAVIORS),
    )


def default_research_artifact_index_module_boundary_policies() -> list[
    ResearchArtifactIndexModuleBoundaryPolicy
]:
    return [
        _module_policy("research_artifact_index", "planning and guardrail placeholders only"),
        _module_policy("research_artifact_index_api", "API contract skeleton placeholders only"),
        _module_policy("research_artifact_index_display", "display contract skeleton placeholders only"),
        _module_policy(
            "research_artifact_index_boundary",
            "system boundary-hardening registry, policies, and invariant helpers only",
        ),
    ]


def evaluate_research_artifact_index_module_boundary_policies(
    policies: list[ResearchArtifactIndexModuleBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_research_artifact_index_module_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if policy.may_make_external_calls:
            blockers.append(f"{policy.module_family}: may make external calls")
        if policy.may_write_persistent_state:
            blockers.append(f"{policy.module_family}: may write persistent state")
        if policy.may_create_active_ui:
            blockers.append(f"{policy.module_family}: may create active UI")
        if policy.may_create_frontend_components:
            blockers.append(f"{policy.module_family}: may create frontend components")
        if policy.may_create_desktop_components:
            blockers.append(f"{policy.module_family}: may create desktop components")
        if policy.may_index_search_rank_retrieve:
            blockers.append(f"{policy.module_family}: may index/search/rank/retrieve")
        if policy.may_embed_or_use_vector_store:
            blockers.append(f"{policy.module_family}: may embed or use vector store")
        if policy.may_ingest_or_store:
            blockers.append(f"{policy.module_family}: may ingest or store")
        if policy.may_upload_download_preview:
            blockers.append(f"{policy.module_family}: may upload/download/preview")
        if policy.may_parse_papers:
            blockers.append(f"{policy.module_family}: may parse papers")
        if policy.may_generate_strategy_or_backtest:
            blockers.append(f"{policy.module_family}: may generate strategy or backtest")
        if policy.may_generate_recommendations:
            blockers.append(f"{policy.module_family}: may generate recommendations")
        if policy.may_generate_actions_or_confidence:
            blockers.append(f"{policy.module_family}: may generate actions or confidence")
        if policy.may_generate_decision_objects:
            blockers.append(f"{policy.module_family}: may generate DecisionObjects")
        if policy.may_generate_readiness_to_trade:
            blockers.append(f"{policy.module_family}: may generate readiness-to-trade")
        if policy.may_expose_broker_controls:
            blockers.append(f"{policy.module_family}: may expose broker controls")
        if policy.may_approve_or_override:
            blockers.append(f"{policy.module_family}: may approve or override")
        if policy.may_execute:
            blockers.append(f"{policy.module_family}: may execute")
    return blockers

