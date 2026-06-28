from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_index"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index.py"


def _source_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in [*PACKAGE_ROOT.glob("*.py"), ROUTE_PATH])


def test_no_ingestion_storage_upload_download_preview_or_parsing_functions_exist() -> None:
    text = _source_text()
    for forbidden in [
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
    ]:
        assert forbidden not in text


def test_no_strategy_backtest_recommendation_or_execution_functions_exist() -> None:
    text = _source_text()
    for forbidden in [
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def execute_trade",
    ]:
        assert forbidden not in text


def test_no_artifact_index_database_migrations_or_tables_exist() -> None:
    candidate_paths = [path for path in ROOT.rglob("*research_artifact_index*") if ".venv" not in path.parts]
    migration_like = [
        path
        for path in candidate_paths
        if "migration" in path.name.lower() or "alembic" in str(path).lower() or "table" in path.name.lower()
    ]

    assert migration_like == []


def test_no_execution_or_broker_like_index_routes_exist() -> None:
    route_source = ROUTE_PATH.read_text(encoding="utf-8").lower()
    for forbidden in ["broker", "order", "approval", "override", "execute", "trade"]:
        assert f"/research-artifact-index/{forbidden}" not in route_source
    assert "@router.post" not in route_source

