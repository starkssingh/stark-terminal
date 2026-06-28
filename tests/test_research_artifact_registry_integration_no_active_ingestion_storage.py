from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_active_ingestion_storage_docs_state_integration_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_ACTIVE_INGESTION_STORAGE_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no active artifact ingestion",
        "no artifact ingest endpoints",
        "no persistent artifact storage",
        "no artifact registry database tables",
        "no migrations",
        "no repository writes",
        "no object storage",
        "no background ingestion jobs",
        "no artifact source fetching",
    ]:
        assert phrase in text


def test_no_active_ingestion_storage_functions_or_tables_exist() -> None:
    forbidden_defs = [
        "ingest_artifact",
        "import_artifact",
        "fetch_artifact_source",
        "store_artifact",
        "persist_artifact",
        "write_artifact",
    ]
    pattern = re.compile(r"^\s*def\s+(" + "|".join(forbidden_defs) + r")\s*\(", re.MULTILINE)
    for root in [
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary",
    ]:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert pattern.search(text) is None, str(path.relative_to(ROOT))

    for path in ROOT.rglob("*research_artifact_registry*"):
        lowered = str(path.relative_to(ROOT)).lower()
        assert "migration" not in lowered
        assert "alembic" not in lowered

