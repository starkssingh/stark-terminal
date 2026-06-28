from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)

ENDPOINTS = [
    "/research-artifact-registry/health",
    "/research-artifact-registry/contracts",
    "/research-artifact-registry/placeholder-artifact",
    "/research-artifact-registry/readiness-template",
    "/research-artifact-registry/unavailable-template",
    "/research-artifact-registry-api/health",
    "/research-artifact-registry-api/contracts",
    "/research-artifact-registry-api/unavailable-template",
    "/research-artifact-registry-api/response-placeholder",
    "/research-artifact-registry-api/reference-placeholder",
    "/research-artifact-registry-display/health",
    "/research-artifact-registry-display/contracts",
    "/research-artifact-registry-display/unavailable-template",
    "/research-artifact-registry-display/placeholder-card",
    "/research-artifact-registry-display/placeholder-provenance",
    "/research-artifact-registry-display/placeholder-lifecycle",
]

DANGEROUS_FALSE_KEYS = {
    "active_ui_enabled",
    "frontend_components_enabled",
    "desktop_components_enabled",
    "active_ingestion_enabled",
    "persistent_storage_enabled",
    "file_uploads_enabled",
    "file_downloads_enabled",
    "paper_parsing_enabled",
    "strategy_generation_enabled",
    "backtesting_enabled",
    "recommendations_enabled",
    "execution_enabled",
}


def _walk(value: Any) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            items.append((key, child))
            items.extend(_walk(child))
    elif isinstance(value, list):
        for child in value:
            items.extend(_walk(child))
    return items


def test_research_artifact_registry_endpoint_families_work_and_keep_dangerous_flags_false() -> None:
    for endpoint in ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        for key, value in _walk(body):
            if key in DANGEROUS_FALSE_KEYS:
                assert value is False, (endpoint, key, value)


def test_research_artifact_registry_endpoint_responses_do_not_expose_secrets_or_live_claims() -> None:
    serialized = " ".join(str(client.get(endpoint).json()).lower() for endpoint in ENDPOINTS)

    for forbidden in [
        "password",
        "api_key",
        "access_token",
        "broker token",
        "live_market_data_enabled': true",
        '"live_market_data_enabled": true',
        "real market data enabled",
        "ready_to_trade=True",
    ]:
        assert forbidden not in serialized


def test_research_artifact_registry_routes_are_get_only() -> None:
    for route_file in [
        "apps/api/stark_terminal_api/routes/research_artifact_registry.py",
        "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py",
        "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py",
    ]:
        text = (ROOT / route_file).read_text(encoding="utf-8")
        assert "@router.get" in text
        assert "@router.post" not in text
        assert "@router.put" not in text
        assert "@router.delete" not in text
