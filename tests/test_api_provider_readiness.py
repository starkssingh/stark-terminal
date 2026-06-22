from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_provider_readiness_health_endpoint_returns_safe_defaults() -> None:
    body = TestClient(app).get("/provider-readiness/health").json()

    assert body["service"] == "stark-terminal-provider-readiness"
    assert body["enabled"] is True
    assert body["schema_version"] == "v1"
    assert body["real_implementation_allowed"] is False
    assert body["network_checks_allowed"] is False
    assert body["scraping_checks_allowed"] is False
    assert body["credentials_allowed"] is False
    assert body["minimum_score_for_design"] == 70
    assert body["status"] == "HEALTHY"
    assert "secret" not in str(body).lower()


def test_provider_readiness_contracts_endpoint_is_fail_closed() -> None:
    body = TestClient(app).get("/provider-readiness/contracts").json()

    assert body["service"] == "stark-terminal-provider-readiness"
    assert body["real_implementation_allowed_now"] is False
    assert body["external_calls_allowed_now"] is False
    assert body["scraping_allowed_now"] is False
    assert body["credentials_allowed_now"] is False
    assert body["production_approval_available_now"] is False
    assert body["current_allowed_provider_type"] == "local_sample_and_local_file_only"


def test_provider_readiness_template_is_generic_and_safe() -> None:
    body = TestClient(app).get("/provider-readiness/template").json()

    assert body["service"] == "stark-terminal-provider-readiness"
    assert body["template_only"] is True
    assert body["real_provider_approved"] is False
    assert body["external_calls"] is False
    assert body["credentials_included"] is False
    assert body["execution_allowed"] is False
    assert body["profile"]["provider_name"] == "generic_local_file_candidate"
    assert body["profile"]["requires_network_calls"] is False
    assert body["checklist"]["terms_review_available"] is False
    assert "password" not in str(body).lower()


def test_provider_readiness_example_score_does_not_approve_real_provider() -> None:
    body = TestClient(app).get("/provider-readiness/example-score").json()

    assert body["service"] == "stark-terminal-provider-readiness"
    assert body["example_only"] is True
    assert body["real_implementation_allowed_now"] is False
    assert body["production_approval_available_now"] is False
    assert body["external_calls"] is False
    assert body["candidate_score"]["decision"] == "SHORTLIST"
    assert any(
        "production approval remains unavailable" in warning.lower()
        for warning in body["candidate_score"]["warnings"]
    )
