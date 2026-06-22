from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.providers.guardrails import default_provider_guardrail_policy


ROOT = Path(__file__).resolve().parents[1]


def test_provider_guardrail_defaults_fail_closed() -> None:
    settings = Settings()
    policy = default_provider_guardrail_policy(settings)
    assert policy.network_calls_allowed is False
    assert policy.scraping_allowed is False
    assert policy.credentials_allowed is False
    assert policy.execution_allowed is False
    assert policy.real_ingestion_allowed is False
    assert policy.synthetic_only is True
    assert policy.approval_required is True
    assert policy.terms_review_required is True


def test_provider_guardrail_endpoints_are_safe() -> None:
    client = TestClient(app)
    health = client.get("/provider-guardrails/health")
    assert health.status_code == 200
    body = health.json()
    assert body["execution_allowed"] is False
    assert body["network_calls_default_allowed"] is False
    assert body["scraping_default_allowed"] is False
    assert body["credentials_allowed"] is False

    contracts = client.get("/provider-guardrails/contracts")
    assert contracts.status_code == 200
    contract_body = contracts.json()
    assert contract_body["execution_allowed"] is False
    assert contract_body["default_network_calls_allowed"] is False
    assert contract_body["default_scraping_allowed"] is False
    assert contract_body["credentials_allowed"] is False
    assert contract_body["real_ingestion_allowed_now"] is False


def test_no_provider_sdk_scraping_or_broker_dependencies_added() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    forbidden = [
        "kiteconnect",
        "upstox",
        "nsepython",
        "beautifulsoup",
        "selenium",
        "scrapy",
        "ib_insync",
        "alpaca-trade-api",
    ]
    for dependency in forbidden:
        assert dependency not in pyproject
