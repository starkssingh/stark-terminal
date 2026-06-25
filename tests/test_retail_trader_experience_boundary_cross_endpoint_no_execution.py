from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_retail_trader_experience_endpoints_have_no_execution_or_broker_routes() -> None:
    forbidden_terms = [
        "execute",
        "execution",
        "broker",
        "order",
        "trade",
        "approval",
        "override",
        "market-data-to-recommendation",
        "readiness-to-trade",
    ]
    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-trader-experience"):
            methods = getattr(route, "methods", set())
            assert methods <= {"GET", "HEAD", "OPTIONS"}
            if path.startswith("/retail-trader-experience-boundary"):
                continue
            for term in forbidden_terms:
                assert term not in path, path


def test_retail_trader_experience_boundary_endpoints_do_not_expose_secrets() -> None:
    for path in [
        "/retail-trader-experience-boundary/health",
        "/retail-trader-experience-boundary/contracts",
        "/retail-trader-experience-boundary/invariants",
    ]:
        response = client.get(path)
        assert response.status_code == 200
        serialized = str(response.json()).lower()
        assert "password" not in serialized
        assert "api_key" not in serialized
        assert "access_token" not in serialized
        assert "secret_value" not in serialized
        assert "credential_value" not in serialized
