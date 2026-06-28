from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_boundary.py"


def _source_text() -> str:
    files = [*PACKAGE_ROOT.glob("*.py"), ROUTE_PATH]
    return "\n".join(path.read_text(encoding="utf-8") for path in files)


def test_boundary_has_no_active_ingestion_or_storage_functions() -> None:
    text = _source_text()
    for phrase in [
        "def ingest_artifact",
        "def import_artifact",
        "def fetch_artifact_source",
        "def store_artifact",
        "def persist_artifact",
    ]:
        assert phrase not in text


def test_boundary_has_no_artifact_db_migration_or_object_storage_behavior() -> None:
    candidates = [
        path
        for path in ROOT.rglob("*research_artifact_registry_boundary*")
        if ".venv" not in path.parts
    ]
    bad = [
        path
        for path in candidates
        if "migration" in path.name.lower()
        or "alembic" in str(path).lower()
        or "table" in path.name.lower()
        or "object_storage" in path.name.lower()
    ]

    assert bad == []


def test_boundary_docs_state_no_ingestion_storage_policy() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_INGESTION_STORAGE_POLICY.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no active ingestion/storage",
        "no active artifact ingestion",
        "no persistent artifact storage",
        "no database tables",
        "no migrations",
        "no object storage",
        "future prompt and audit required",
    ]:
        assert phrase in text

