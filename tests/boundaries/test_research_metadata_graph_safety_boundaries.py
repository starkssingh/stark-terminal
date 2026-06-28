from pathlib import Path

from stark_terminal_core.research_metadata_graph.guardrails import (
    assert_no_graph_backtesting_enabled,
    assert_no_graph_database_enabled,
    assert_no_graph_embeddings_enabled,
    assert_no_graph_execution_enabled,
    assert_no_graph_ingestion_enabled,
    assert_no_graph_paper_parsing_enabled,
    assert_no_graph_persistent_writes_enabled,
    assert_no_graph_ranking_enabled,
    assert_no_graph_recommendation_enabled,
    assert_no_graph_retrieval_enabled,
    assert_no_graph_search_enabled,
    assert_no_graph_strategy_generation_enabled,
    assert_no_graph_traversal_enabled,
    assert_no_graph_upload_download_preview_enabled,
    assert_no_graph_vector_store_enabled,
)
from stark_terminal_core.research_metadata_graph.planning import (
    default_research_metadata_graph_planning_contract,
)
from stark_terminal_core.research_metadata_graph_api.contracts import (
    default_research_metadata_graph_api_contract,
)
from stark_terminal_core.research_metadata_graph_api.safety import (
    assert_no_graph_api_backtesting_enabled,
    assert_no_graph_api_database_enabled,
    assert_no_graph_api_embeddings_enabled,
    assert_no_graph_api_execution_enabled,
    assert_no_graph_api_ingestion_enabled,
    assert_no_graph_api_paper_parsing_enabled,
    assert_no_graph_api_persistent_writes_enabled,
    assert_no_graph_api_ranking_enabled,
    assert_no_graph_api_recommendation_enabled,
    assert_no_graph_api_retrieval_enabled,
    assert_no_graph_api_search_enabled,
    assert_no_graph_api_strategy_generation_enabled,
    assert_no_graph_api_traversal_enabled,
    assert_no_graph_api_upload_download_preview_enabled,
    assert_no_graph_api_vector_store_enabled,
)
from stark_terminal_core.research_metadata_graph_display.contracts import (
    default_research_metadata_graph_display_contract,
)
from stark_terminal_core.research_metadata_graph_display.safety import (
    assert_no_graph_display_active_ui_enabled,
    assert_no_graph_display_backtesting_enabled,
    assert_no_graph_display_database_enabled,
    assert_no_graph_display_desktop_components_enabled,
    assert_no_graph_display_embeddings_enabled,
    assert_no_graph_display_execution_enabled,
    assert_no_graph_display_frontend_components_enabled,
    assert_no_graph_display_ingestion_enabled,
    assert_no_graph_display_paper_parsing_enabled,
    assert_no_graph_display_persistent_writes_enabled,
    assert_no_graph_display_ranking_enabled,
    assert_no_graph_display_recommendation_enabled,
    assert_no_graph_display_retrieval_enabled,
    assert_no_graph_display_search_enabled,
    assert_no_graph_display_strategy_generation_enabled,
    assert_no_graph_display_traversal_enabled,
    assert_no_graph_display_upload_download_preview_enabled,
    assert_no_graph_display_vector_store_enabled,
)


ROOT = Path(__file__).resolve().parents[2]


def test_research_metadata_graph_packages_remain_skeleton_only() -> None:
    planning = default_research_metadata_graph_planning_contract()
    api = default_research_metadata_graph_api_contract()
    display = default_research_metadata_graph_display_contract()

    assert planning.planning_only is True
    assert api.api_contract_skeleton_only is True
    assert display.display_contract_skeleton_only is True
    assert planning.read_only is True
    assert api.read_only is True
    assert display.read_only is True
    assert planning.unavailable_by_default is True
    assert api.unavailable_by_default is True
    assert display.unavailable_by_default is True

    for contract in [planning, api, display]:
        assert contract.graph_database_enabled is False
        assert contract.persistent_writes_enabled is False
        assert contract.graph_traversal_enabled is False
        assert contract.graph_search_enabled is False
        assert contract.graph_ranking_enabled is False
        assert contract.graph_retrieval_enabled is False
        assert contract.embeddings_enabled is False
        assert contract.vector_store_enabled is False
        assert contract.active_ingestion_enabled is False
        assert contract.file_uploads_enabled is False
        assert contract.file_downloads_enabled is False
        assert contract.file_previews_enabled is False
        assert contract.paper_parsing_enabled is False
        assert contract.strategy_generation_enabled is False
        assert contract.backtesting_enabled is False
        assert contract.recommendations_enabled is False
        assert contract.execution_enabled is False

    assert display.active_ui_enabled is False
    assert display.frontend_components_enabled is False
    assert display.desktop_components_enabled is False


