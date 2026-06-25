from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)

DISPLAY_PATHS = [
    "/retail-trader-experience-display/health",
    "/retail-trader-experience-display/contracts",
    "/retail-trader-experience-display/unavailable-template",
    "/retail-trader-experience-display/placeholder-experience",
]


def _package_text() -> str:
    package_root = ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display"
    return "\n".join(path.read_text(encoding="utf-8") for path in package_root.glob("*.py"))


def test_retail_trader_experience_display_package_remains_contract_skeleton_only() -> None:
    text = _package_text().lower()

    assert "display_contract_only" in text
    assert "unavailable" in text
    for forbidden in [
        "def render_active_experience",
        "def build_active_experience",
        "def generate_trader_recommendation",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def build_suitability_profile",
        "def execute_trade",
        "def place_order",
        "decisionobject(",
        "from pyside6",
        "import pyside6",
        "from tkinter",
        "import tkinter",
    ]:
        assert forbidden not in text


def test_retail_trader_experience_display_endpoints_are_read_only_and_safe() -> None:
    for path in DISPLAY_PATHS:
        response = client.get(path)
        assert response.status_code == 200
        payload = response.json()
        serialized = json.dumps(payload).lower()
        assert "password" not in serialized
        assert "secret" not in serialized
        assert "api_key" not in serialized
        assert "token" not in serialized
        assert '"live_market_data": true' not in serialized
        assert '"real_market_data": true' not in serialized
        assert '"live_data_available": true' not in serialized
        assert "trusted real market data" not in serialized
        assert client.post(path).status_code in {404, 405}


def test_retail_trader_experience_display_has_no_forbidden_endpoint_paths() -> None:
    forbidden_path_terms = [
        "market-data",
        "recommendation",
        "decisionobject",
        "suitability",
        "broker",
        "execution",
        "order",
        "approval",
        "override",
        "confidence",
        "readiness-to-trade",
    ]

    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-trader-experience-display"):
            assert "POST" not in getattr(route, "methods", set())
            for term in forbidden_path_terms:
                assert term not in path


def test_retail_trader_experience_display_endpoint_payloads_remain_placeholders() -> None:
    payload = client.get("/retail-trader-experience-display/placeholder-experience").json()

    assert payload["display_contract_skeleton_only"] is True
    assert payload["no_active_ui"] is True
    assert payload["no_generated_outputs"] is True
    assert payload["no_broker_controls"] is True
    assert payload["no_suitability_profiling"] is True
    assert payload["no_execution"] is True
    for key in [
        "active_ui_generated",
        "frontend_component_generated",
        "desktop_component_generated",
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "broker_control_generated",
        "suitability_profile_generated",
        "execution_ready",
        "approval_granted",
        "override_granted",
    ]:
        assert payload[key] is False
