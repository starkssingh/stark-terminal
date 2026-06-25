from pathlib import Path

from stark_terminal_api.routes.strategy_research_workspace_api import (
    router as strategy_research_workspace_api_router,
)


ROOT = Path(__file__).resolve().parents[1]
API_ROOT = ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api"


def test_strategy_research_workspace_api_modules_do_not_generate_decision_objects():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in API_ROOT.glob("*.py"))

    assert "DecisionObject(" not in combined
    assert "def ingest_paper" not in combined
    assert "def parse_paper" not in combined
    assert "def generate_strategy" not in combined
    assert "def generate_strategy_code" not in combined
    assert "def run_backtest" not in combined
    assert "def optimize_strategy" not in combined
    assert "def generate_recommendation" not in combined
    assert "def score_confidence" not in combined
    assert "def generate_decision_object" not in combined
    assert "def generate_readiness_status" not in combined
    assert "def create_order_button" not in combined
    assert "def execute_trade" not in combined


def test_strategy_research_workspace_api_has_no_active_recommendation_or_execution_routes():
    forbidden_path_terms = [
        "recommendation",
        "strategy-generator",
        "backtest-run",
        "order",
        "broker",
        "execute",
        "execution",
        "approve",
        "override",
    ]
    api_paths = [
        route.path
        for route in strategy_research_workspace_api_router.routes
        if getattr(route, "path", "").startswith("/strategy-research-workspace-api")
    ]

    assert api_paths
    for path in api_paths:
        lowered = path.lower()
        assert all(term not in lowered for term in forbidden_path_terms)


def test_strategy_research_workspace_api_adds_no_frontend_or_desktop_files():
    frontend_matches = list((ROOT / "apps").glob("**/*strategy*research*workspace*api*frontend*"))
    desktop_matches = list((ROOT / "apps/desktop").glob("**/*strategy*research*workspace*api*"))

    assert frontend_matches == []
    assert desktop_matches == []


def test_strategy_research_workspace_api_docs_explicitly_state_no_active_ui_or_execution():
    docs = [
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_CONTRACT_SKELETON.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_SAFETY_BOUNDARY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_EXECUTION_POLICY.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs)

    assert "no active UI" in combined
    assert "no execution APIs" in combined
    assert "no broker controls" in combined
    assert "no action generation" in combined
    assert "no paper ingestion" in combined
    assert "no paper parsing" in combined
