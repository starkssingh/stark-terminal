from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_database_health_endpoint_returns_expected_keys() -> None:
    client = TestClient(app)

    response = client.get("/database/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-database"
    assert set(body) == {
        "service",
        "configured",
        "reachable",
        "dialect",
        "database_url_present",
        "error",
    }


def test_database_health_endpoint_does_not_expose_raw_database_url() -> None:
    client = TestClient(app)

    body = client.get("/database/health").json()

    assert "database_url" not in body
    assert "postgresql" not in str(body).lower()
