from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_provider_guardrails_health_endpoint_returns_safe_defaults() -> None:
    body = TestClient(app).get("/provider-guardrails/health").json()

    assert body["service"] == "stark-terminal-provider-guardrails"
    assert body["enabled"] is True
    assert body["approval_required"] is True
    assert body["terms_review_required"] is True
    assert body["network_calls_default_allowed"] is False
    assert body["scraping_default_allowed"] is False
    assert body["credentials_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["schema_version"] == "v1"
    assert body["status"] == "HEALTHY"
    assert "secret" not in str(body).lower()


def test_provider_guardrails_contracts_endpoint_is_fail_closed() -> None:
    body = TestClient(app).get("/provider-guardrails/contracts").json()

    assert body["service"] == "stark-terminal-provider-guardrails"
    assert body["execution_allowed"] is False
    assert body["default_network_calls_allowed"] is False
    assert body["default_scraping_allowed"] is False
    assert body["credentials_allowed"] is False
    assert body["approval_required"] is True
    assert body["terms_review_required"] is True
    assert body["allowed_current_mode"] == "SYNTHETIC_ONLY"
    assert body["real_ingestion_allowed_now"] is False


def test_provider_guardrails_readiness_template_does_not_approve_real_provider() -> None:
    body = TestClient(app).get("/provider-guardrails/readiness-template").json()

    assert body["service"] == "stark-terminal-provider-guardrails"
    assert body["template_only"] is True
    assert body["real_provider_approved"] is False
    assert body["external_calls"] is False
    assert body["credentials_included"] is False
    assert body["execution_allowed"] is False
    assert body["approval_record"]["approval_status"] == "DRAFT"
    assert body["approval_record"]["requested_mode"] == "SYNTHETIC_ONLY"
    assert body["compliance_checklist"]["terms_review_completed"] is False
    assert "password" not in str(body).lower()
