from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_data_quality_health_endpoint_returns_expected_keys() -> None:
    client = TestClient(app)

    response = client.get("/data-quality/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-data-quality"
    assert body["enabled"] is True
    assert body["schema_version"] == "v1"
    assert body["validator_count"] == 10
    assert body["external_validation_enabled"] is False
    assert body["status"] == "healthy"


def test_data_quality_contracts_endpoint_returns_enums_without_external_work() -> None:
    client = TestClient(app)

    response = client.get("/data-quality/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-data-quality"
    assert "MARKET_DATA_BAR" in body["validation_scopes"]
    assert "PASS" in body["validation_statuses"]
    assert "ERROR" in body["validation_severities"]
    assert "BLOCK" in body["quality_gate_decisions"]
    assert "SOURCE_REFERENCE_CHECK" in body["rule_types"]


def test_data_quality_api_responses_do_not_expose_secrets_or_claim_ingestion() -> None:
    client = TestClient(app)

    for endpoint in ("/data-quality/health", "/data-quality/contracts"):
        body = client.get(endpoint).json()
        text = str(body).lower()
        assert "database_url" not in text
        assert "kafka_bootstrap_servers" not in text
        assert "broker_secret" not in text
        assert "real market ingestion" not in text
