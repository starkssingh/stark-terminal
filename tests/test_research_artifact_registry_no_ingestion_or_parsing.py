from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry.py"


def _source_text() -> str:
    files = [*PACKAGE_ROOT.glob("*.py"), ROUTE_PATH]
    return "\n".join(path.read_text(encoding="utf-8") for path in files)


def test_no_active_ingestion_storage_or_file_transfer_functions_exist() -> None:
    text = _source_text()
    forbidden_names = [
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
    ]

    for name in forbidden_names:
        assert name not in text


def test_no_paper_pdf_arxiv_or_llm_parsing_functions_exist() -> None:
    text = _source_text()
    forbidden_names = [
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
    ]

    for name in forbidden_names:
        assert name not in text


def test_no_research_artifact_registry_write_routes_exist() -> None:
    route_source = ROUTE_PATH.read_text(encoding="utf-8")

    assert "/research-artifact-registry/health" in route_source
    assert "@router.post" not in route_source
    assert "@router.put" not in route_source
    assert "@router.delete" not in route_source


def test_no_database_migrations_or_tables_for_artifact_registry() -> None:
    candidate_paths = [
        path
        for path in ROOT.rglob("*research_artifact_registry*")
        if ".venv" not in path.parts
    ]
    migration_like = [
        path
        for path in candidate_paths
        if "migration" in path.name.lower() or "alembic" in str(path).lower() or "table" in path.name.lower()
    ]

    assert migration_like == []
