from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)

RESEARCH_ARTIFACT_ENDPOINTS = [
    "/research-artifact-registry/health",
    "/research-artifact-registry/contracts",
    "/research-artifact-registry/placeholder-artifact",
    "/research-artifact-registry/readiness-template",
    "/research-artifact-registry/unavailable-template",
    "/research-artifact-registry-api/health",
    "/research-artifact-registry-api/contracts",
    "/research-artifact-registry-api/unavailable-template",
    "/research-artifact-registry-api/response-placeholder",
    "/research-artifact-registry-api/reference-placeholder",
    "/research-artifact-registry-display/health",
    "/research-artifact-registry-display/contracts",
    "/research-artifact-registry-display/unavailable-template",
    "/research-artifact-registry-display/placeholder-card",
    "/research-artifact-registry-display/placeholder-provenance",
    "/research-artifact-registry-display/placeholder-lifecycle",
    "/research-artifact-registry-boundary/health",
    "/research-artifact-registry-boundary/contracts",
    "/research-artifact-registry-boundary/invariants",
]

DANGEROUS_FALSE_KEYS = {
    "active_ingestion_enabled",
    "active_ingestion_allowed",
    "persistent_storage_enabled",
    "persistent_storage_allowed",
    "file_uploads_enabled",
    "file_uploads_allowed",
    "file_upload_enabled",
    "file_downloads_enabled",
    "file_downloads_allowed",
    "file_download_enabled",
    "file_previews_allowed",
    "file_preview_enabled",
    "active_ui_enabled",
    "active_ui_allowed",
    "active_ui_generated",
    "frontend_components_enabled",
    "frontend_components_allowed",
    "frontend_component_generated",
    "desktop_components_enabled",
    "desktop_components_allowed",
    "desktop_component_generated",
    "paper_parsing_enabled",
    "paper_parsing_allowed",
    "paper_parsed",
    "pdf_parsing_enabled",
    "pdf_parsing_allowed",
    "arxiv_ingestion_enabled",
    "arxiv_ingestion_allowed",
    "llm_analysis_enabled",
    "llm_analysis_allowed",
    "strategy_generation_enabled",
    "strategy_generation_allowed",
    "strategy_generated",
    "strategy_code_generation_enabled",
    "strategy_code_generation_allowed",
    "strategy_code_generated",
    "backtesting_enabled",
    "backtesting_allowed",
    "backtest_generated",
    "optimization_allowed",
    "optimization_generated",
    "recommendations_enabled",
    "recommendations_allowed",
    "recommendation_generated",
    "action_generation_allowed",
    "action_generated",
    "confidence_scoring_allowed",
    "confidence_generated",
    "decision_object_generation_allowed",
    "decision_object_generated",
    "readiness_to_trade_enabled",
    "readiness_to_trade_allowed",
    "readiness_to_trade_generated",
    "broker_controls_enabled",
    "broker_controls_allowed",
    "broker_control_enabled",
    "execution_enabled",
    "execution_allowed",
    "execution_ready",
    "approval_allowed",
    "approval_granted",
    "override_allowed",
    "override_granted",
    "active_decision_objects_enabled",
}

FORBIDDEN_SECRET_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_password",
    "kafka_bootstrap_servers",
    "sasl_password",
    "api_key",
    "token",
    "broker_token",
    "broker_secret",
    "password",
}


def _walk(value: object) -> Iterator[tuple[str | None, object]]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key, nested
            yield from _walk(nested)
    elif isinstance(value, list):
        for nested in value:
            yield None, nested
            yield from _walk(nested)


def test_research_artifact_registry_endpoint_families_are_safe_and_consistent() -> None:
    for endpoint in RESEARCH_ARTIFACT_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        for key, value in _walk(body):
            if key in DANGEROUS_FALSE_KEYS:
                assert value is False, f"{endpoint}:{key}"
            if key is not None:
                assert key.lower() not in FORBIDDEN_SECRET_KEYS, f"{endpoint}:{key}"
        lowered = repr(body).lower()
        for phrase in [
            "claims live market data",
            "validated real market data",
            "ingestion enabled",
            "storage enabled",
            "upload enabled",
            "download enabled",
            "preview enabled",
            "paper parsed",
            "readiness-to-trade generated",
            "execute trade",
        ]:
            assert phrase not in lowered, f"{endpoint}:{phrase}"


def test_research_artifact_registry_endpoint_families_have_no_post_methods() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/research-artifact-registry"):
            assert methods <= {"GET", "HEAD", "OPTIONS"}, path
            assert "POST" not in methods, path


def test_cross_endpoint_consistency_doc_lists_expected_endpoint_families() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for family in [
        "research-artifact-registry",
        "research-artifact-registry-api",
        "research-artifact-registry-display",
        "research-artifact-registry-boundary",
    ]:
        assert family in text
