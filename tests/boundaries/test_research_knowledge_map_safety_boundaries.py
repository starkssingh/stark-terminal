from pathlib import Path

from stark_terminal_core.research_knowledge_map.guardrails import (
    assert_no_knowledge_map_backtesting_enabled,
    assert_no_knowledge_map_database_enabled,
    assert_no_knowledge_map_embeddings_enabled,
    assert_no_knowledge_map_execution_enabled,
    assert_no_knowledge_map_paper_parsing_enabled,
    assert_no_knowledge_map_persistent_writes_enabled,
    assert_no_knowledge_map_ranking_enabled,
    assert_no_knowledge_map_recommendation_enabled,
    assert_no_knowledge_map_retrieval_enabled,
    assert_no_knowledge_map_search_enabled,
    assert_no_knowledge_map_strategy_generation_enabled,
    assert_no_knowledge_map_traversal_enabled,
    assert_no_knowledge_map_vector_store_enabled,
)
from stark_terminal_core.research_knowledge_map.planning import (
    default_research_knowledge_map_planning_contract,
)
from stark_terminal_core.research_knowledge_map_api.contracts import (
    default_research_knowledge_map_api_contract,
)
from stark_terminal_core.research_knowledge_map_api.safety import (
    assert_no_knowledge_map_api_backtesting_enabled,
    assert_no_knowledge_map_api_database_enabled,
    assert_no_knowledge_map_api_embeddings_enabled,
    assert_no_knowledge_map_api_execution_enabled,
    assert_no_knowledge_map_api_paper_parsing_enabled,
    assert_no_knowledge_map_api_persistent_writes_enabled,
    assert_no_knowledge_map_api_ranking_enabled,
    assert_no_knowledge_map_api_recommendation_enabled,
    assert_no_knowledge_map_api_retrieval_enabled,
    assert_no_knowledge_map_api_search_enabled,
    assert_no_knowledge_map_api_strategy_generation_enabled,
    assert_no_knowledge_map_api_traversal_enabled,
    assert_no_knowledge_map_api_vector_store_enabled,
)
from stark_terminal_core.research_knowledge_map_display.contracts import (
    default_research_knowledge_map_display_contract,
)
from stark_terminal_core.research_knowledge_map_display.safety import (
    assert_no_knowledge_map_display_active_ui_enabled,
    assert_no_knowledge_map_display_backtesting_enabled,
    assert_no_knowledge_map_display_database_enabled,
    assert_no_knowledge_map_display_desktop_components_enabled,
    assert_no_knowledge_map_display_embeddings_enabled,
    assert_no_knowledge_map_display_execution_enabled,
    assert_no_knowledge_map_display_frontend_components_enabled,
    assert_no_knowledge_map_display_paper_parsing_enabled,
    assert_no_knowledge_map_display_persistent_writes_enabled,
    assert_no_knowledge_map_display_ranking_enabled,
    assert_no_knowledge_map_display_recommendation_enabled,
    assert_no_knowledge_map_display_retrieval_enabled,
    assert_no_knowledge_map_display_search_enabled,
    assert_no_knowledge_map_display_strategy_generation_enabled,
    assert_no_knowledge_map_display_traversal_enabled,
    assert_no_knowledge_map_display_vector_store_enabled,
)


ROOT = Path(__file__).resolve().parents[2]


def test_research_knowledge_map_packages_remain_skeleton_only() -> None:
    planning = default_research_knowledge_map_planning_contract()
    api = default_research_knowledge_map_api_contract()
    display = default_research_knowledge_map_display_contract()

    assert planning.planning_only is True
    assert planning.read_only is True
    assert planning.unavailable_by_default is True
    assert api.api_contract_skeleton_only is True
    assert api.read_only is True
    assert api.unavailable_by_default is True
    assert display.display_contract_skeleton_only is True
    assert display.read_only is True
    assert display.unavailable_by_default is True

    for contract in [planning, api, display]:
        assert contract.database_enabled is False
        assert contract.persistent_writes_enabled is False
        assert contract.traversal_enabled is False
        assert contract.search_enabled is False
        assert contract.ranking_enabled is False
        assert contract.retrieval_enabled is False
        assert contract.embeddings_enabled is False
        assert contract.vector_store_enabled is False
        assert contract.paper_parsing_enabled is False
        assert contract.strategy_generation_enabled is False
        assert contract.backtesting_enabled is False
        assert contract.recommendations_enabled is False
        assert contract.execution_enabled is False

    assert display.active_ui_enabled is False
    assert display.frontend_components_enabled is False
    assert display.desktop_components_enabled is False


