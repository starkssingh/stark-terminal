from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index_boundary.endpoints import (
    ResearchArtifactIndexEndpointBoundaryPolicy,
    default_research_artifact_index_endpoint_boundary_policies,
    evaluate_research_artifact_index_endpoint_boundary_policies,
)
from stark_terminal_core.research_artifact_index_boundary.forbidden import (
    ResearchArtifactIndexForbiddenBehaviorRegistry,
    _non_empty_text,
    _utc_datetime,
    default_research_artifact_index_forbidden_behavior_registry,
)
from stark_terminal_core.research_artifact_index_boundary.modules import (
    ResearchArtifactIndexModuleBoundaryPolicy,
    default_research_artifact_index_module_boundary_policies,
    evaluate_research_artifact_index_module_boundary_policies,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ResearchArtifactIndexBoundaryInvariantResult(BaseModel):
    result_id: str
    passed: bool
    checked_families: list[str]
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    blocked: bool = False
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    indexing_engine_allowed: bool = False
    search_engine_allowed: bool = False
    ranking_engine_allowed: bool = False
    retrieval_engine_allowed: bool = False
    embeddings_allowed: bool = False
    vector_store_allowed: bool = False
    active_ingestion_allowed: bool = False
    persistent_storage_allowed: bool = False
    file_uploads_allowed: bool = False
    file_downloads_allowed: bool = False
    file_previews_allowed: bool = False
    paper_parsing_allowed: bool = False
    strategy_generation_allowed: bool = False
    backtesting_allowed: bool = False
    recommendations_allowed: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "research artifact index invariant result text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def invariant_result_must_fail_closed(self) -> ResearchArtifactIndexBoundaryInvariantResult:
        if not self.checked_families:
            raise ValueError("research artifact index invariant result requires checked families")
        if self.passed and self.blockers:
            raise ValueError("research artifact index invariant cannot pass with blockers")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "indexing engine": self.indexing_engine_allowed,
            "search engine": self.search_engine_allowed,
            "ranking engine": self.ranking_engine_allowed,
            "retrieval engine": self.retrieval_engine_allowed,
            "embeddings": self.embeddings_allowed,
            "vector store": self.vector_store_allowed,
            "active ingestion": self.active_ingestion_allowed,
            "persistent storage": self.persistent_storage_allowed,
            "file uploads": self.file_uploads_allowed,
            "file downloads": self.file_downloads_allowed,
            "file previews": self.file_previews_allowed,
            "paper parsing": self.paper_parsing_allowed,
            "strategy generation": self.strategy_generation_allowed,
            "backtesting": self.backtesting_allowed,
            "recommendations": self.recommendations_allowed,
            "execution": self.execution_allowed,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research artifact index invariant cannot allow: " + ", ".join(enabled))
        return self


def evaluate_research_artifact_index_boundary_invariants(
    endpoint_policies: list[ResearchArtifactIndexEndpointBoundaryPolicy] | None = None,
    module_policies: list[ResearchArtifactIndexModuleBoundaryPolicy] | None = None,
    registry: ResearchArtifactIndexForbiddenBehaviorRegistry | None = None,
) -> ResearchArtifactIndexBoundaryInvariantResult:
    resolved_endpoint_policies = (
        endpoint_policies or default_research_artifact_index_endpoint_boundary_policies()
    )
    resolved_module_policies = module_policies or default_research_artifact_index_module_boundary_policies()
    resolved_registry = registry or default_research_artifact_index_forbidden_behavior_registry()
    blockers = [
        *evaluate_research_artifact_index_endpoint_boundary_policies(resolved_endpoint_policies),
        *evaluate_research_artifact_index_module_boundary_policies(resolved_module_policies),
    ]
    if not resolved_registry.complete:
        blockers.append("research artifact index forbidden registry is incomplete")
    checked_families = [
        *[policy.endpoint_family for policy in resolved_endpoint_policies],
        *[policy.module_family for policy in resolved_module_policies],
        resolved_registry.registry_id,
    ]
    return ResearchArtifactIndexBoundaryInvariantResult(
        result_id="research-artifact-index-boundary-invariant-result-v1",
        passed=not blockers,
        checked_families=checked_families,
        blockers=blockers,
    )


def _blocked_result(result_id: str, reason: str) -> ResearchArtifactIndexBoundaryInvariantResult:
    return ResearchArtifactIndexBoundaryInvariantResult(
        result_id=result_id,
        passed=False,
        blocked=True,
        checked_families=["research_artifact_index_boundary"],
        blockers=[reason],
    )


def reject_index_active_ui_boundary_violation(
    reason: str = "research artifact index active UI boundary violation",
) -> ResearchArtifactIndexBoundaryInvariantResult:
    return _blocked_result("research-artifact-index-boundary-reject-active-ui-v1", reason)


def reject_index_indexing_search_boundary_violation(
    reason: str = "research artifact index indexing/search boundary violation",
) -> ResearchArtifactIndexBoundaryInvariantResult:
    return _blocked_result("research-artifact-index-boundary-reject-indexing-search-v1", reason)


def reject_index_retrieval_boundary_violation(
    reason: str = "research artifact index retrieval boundary violation",
) -> ResearchArtifactIndexBoundaryInvariantResult:
    return _blocked_result("research-artifact-index-boundary-reject-retrieval-v1", reason)


def reject_index_embeddings_vector_store_boundary_violation(
    reason: str = "research artifact index embeddings/vector-store boundary violation",
) -> ResearchArtifactIndexBoundaryInvariantResult:
    return _blocked_result("research-artifact-index-boundary-reject-embeddings-vector-v1", reason)


def reject_index_ingestion_storage_boundary_violation(
    reason: str = "research artifact index ingestion/storage boundary violation",
) -> ResearchArtifactIndexBoundaryInvariantResult:
    return _blocked_result("research-artifact-index-boundary-reject-ingestion-storage-v1", reason)


def reject_index_upload_download_preview_boundary_violation(
    reason: str = "research artifact index upload/download/preview boundary violation",
) -> ResearchArtifactIndexBoundaryInvariantResult:
    return _blocked_result("research-artifact-index-boundary-reject-upload-download-preview-v1", reason)


def reject_index_paper_parsing_boundary_violation(
    reason: str = "research artifact index paper parsing boundary violation",
) -> ResearchArtifactIndexBoundaryInvariantResult:
    return _blocked_result("research-artifact-index-boundary-reject-paper-parsing-v1", reason)


def reject_index_strategy_backtest_boundary_violation(
    reason: str = "research artifact index strategy/backtest boundary violation",
) -> ResearchArtifactIndexBoundaryInvariantResult:
    return _blocked_result("research-artifact-index-boundary-reject-strategy-backtest-v1", reason)


def reject_index_recommendation_execution_boundary_violation(
    reason: str = "research artifact index recommendation/execution boundary violation",
) -> ResearchArtifactIndexBoundaryInvariantResult:
    return _blocked_result("research-artifact-index-boundary-reject-recommendation-execution-v1", reason)

