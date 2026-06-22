from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_local_file_provider_health_endpoint_is_safe() -> None:
    body = TestClient(app).get("/local-file-provider/health").json()

    assert body["service"] == "stark-terminal-local-file-provider"
    assert body["enabled"] is True
    assert body["provider_name"] == "local_file"
    assert body["synthetic_or_local_only"] is True
    assert body["real_data_claims_allowed"] is False
    assert body["network_allowed"] is False
    assert body["credentials_required"] is False
    assert body["csv_allowed"] is True
    assert body["parquet_allowed"] is True
    assert body["symlinks_allowed"] is False
    assert body["max_rows"] == 10000
    assert body["status"] == "HEALTHY"
    assert "secret" not in str(body).lower()


def test_local_file_provider_contracts_endpoint_is_fail_closed() -> None:
    body = TestClient(app).get("/local-file-provider/contracts").json()

    assert body["service"] == "stark-terminal-local-file-provider"
    assert body["provider_name"] == "local_file"
    assert body["local_file_only"] is True
    assert body["real_market_data"] is False
    assert body["network_calls"] is False
    assert body["credentials_required"] is False
    assert "CSV" in body["supported_formats"]
    assert "PARQUET" in body["supported_formats"]
    assert "INSTRUMENT_MASTER" in body["supported_capabilities"]
    assert "HISTORICAL_BARS" in body["supported_capabilities"]
    assert "LATEST_BAR" in body["unsupported_capabilities"]
    assert body["path_safety"]["api_file_path_parameters"] is False
    assert body["path_safety"]["arbitrary_file_read_api"] is False
    assert body["template_source"]["real_market_data"] is False
    assert "not read" in body["note"].lower()


def test_local_file_provider_api_does_not_expose_file_read_endpoint() -> None:
    client = TestClient(app)

    assert client.post("/local-file-provider/contracts").status_code == 405
    assert client.get("/local-file-provider/read?path=/tmp/example.csv").status_code == 404


def test_local_file_provider_api_does_not_claim_live_data_or_signals() -> None:
    body = TestClient(app).get("/local-file-provider/contracts").json()
    text = str(body).lower()

    assert "live market data" not in text
    assert "real_market_data': true" not in text
    assert "signal" not in text
    assert "decision" not in text
