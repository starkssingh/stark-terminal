from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_PACKAGE = ROOT / "packages/core/stark_terminal_core/research_artifact_index_display"
DISPLAY_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_display.py"


def test_research_artifact_index_display_adds_no_ingestion_parsing_strategy_backtest_execution_functions() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in DISPLAY_PACKAGE.glob("*.py"))
    source += "\n" + DISPLAY_ROUTE.read_text(encoding="utf-8")

    for forbidden in [
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def generate_strategy",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
    ]:
        assert forbidden not in source


def test_research_artifact_index_display_adds_no_execution_or_broker_routes() -> None:
    route_source = DISPLAY_ROUTE.read_text(encoding="utf-8")

    assert "@router.post" not in route_source
    for forbidden in [
        "ingest",
        "store",
        "upload",
        "download",
        "parse",
        "strategy",
        "backtest",
        "recommend",
        "decision",
        "readiness-to-trade",
        "broker",
        "order",
        "approval",
        "override",
        "execute",
    ]:
        assert f'@router.get("/research-artifact-index-display/{forbidden}' not in route_source


def test_research_artifact_index_display_adds_no_database_migrations_or_tables() -> None:
    migrations_dir = ROOT / "alembic/versions"
    migration_text = ""
    if migrations_dir.exists():
        migration_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in migrations_dir.glob("*.py"))

    assert "research_artifact_index_display" not in migration_text
    assert "artifact_index_display" not in migration_text
