from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_api.routes.research_artifact_registry_api import (
    router as research_artifact_registry_api_router,
)


ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py"


client = TestClient(app)


def test_research_artifact_registry_api_remains_read_only_unavailable_by_default() -> None:
    response = client.get("/research-artifact-registry-api/health")
    body = response.json()

    assert response.status_code == 200
    assert body["service"] == "stark-terminal-research-artifact-registry-api"
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["active_ingestion_enabled"] is False
    assert body["persistent_storage_enabled"] is False
    assert body["file_uploads_enabled"] is False
    assert body["file_downloads_enabled"] is False
    assert body["paper_parsing_enabled"] is False
    assert body["strategy_generation_enabled"] is False
    assert body["backtesting_enabled"] is False
    assert body["recommendations_enabled"] is False
    assert body["execution_enabled"] is False


def test_research_artifact_registry_api_has_no_forbidden_endpoint_paths_or_methods() -> None:
    paths = [
        route.path
        for route in research_artifact_registry_api_router.routes
        if getattr(route, "path", "").startswith("/research-artifact-registry-api")
    ]

    assert paths
    route_source = ROUTE_PATH.read_text(encoding="utf-8")
    assert "@router.post" not in route_source
    assert "@router.put" not in route_source
    assert "@router.delete" not in route_source
    for path in paths:
        lowered = path.lower()
        for forbidden in [
            "upload",
            "download",
            "ingest",
            "parse",
            "pdf",
            "arxiv",
            "strategy",
            "backtest",
            "recommendation",
            "execute",
            "execution",
            "broker",
            "order",
        ]:
            assert forbidden not in lowered, (path, forbidden)


def test_research_artifact_registry_api_boundary_doc_lists_required_scope() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_API_BOUNDARY_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()

    for phrase in [
        "api contract skeleton exists",
        "request placeholders",
        "response placeholders",
        "unavailable responses",
        "get-only/read-only",
        "no post endpoints",
        "no upload/download endpoints",
        "no ingestion endpoints",
        "no parsing endpoints",
        "no strategy endpoints",
        "no backtest endpoints",
        "no recommendation endpoints",
        "no execution endpoints",
    ]:
        assert phrase in text
