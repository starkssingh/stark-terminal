from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_api.routes.research_artifact_registry_api import (
    router as research_artifact_registry_api_router,
)


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_research_artifact_registry_api_endpoints_remain_get_only_read_only() -> None:
    paths = [
        route.path
        for route in research_artifact_registry_api_router.routes
        if getattr(route, "path", "").startswith("/research-artifact-registry-api")
    ]
    assert paths
    for route in research_artifact_registry_api_router.routes:
        if getattr(route, "path", "").startswith("/research-artifact-registry-api"):
            assert getattr(route, "methods", set()) == {"GET"}

    for endpoint in [
        "/research-artifact-registry-api/health",
        "/research-artifact-registry-api/contracts",
        "/research-artifact-registry-api/unavailable-template",
        "/research-artifact-registry-api/response-placeholder",
        "/research-artifact-registry-api/reference-placeholder",
    ]:
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        assert body.get("service") == "stark-terminal-research-artifact-registry-api"
        if "read_only" in body:
            assert body["read_only"] is True
        if "unavailable_by_default" in body:
            assert body["unavailable_by_default"] is True


def test_research_artifact_registry_api_exposes_no_forbidden_paths_or_post_routes() -> None:
    source = (ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py").read_text(
        encoding="utf-8"
    )
    assert "@router.post" not in source
    assert "@router.put" not in source
    assert "@router.delete" not in source

    for route in research_artifact_registry_api_router.routes:
        path = getattr(route, "path", "").lower()
        for forbidden in [
            "upload",
            "download",
            "ingest",
            "parse",
            "strategy",
            "backtest",
            "recommendation",
            "execute",
            "execution",
            "broker",
            "order",
        ]:
            assert forbidden not in path, (path, forbidden)


def test_api_milestone_doc_states_required_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_API_MILESTONE_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "api contract skeleton exists",
        "request placeholders exist",
        "response placeholders exist",
        "reference placeholders exist",
        "unavailable responses exist",
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
