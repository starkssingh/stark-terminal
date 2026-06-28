from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py"


def _source_text() -> str:
    paths = list(PACKAGE_ROOT.glob("*.py")) + [ROUTE_PATH]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_display_package_has_no_ingestion_storage_upload_download_or_parsing_functions() -> None:
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


def test_display_route_has_no_ingestion_or_file_routes() -> None:
    text = ROUTE_PATH.read_text(encoding="utf-8").lower()
    forbidden_route_terms = [
        "/ingest",
        "/store",
        "/upload",
        "/download",
        "/preview",
        "/parse",
        "/pdf",
        "/arxiv",
    ]

    for term in forbidden_route_terms:
        assert term not in text
    assert "@router.post" not in text


def test_no_artifact_registry_migrations_or_tables_added_for_display() -> None:
    migration_paths = list(ROOT.glob("**/versions/*research_artifact_registry_display*"))
    table_mentions = [
        path
        for path in PACKAGE_ROOT.glob("*.py")
        if "__tablename__" in path.read_text(encoding="utf-8")
    ]

    assert migration_paths == []
    assert table_mentions == []
