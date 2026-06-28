from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
]
ROUTE_FILES = [
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py",
]


def _source_text() -> str:
    paths = [path for root in SOURCE_ROOTS for path in root.glob("*.py")] + ROUTE_FILES
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_phase_has_no_active_ingestion_storage_or_persistence_paths() -> None:
    text = _source_text()
    for phrase in [
        "def ingest_artifact",
        "def import_artifact",
        "def store_artifact",
        "def fetch_artifact_source",
        "def start_ingestion_job",
        "class ArtifactRepository",
        "class ArtifactIngestionJob",
        "@router.post",
        "object_storage",
    ]:
        assert phrase not in text

    migrations = list((ROOT / "migrations").rglob("*artifact_registry*"))
    alembic = list((ROOT / "alembic").rglob("*artifact_registry*"))
    assert migrations == []
    assert alembic == []


def test_phase_no_ingestion_storage_doc_states_boundary() -> None:
    text = (
        ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_ACTIVE_INGESTION_STORAGE_AUDIT.md"
    ).read_text(encoding="utf-8").lower()
    for phrase in [
        "no active artifact ingestion",
        "no persistent artifact storage",
        "no artifact registry database tables",
        "no migrations",
        "no object storage",
        "no repository writes",
        "no background ingestion jobs",
        "no artifact source fetching",
    ]:
        assert phrase in text
