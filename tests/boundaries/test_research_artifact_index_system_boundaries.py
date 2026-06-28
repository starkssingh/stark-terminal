from pathlib import Path

from stark_terminal_core.research_artifact_index_boundary.endpoints import (
    default_research_artifact_index_endpoint_boundary_policies,
)
from stark_terminal_core.research_artifact_index_boundary.forbidden import (
    REQUIRED_RESEARCH_ARTIFACT_INDEX_FORBIDDEN_BEHAVIORS,
    ResearchArtifactIndexForbiddenBehaviorKind,
    default_research_artifact_index_forbidden_behavior_registry,
)
from stark_terminal_core.research_artifact_index_boundary.invariants import (
    evaluate_research_artifact_index_boundary_invariants,
    reject_index_active_ui_boundary_violation,
    reject_index_embeddings_vector_store_boundary_violation,
    reject_index_indexing_search_boundary_violation,
    reject_index_ingestion_storage_boundary_violation,
    reject_index_paper_parsing_boundary_violation,
    reject_index_recommendation_execution_boundary_violation,
    reject_index_retrieval_boundary_violation,
    reject_index_strategy_backtest_boundary_violation,
    reject_index_upload_download_preview_boundary_violation,
)
from stark_terminal_core.research_artifact_index_boundary.modules import (
    default_research_artifact_index_module_boundary_policies,
)


ROOT = Path(__file__).resolve().parents[2]


def test_forbidden_registry_covers_major_categories_and_fails_closed() -> None:
    registry = default_research_artifact_index_forbidden_behavior_registry()
    kinds = {behavior.kind for behavior in registry.behaviors}

    assert REQUIRED_RESEARCH_ARTIFACT_INDEX_FORBIDDEN_BEHAVIORS <= kinds
    for required in [
        ResearchArtifactIndexForbiddenBehaviorKind.ACTIVE_UI,
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
        ResearchArtifactIndexForbiddenBehaviorKind.EXECUTION,
    ]:
        assert required in kinds
    assert all(behavior.forbidden_now for behavior in registry.behaviors)
    assert all(behavior.requires_future_prompt for behavior in registry.behaviors)
    assert all(behavior.requires_audit_before_unlock for behavior in registry.behaviors)
    assert not registry.indexing_engine_allowed
    assert not registry.search_engine_allowed
    assert not registry.execution_allowed


def test_endpoint_and_module_policies_are_get_only_and_read_only() -> None:
    endpoint_policies = default_research_artifact_index_endpoint_boundary_policies()
    module_policies = default_research_artifact_index_module_boundary_policies()

    assert {policy.endpoint_family for policy in endpoint_policies} == {
        "research-artifact-index",
        "research-artifact-index-api",
        "research-artifact-index-display",
        "research-artifact-index-boundary",
    }
    assert all(policy.allowed_methods == ["GET"] for policy in endpoint_policies)
    assert all(policy.read_only for policy in endpoint_policies)
    assert all(not policy.allows_execution for policy in endpoint_policies)
    assert all(not policy.allows_indexing_search_ranking_retrieval for policy in endpoint_policies)
    assert all(not policy.allows_embeddings_vector_store for policy in endpoint_policies)

    assert {policy.module_family for policy in module_policies} == {
        "research_artifact_index",
        "research_artifact_index_api",
        "research_artifact_index_display",
        "research_artifact_index_boundary",
    }
    assert all(not policy.may_create_active_ui for policy in module_policies)
    assert all(not policy.may_index_search_rank_retrieve for policy in module_policies)
    assert all(not policy.may_embed_or_use_vector_store for policy in module_policies)
    assert all(not policy.may_ingest_or_store for policy in module_policies)
    assert all(not policy.may_execute for policy in module_policies)


def test_invariants_pass_by_default_and_reject_helpers_block() -> None:
    result = evaluate_research_artifact_index_boundary_invariants()
    assert result.passed
    assert not result.blockers
    assert not result.execution_allowed

    reject_helpers = [
        reject_index_active_ui_boundary_violation,
        reject_index_indexing_search_boundary_violation,
        reject_index_retrieval_boundary_violation,
        reject_index_embeddings_vector_store_boundary_violation,
        reject_index_ingestion_storage_boundary_violation,
        reject_index_upload_download_preview_boundary_violation,
        reject_index_paper_parsing_boundary_violation,
        reject_index_strategy_backtest_boundary_violation,
        reject_index_recommendation_execution_boundary_violation,
    ]
    for helper in reject_helpers:
        blocked = helper()
        assert not blocked.passed
        assert blocked.blocked
        assert blocked.blockers


def test_source_has_no_active_index_or_execution_implementation() -> None:
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_index",
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_api",
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_display",
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_boundary",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {
        "research_artifact_index.py",
        "research_artifact_index_api.py",
        "research_artifact_index_display.py",
        "research_artifact_index_boundary.py",
    }
    forbidden = [
        "def render_index_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def build_index",
        "def run_indexing",
        "def search_artifacts",
        "def semantic_search",
        "def keyword_search",
        "def rank_artifacts",
        "def score_artifacts",
        "def retrieve_artifacts",
        "def lookup_artifact",
        "def lookup_index",
        "def embed_artifacts",
        "def create_embeddings",
        "def create_vector_store",
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def score_confidence",
        "def execute_trade",
        "@router.post",
    ]
    violations: list[str] = []
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                if phrase in text:
                    violations.append(f"{path.relative_to(ROOT)}:{phrase}")
    assert violations == []

