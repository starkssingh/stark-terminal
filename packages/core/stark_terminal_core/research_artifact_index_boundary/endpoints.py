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


DEFAULT_INDEX_ENDPOINT_FORBIDDEN_BEHAVIORS = [
    ResearchArtifactIndexForbiddenBehaviorKind.ACTIVE_UI,
    ResearchArtifactIndexForbiddenBehaviorKind.FRONTEND_COMPONENTS,
    ResearchArtifactIndexForbiddenBehaviorKind.DESKTOP_COMPONENTS,
    ResearchArtifactIndexForbiddenBehaviorKind.INDEXING_ENGINE,
    ResearchArtifactIndexForbiddenBehaviorKind.SEARCH_ENGINE,
    ResearchArtifactIndexForbiddenBehaviorKind.RANKING_ENGINE,
    ResearchArtifactIndexForbiddenBehaviorKind.RETRIEVAL_ENGINE,
    ResearchArtifactIndexForbiddenBehaviorKind.EMBEDDING_PIPELINE,
    ResearchArtifactIndexForbiddenBehaviorKind.VECTOR_STORE,
    ResearchArtifactIndexForbiddenBehaviorKind.ACTIVE_INGESTION,
    ResearchArtifactIndexForbiddenBehaviorKind.PERSISTENT_STORAGE,
    ResearchArtifactIndexForbiddenBehaviorKind.FILE_UPLOAD,
    ResearchArtifactIndexForbiddenBehaviorKind.FILE_DOWNLOAD,
    ResearchArtifactIndexForbiddenBehaviorKind.FILE_PREVIEW,
    ResearchArtifactIndexForbiddenBehaviorKind.PAPER_PARSING,
    ResearchArtifactIndexForbiddenBehaviorKind.STRATEGY_GENERATION,
    ResearchArtifactIndexForbiddenBehaviorKind.BACKTESTING,
    ResearchArtifactIndexForbiddenBehaviorKind.RECOMMENDATION_GENERATION,
    ResearchArtifactIndexForbiddenBehaviorKind.BROKER_CONTROLS,
    ResearchArtifactIndexForbiddenBehaviorKind.EXECUTION,
]


class ResearchArtifactIndexEndpointBoundaryPolicy(BaseModel):
    policy_id: str
    endpoint_family: str
    allowed_methods: list[str]
    forbidden_methods: list[str]
    forbidden_behaviors: list[ResearchArtifactIndexForbiddenBehaviorKind]
    read_only: bool = True
    unavailable_by_default: bool = True
    allows_post: bool = False
    allows_upload_download_preview: bool = False
    allows_ingestion_storage: bool = False
    allows_indexing_search_ranking_retrieval: bool = False
    allows_embeddings_vector_store: bool = False
    allows_parsing: bool = False
    allows_strategy_backtest: bool = False
    allows_recommendations: bool = False
    allows_broker_controls: bool = False
    allows_execution: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("policy_id", "endpoint_family", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "research artifact index endpoint policy text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def endpoint_policy_must_be_get_only(self) -> ResearchArtifactIndexEndpointBoundaryPolicy:
        if self.allowed_methods != ["GET"]:
            raise ValueError("research artifact index endpoints must remain GET-only")
        if not {"POST", "PUT", "PATCH", "DELETE"}.issubset(set(self.forbidden_methods)):
            raise ValueError("research artifact index endpoint policy must forbid mutating methods")
        if not self.read_only:
            raise ValueError("research artifact index endpoints must remain read-only")
        if not self.unavailable_by_default:
            raise ValueError("research artifact index endpoints must remain unavailable-by-default")
        if not self.forbidden_behaviors:
            raise ValueError("research artifact index endpoint policy requires forbidden behaviors")
        if ResearchArtifactIndexForbiddenBehaviorKind.UNKNOWN in self.forbidden_behaviors:
            raise ValueError("UNKNOWN forbidden endpoint behavior is not allowed")
        dangerous_flags = {
            "POST": self.allows_post,
            "upload/download/preview": self.allows_upload_download_preview,
            "ingestion/storage": self.allows_ingestion_storage,
            "indexing/search/ranking/retrieval": self.allows_indexing_search_ranking_retrieval,
            "embeddings/vector store": self.allows_embeddings_vector_store,
            "parsing": self.allows_parsing,
            "strategy/backtest": self.allows_strategy_backtest,
            "recommendations": self.allows_recommendations,
            "broker controls": self.allows_broker_controls,
            "execution": self.allows_execution,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research artifact index endpoint boundary cannot allow: " + ", ".join(enabled))
        return self


def _endpoint_policy(endpoint_family: str) -> ResearchArtifactIndexEndpointBoundaryPolicy:
    return ResearchArtifactIndexEndpointBoundaryPolicy(
        policy_id=f"{endpoint_family}-boundary-policy-v1",
        endpoint_family=endpoint_family,
        allowed_methods=["GET"],
        forbidden_methods=["POST", "PUT", "PATCH", "DELETE"],
        forbidden_behaviors=list(DEFAULT_INDEX_ENDPOINT_FORBIDDEN_BEHAVIORS),
    )


def default_research_artifact_index_endpoint_boundary_policies() -> list[
    ResearchArtifactIndexEndpointBoundaryPolicy
]:
    return [
        _endpoint_policy("research-artifact-index"),
        _endpoint_policy("research-artifact-index-api"),
        _endpoint_policy("research-artifact-index-display"),
        _endpoint_policy("research-artifact-index-boundary"),
    ]


def evaluate_research_artifact_index_endpoint_boundary_policies(
    policies: list[ResearchArtifactIndexEndpointBoundaryPolicy] | None = None,
) -> list[str]:
    resolved_policies = policies or default_research_artifact_index_endpoint_boundary_policies()
    blockers: list[str] = []
    for policy in resolved_policies:
        if policy.allowed_methods != ["GET"]:
            blockers.append(f"{policy.endpoint_family}: not GET-only")
        if not policy.read_only:
            blockers.append(f"{policy.endpoint_family}: not read-only")
        if not policy.unavailable_by_default:
            blockers.append(f"{policy.endpoint_family}: not unavailable-by-default")
        if policy.allows_post:
            blockers.append(f"{policy.endpoint_family}: allows POST")
        if policy.allows_upload_download_preview:
            blockers.append(f"{policy.endpoint_family}: allows upload/download/preview")
        if policy.allows_ingestion_storage:
            blockers.append(f"{policy.endpoint_family}: allows ingestion/storage")
        if policy.allows_indexing_search_ranking_retrieval:
            blockers.append(f"{policy.endpoint_family}: allows indexing/search/ranking/retrieval")
        if policy.allows_embeddings_vector_store:
            blockers.append(f"{policy.endpoint_family}: allows embeddings/vector store")
        if policy.allows_parsing:
            blockers.append(f"{policy.endpoint_family}: allows parsing")
        if policy.allows_strategy_backtest:
            blockers.append(f"{policy.endpoint_family}: allows strategy/backtest")
        if policy.allows_recommendations:
            blockers.append(f"{policy.endpoint_family}: allows recommendations")
        if policy.allows_broker_controls:
            blockers.append(f"{policy.endpoint_family}: allows broker controls")
        if policy.allows_execution:
            blockers.append(f"{policy.endpoint_family}: allows execution")
    return blockers

