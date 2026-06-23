from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_retail_dashboard_endpoints_do_not_include_execution_like_routes() -> None:
    forbidden_fragments = [
        "execution",
        "execute",
        "broker",
        "order",
        "trade",
        "approval",
        "override",
        "recommendation",
        "market-data",
        "readiness-to-trade",
    ]
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith(("/retail-dashboard", "/retail-dashboard-api", "/retail-dashboard-display", "/retail-dashboard-boundary")):
            lowered = path.lower()
            for fragment in forbidden_fragments:
                assert fragment not in lowered
            assert "POST" not in methods


def test_retail_dashboard_boundary_endpoints_do_not_expose_secrets() -> None:
    for route in [
        "/retail-dashboard-boundary/health",
        "/retail-dashboard-boundary/contracts",
        "/retail-dashboard-boundary/invariants",
    ]:
        response = client.get(route)
        assert response.status_code == 200
        lowered = str(response.json()).lower()
        assert "password" not in lowered
        assert "token" not in lowered
        assert "api_key" not in lowered