def test_research_metadata_graph_source_contains_no_active_implementation_functions() -> None:
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_metadata_graph",
        ROOT / "packages/core/stark_terminal_core/research_metadata_graph_api",
        ROOT / "packages/core/stark_terminal_core/research_metadata_graph_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {
        "research_metadata_graph.py",
        "research_metadata_graph_api.py",
        "research_metadata_graph_display.py",
    }
    forbidden_phrases = [
        "@router.post",
        "@router.put",
        "@router.patch",
        "@router.delete",
        "def create_graph_database",
        "def persist_graph",
        "def write_graph",
        "def traverse_graph",
        "def query_graph",
        "def search_graph",
        "def rank_graph",
        "def retrieve_graph",
        "def graph_search",
        "def graph_retrieval",
        "def create_embeddings",
        "def create_vector_store",
        "def ingest_graph",
        "def store_graph",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
        "def place_order",
    ]
    bad: list[str] = []
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")

    assert bad == []


def test_research_metadata_graph_has_no_graph_migrations_or_tables() -> None:
    graph_migration_files = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "alembic").rglob("*graph*")
        if path.is_file()
    ]
    assert graph_migration_files == []


def test_research_metadata_graph_guardrails_and_safety_helpers_reject_dangerous_behavior() -> None:
    helpers = [
        assert_no_graph_database_enabled,
        assert_no_graph_persistent_writes_enabled,
        assert_no_graph_traversal_enabled,
        assert_no_graph_search_enabled,
        assert_no_graph_ranking_enabled,
        assert_no_graph_retrieval_enabled,
        assert_no_graph_embeddings_enabled,
        assert_no_graph_vector_store_enabled,
        assert_no_graph_ingestion_enabled,
        assert_no_graph_upload_download_preview_enabled,
        assert_no_graph_paper_parsing_enabled,
        assert_no_graph_strategy_generation_enabled,
        assert_no_graph_backtesting_enabled,
        assert_no_graph_recommendation_enabled,
        assert_no_graph_execution_enabled,
        assert_no_graph_api_database_enabled,
        assert_no_graph_api_persistent_writes_enabled,
        assert_no_graph_api_traversal_enabled,
        assert_no_graph_api_search_enabled,
        assert_no_graph_api_ranking_enabled,
        assert_no_graph_api_retrieval_enabled,
        assert_no_graph_api_embeddings_enabled,
        assert_no_graph_api_vector_store_enabled,
        assert_no_graph_api_ingestion_enabled,
        assert_no_graph_api_upload_download_preview_enabled,
        assert_no_graph_api_paper_parsing_enabled,
        assert_no_graph_api_strategy_generation_enabled,
        assert_no_graph_api_backtesting_enabled,
        assert_no_graph_api_recommendation_enabled,
        assert_no_graph_api_execution_enabled,
        assert_no_graph_display_active_ui_enabled,
        assert_no_graph_display_frontend_components_enabled,
        assert_no_graph_display_desktop_components_enabled,
        assert_no_graph_display_database_enabled,
        assert_no_graph_display_persistent_writes_enabled,
        assert_no_graph_display_traversal_enabled,
        assert_no_graph_display_search_enabled,
        assert_no_graph_display_ranking_enabled,
        assert_no_graph_display_retrieval_enabled,
        assert_no_graph_display_embeddings_enabled,
        assert_no_graph_display_vector_store_enabled,
        assert_no_graph_display_ingestion_enabled,
        assert_no_graph_display_upload_download_preview_enabled,
        assert_no_graph_display_paper_parsing_enabled,
        assert_no_graph_display_strategy_generation_enabled,
        assert_no_graph_display_backtesting_enabled,
        assert_no_graph_display_recommendation_enabled,
        assert_no_graph_display_execution_enabled,
    ]
    for helper in helpers:
        result = helper(True)
        assert result.blocked is True
        assert result.safe is False
        assert result.allowed is False
