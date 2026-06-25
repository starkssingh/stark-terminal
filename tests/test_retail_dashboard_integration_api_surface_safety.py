from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)

ENDPOINTS = [
    "/retail-dashboard/health",
    "/retail-dashboard/contracts",
    "/retail-dashboard/placeholder-layout",
    "/retail-dashboard/readiness-template",
    "/retail-dashboard-api/health",
    "/retail-dashboard-api/contracts",
    "/retail-dashboard-api/unavailable-template",
    "/retail-dashboard-api/response-placeholder",
    "/retail-dashboard-display/health",
    "/retail-dashboard-display/contracts",
    "/retail-dashboard-display/unavailable-template",
    "/retail-dashboard-display/placeholder-layout",
    "/retail-dashboard-boundary/health",
    "/retail-dashboard-boundary/contracts",
    "/retail-dashboard-boundary/invariants",
]

SECRET_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_password",
    "provider_token",
    "broker_token",
    "broker_secret",
    "api_key",
}


def _keys(value: object) -> Iterator[str]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _keys(nested)


def test_api_surface_inventory_includes_retail_dashboard_endpoint_families() -> None:
    text = (ROOT / "docs/API_SURFACE_INVENTORY.md").read_text(encoding="utf-8")
    for endpoint in ENDPOINTS:
        assert endpoint in text
    for phrase in [
        "do not expose secrets",
        "do not return live market data",
        "do not generate recommendations",
        "do not generate action states",
        "do not compute confidence",
        "do not generate DecisionObjects",
        "do not approve or override",
        "do not create active UI",
        "do not generate readiness-to-trade",
        "do not expose broker controls",
        "do not execute trades",
    ]:
        assert phrase in text


def test_retail_dashboard_api_surface_has_no_post_or_secret_exposure() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-dashboard"):
            assert "POST" not in getattr(route, "methods", set()), path

    for endpoint in ENDPOINTS:
        body = client.get(endpoint).json()
        lowered = repr(body).lower()
        assert "real-money" not in lowered
        assert SECRET_KEYS.isdisjoint(key.lower() for key in _keys(body))
