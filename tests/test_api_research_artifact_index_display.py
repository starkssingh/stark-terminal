from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_display.py"


def _assert_safe_flags(body: dict[str, object]) -> None:
    assert body["service"] == "stark-terminal-research-artifact-index-display"
    for flag in [
        "active_ui_enabled",
        "frontend_components_enabled",
        "desktop_components_enabled",
        "indexing_engine_enabled",
        "search_engine_enabled",
        "ranking_engine_enabled",
        "retrieval_engine_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "active_ingestion_enabled",
        "persistent_storage_enabled",
        "file_uploads_enabled",
        "file_downloads_enabled",
        "file_previews_enabled",
        "paper_parsing_enabled",
        "strategy_generation_enabled",
        "backtesting_enabled",
        "recommendations_enabled",
        "execution_enabled",
    ]:
        assert body[flag] is False


def test_research_artifact_index_display_health_endpoint() -> None:
    response = client.get("/research-artifact-index-display/health")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["enabled"] is True
    assert body["stage"] == "display_contract_skeleton"
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["status"] == "healthy"


def test_research_artifact_index_display_contracts_endpoint() -> None:
    response = client.get("/research-artifact-index-display/contracts")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["display_contract_skeleton_only"] is True
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["contract"]["read_only"] is True
    for action in ["ACTIVE_UI", "FRONTEND_COMPONENT", "DESKTOP_COMPONENT", "INDEXING_ENGINE", "EXECUTION"]:
        assert action in body["forbidden_actions"]


def test_research_artifact_index_display_unavailable_template_endpoint() -> None:
    response = client.get("/research-artifact-index-display/unavailable-template")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["unavailable_response"]["unavailable"] is True
    assert body["unavailable_response"]["allowed_stage"] == "display_contract_skeleton"
    assert body["no_broker_controls"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_active_decision_objects"] is True


def test_research_artifact_index_display_placeholder_card_endpoint() -> None:
    response = client.get("/research-artifact-index-display/placeholder-card")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["card_placeholders"]["index_card"]["active_ui"] is False
    assert body["card_placeholders"]["index_card"]["indexed_artifact_records_present"] is False
    assert body["card_placeholders"]["index_card"]["search_results_present"] is False
    assert body["card_placeholders"]["index_card"]["ranking_results_present"] is False
    assert body["card_placeholders"]["index_card"]["embeddings_present"] is False
    assert body["no_active_ui"] is True
    assert body["no_file_preview"] is True
    assert body["no_generated_strategy"] is True
    assert body["no_execution_controls"] is True


def test_research_artifact_index_display_placeholder_reference_endpoint() -> None:
    response = client.get("/research-artifact-index-display/placeholder-reference")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["display_reference"]["external_fetch_enabled"] is False
    assert body["source_display"]["local_file_read_enabled"] is False
    assert body["registry_display_reference"]["registry_lookup_enabled"] is False
    assert body["no_external_fetch"] is True
    assert body["no_index_lookup"] is True
    assert body["no_source_trust_claim"] is True


def test_research_artifact_index_display_placeholder_tag_endpoint() -> None:
    response = client.get("/research-artifact-index-display/placeholder-tag")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["tag_display"]["search_behavior_enabled"] is False
    assert body["tag_display"]["ranking_behavior_enabled"] is False
    assert body["tag_display"]["vector_store_reference_present"] is False
    assert body["no_active_filter_ui"] is True


def test_research_artifact_index_display_placeholder_provenance_endpoint() -> None:
    response = client.get("/research-artifact-index-display/placeholder-provenance")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["provenance_display"]["descriptive_only"] is True
    assert body["provenance_display"]["source_validation_claim"] is False
    assert body["display_reference"]["external_fetch_enabled"] is False
    assert body["no_source_validation_claim"] is True
    assert body["no_real_data_trust_claim"] is True


def test_research_artifact_index_display_placeholder_lifecycle_endpoint() -> None:
    response = client.get("/research-artifact-index-display/placeholder-lifecycle")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["lifecycle_display"]["indexed"] is False
    assert body["lifecycle_display"]["searchable"] is False
    assert body["lifecycle_display"]["ranked"] is False
    assert body["lifecycle_display"]["validated_strategy"] is False
    assert body["lifecycle_badge"]["execution_ready"] is False
    assert body["no_recommendation"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_execution"] is True


def test_research_artifact_index_display_no_post_endpoints() -> None:
    route_source = ROUTE_PATH.read_text(encoding="utf-8")

    assert '@router.get("/research-artifact-index-display/health")' in route_source
    assert "@router.post" not in route_source
    assert "@router.put" not in route_source
    assert "@router.delete" not in route_source


def test_research_artifact_index_display_responses_do_not_expose_secrets_or_active_behavior() -> None:
    responses = [
        client.get("/research-artifact-index-display/health").json(),
        client.get("/research-artifact-index-display/contracts").json(),
        client.get("/research-artifact-index-display/unavailable-template").json(),
        client.get("/research-artifact-index-display/placeholder-card").json(),
        client.get("/research-artifact-index-display/placeholder-reference").json(),
        client.get("/research-artifact-index-display/placeholder-tag").json(),
        client.get("/research-artifact-index-display/placeholder-provenance").json(),
        client.get("/research-artifact-index-display/placeholder-lifecycle").json(),
    ]
    serialized = " ".join(str(response).lower() for response in responses)

    for forbidden in ["secret", "password", "credential", "api_key"]:
        assert forbidden not in serialized
    assert "ready_to_trade': true" not in serialized
    assert '"ready_to_trade": true' not in serialized
