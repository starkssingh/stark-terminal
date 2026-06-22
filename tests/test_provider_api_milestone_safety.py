from fastapi.testclient import TestClient

from stark_terminal_api.main import app


PROVIDER_ENDPOINTS = [
    "/provider-guardrails/health",
    "/provider-guardrails/contracts",
    "/provider-guardrails/readiness-template",
    "/provider-readiness/health",
    "/provider-readiness/contracts",
    "/provider-readiness/template",
    "/provider-readiness/example-score",
    "/local-sample-provider/health",
    "/local-sample-provider/contracts",
    "/local-sample-provider/instruments",
    "/local-sample-provider/sample-bars",
    "/local-file-provider/health",
    "/local-file-provider/contracts",
]

FORBIDDEN_RESPONSE_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_user",
    "clickhouse_password",
    "kafka_bootstrap_servers",
    "kafka_sasl_username",
    "kafka_sasl_password",
    "broker_secret",
    "broker_token",
    "api_key",
    "password",
}


def _collect_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for nested in value.values():
            keys.update(_collect_keys(nested))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_collect_keys(item))
        return keys
    return set()


def test_provider_milestone_api_endpoints_are_safe() -> None:
    client = TestClient(app)

    for endpoint in PROVIDER_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(body)), endpoint


def test_provider_milestone_api_responses_do_not_claim_real_live_data_or_decisions() -> None:
    client = TestClient(app)

    for endpoint in PROVIDER_ENDPOINTS:
        body = client.get(endpoint).json()
        text = str(body).lower()
        assert "real_market_data': true" not in text
        assert "real_implementation_allowed_now': true" not in text
        assert "production_approval_available_now': true" not in text
        assert "execution_allowed': true" not in text
        assert "trading decision" not in text
        assert "recommendation" not in text


def test_provider_milestone_api_specific_fail_closed_flags() -> None:
    client = TestClient(app)

    guardrails = client.get("/provider-guardrails/contracts").json()
    assert guardrails["execution_allowed"] is False
    assert guardrails["default_network_calls_allowed"] is False
    assert guardrails["default_scraping_allowed"] is False
    assert guardrails["credentials_allowed"] is False
    assert guardrails["real_ingestion_allowed_now"] is False

    readiness = client.get("/provider-readiness/contracts").json()
    assert readiness["real_implementation_allowed_now"] is False
    assert readiness["external_calls_allowed_now"] is False
    assert readiness["scraping_allowed_now"] is False
    assert readiness["credentials_allowed_now"] is False
    assert readiness["production_approval_available_now"] is False
    assert readiness["current_allowed_provider_type"] == "local_sample_and_local_file_only"

    local_file = client.get("/local-file-provider/contracts").json()
    assert local_file["local_file_only"] is True
    assert local_file["real_market_data"] is False
    assert local_file["path_safety"]["arbitrary_file_read_api"] is False
    assert local_file["path_safety"]["api_file_path_parameters"] is False
