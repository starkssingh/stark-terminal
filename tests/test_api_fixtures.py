from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_fixtures_health_endpoint_returns_expected_keys() -> None:
    client = TestClient(app)

    response = client.get("/fixtures/health")
    body = response.json()

    assert response.status_code == 200
    assert body["service"] == "stark-terminal-fixtures"
    assert body["enabled"] is True
    assert body["sample_generation_ok"] is True
    assert body["validation_ok"] is True
    assert body["disk_writes_allowed"] is False


def test_fixtures_catalog_endpoint_returns_metadata_only() -> None:
    client = TestClient(app)

    response = client.get("/fixtures/catalog")
    body = response.json()

    assert response.status_code == 200
    assert body["service"] == "stark-terminal-fixtures"
    assert body["synthetic"] is True
    assert body["real_market_data"] is False
    assert body["label"] == "synthetic-local-test-only"
    assert body["count"] == 5
    assert "bars" not in str(body).lower()
    assert "database_url" not in str(body).lower()


def test_fixture_endpoints_do_not_claim_live_data() -> None:
    client = TestClient(app)

    for endpoint in ("/fixtures/health", "/fixtures/catalog"):
        body_text = str(client.get(endpoint).json()).lower()
        assert "live_data': true" not in body_text
        assert "real_market_data': true" not in body_text
