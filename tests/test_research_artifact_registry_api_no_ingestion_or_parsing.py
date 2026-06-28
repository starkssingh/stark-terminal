from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py"


def _source_text() -> str:
    paths = list(PACKAGE_ROOT.glob("*.py")) + [ROUTE_PATH]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_api_package_has_no_ingestion_upload_download_or_parsing_functions() -> None:
    text = _source_text()
    forbidden = [
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
    ]

    for phrase in forbidden:
        assert phrase not in text


def test_api_package_has_no_active_upload_download_or_parse_routes() -> None:
    text = ROUTE_PATH.read_text(encoding="utf-8")

    assert "@router.post" not in text
    assert "@router.put" not in text
    assert "@router.delete" not in text
    assert "/upload" not in text
    assert "/download" not in text
    assert "/ingest" not in text
    assert "/parse" not in text


def test_api_package_does_not_create_database_artifacts() -> None:
    artifact_paths = [
        path
        for path in ROOT.rglob("*research_artifact_registry_api*")
        if any(token in path.name.lower() for token in ["migration", "alembic", "table"])
    ]

    assert artifact_paths == []
