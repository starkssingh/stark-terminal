from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_PACKAGE = ROOT / "packages/core/stark_terminal_core/research_artifact_index_api"
API_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_api.py"


def _api_source() -> str:
    source = "\n".join(path.read_text(encoding="utf-8") for path in API_PACKAGE.glob("*.py"))
    return source + "\n" + API_ROUTE.read_text(encoding="utf-8")


def test_research_artifact_index_api_adds_no_ingestion_storage_or_file_handlers() -> None:
    source = _api_source()

    for forbidden in [
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def read_local_file",
        "def fetch_remote_file",
        "def fetch_artifact_source",
    ]:
        assert forbidden not in source
    assert not (ROOT / "migrations/research_artifact_index_api").exists()


def test_research_artifact_index_api_adds_no_parsing_strategy_backtest_recommendation_or_execution() -> None:
    source = _api_source()

    for forbidden in [
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def execute_trade",
    ]:
        assert forbidden not in source


def test_research_artifact_index_api_adds_no_execution_like_or_broker_like_routes() -> None:
    route_source = API_ROUTE.read_text(encoding="utf-8").lower()

    for forbidden in [
        '@router.post',
        "/execute",
        "/execution",
        "/broker",
        "/order",
        "/approval",
        "/override",
        "/recommend",
        "/backtest",
        "/strategy",
        "/parse",
        "/upload",
        "/download",
        "/preview",
    ]:
        assert forbidden not in route_source