def test_research_knowledge_map_source_has_no_forbidden_implementation() -> None:
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_knowledge_map",
        ROOT / "packages/core/stark_terminal_core/research_knowledge_map_api",
        ROOT / "packages/core/stark_terminal_core/research_knowledge_map_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {
        "research_knowledge_map.py",
        "research_knowledge_map_api.py",
        "research_knowledge_map_display.py",
    }
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "import networkx",
        "from networkx",
        "@router.post",
        "@router.put",
        "@router.patch",
        "@router.delete",
        "def create_database",
        "def create_table",
        "def persist_knowledge",
        "def write_knowledge",
        "def traverse_knowledge",
        "def query_knowledge",
        "def search_knowledge",
        "def rank_knowledge",
        "def retrieve_knowledge",
        "def create_embeddings",
        "def create_vector_store",
        "def ingest_knowledge",
        "def store_knowledge",
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

    migration_hits = [
        path.relative_to(ROOT).as_posix()
        for migrations_root in [ROOT / "alembic", ROOT / "migrations"]
        if migrations_root.exists()
        for path in migrations_root.rglob("*knowledge_map*")
    ]

    assert bad == []
    assert migration_hits == []


def test_research_knowledge_map_safety_helpers_reject_dangerous_behavior() -> None:
    helpers = [
        assert_no_knowledge_map_database_enabled,
        assert_no_knowledge_map_persistent_writes_enabled,
        assert_no_knowledge_map_traversal_enabled,
        assert_no_knowledge_map_search_enabled,
        assert_no_knowledge_map_ranking_enabled,
        assert_no_knowledge_map_retrieval_enabled,
        assert_no_knowledge_map_embeddings_enabled,
        assert_no_knowledge_map_vector_store_enabled,
        assert_no_knowledge_map_paper_parsing_enabled,
        assert_no_knowledge_map_strategy_generation_enabled,
        assert_no_knowledge_map_backtesting_enabled,
        assert_no_knowledge_map_recommendation_enabled,
        assert_no_knowledge_map_execution_enabled,
        assert_no_knowledge_map_api_database_enabled,
        assert_no_knowledge_map_api_persistent_writes_enabled,
        assert_no_knowledge_map_api_traversal_enabled,
        assert_no_knowledge_map_api_search_enabled,
        assert_no_knowledge_map_api_ranking_enabled,
        assert_no_knowledge_map_api_retrieval_enabled,
        assert_no_knowledge_map_api_embeddings_enabled,
        assert_no_knowledge_map_api_vector_store_enabled,
        assert_no_knowledge_map_api_paper_parsing_enabled,
        assert_no_knowledge_map_api_strategy_generation_enabled,
        assert_no_knowledge_map_api_backtesting_enabled,
        assert_no_knowledge_map_api_recommendation_enabled,
        assert_no_knowledge_map_api_execution_enabled,
        assert_no_knowledge_map_display_active_ui_enabled,
        assert_no_knowledge_map_display_frontend_components_enabled,
        assert_no_knowledge_map_display_desktop_components_enabled,
        assert_no_knowledge_map_display_database_enabled,
        assert_no_knowledge_map_display_persistent_writes_enabled,
        assert_no_knowledge_map_display_traversal_enabled,
        assert_no_knowledge_map_display_search_enabled,
        assert_no_knowledge_map_display_ranking_enabled,
        assert_no_knowledge_map_display_retrieval_enabled,
        assert_no_knowledge_map_display_embeddings_enabled,
        assert_no_knowledge_map_display_vector_store_enabled,
        assert_no_knowledge_map_display_paper_parsing_enabled,
        assert_no_knowledge_map_display_strategy_generation_enabled,
        assert_no_knowledge_map_display_backtesting_enabled,
        assert_no_knowledge_map_display_recommendation_enabled,
        assert_no_knowledge_map_display_execution_enabled,
    ]

    for helper in helpers:
        result = helper(True)
        assert result.blocked is True
        assert result.safe is False
        assert result.allowed is False
