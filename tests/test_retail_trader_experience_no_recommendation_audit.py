from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)
PACKAGE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
]


def _code_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for root in PACKAGE_ROOTS
        for path in root.glob("*.py")
    ).lower()


def test_modules_do_not_generate_recommendations_actions_confidence_or_decisionobjects() -> None:
    text = _code_text()

    for forbidden in [
        "def generate_trader_recommendation",
        "def generate_recommendation",
        "def generate_action",
        "def generate_action_state",
        "def score_confidence",
        "def compute_confidence",
        "def generate_decision_object",
        "decisionobject(",
        "recommendation_generated=true",
        "action_generated=true",
        "confidence_generated=true",
        "decision_object_generated=true",
    ]:
        assert forbidden not in text


def test_retail_trader_experience_api_responses_forbid_recommendation_outputs() -> None:
    for path in [
        "/retail-trader-experience/placeholder-experience",
        "/retail-trader-experience-api/response-placeholder",
        "/retail-trader-experience-display/placeholder-experience",
    ]:
        payload = client.get(path).json()
        assert payload.get("recommendation_generated") is False
        assert payload.get("action_generated") is False
        assert payload.get("confidence_generated") is False
        assert payload.get("decision_object_generated") is False


def test_no_recommendation_audit_docs_and_policies_are_explicit() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_POLICY.md",
            "docs/RETAIL_TRADER_EXPERIENCE_API_NO_RECOMMENDATION_POLICY.md",
            "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_RECOMMENDATION_POLICY.md",
        ]
    )

    for phrase in [
        "no recommendation cards",
        "no buy/sell/hold/watch/avoid active outputs",
        "no action generation",
        "no confidence scoring",
        "no active decisionobject display",
        "no readiness-to-trade",
        "no experience-as-recommendation behavior",
    ]:
        assert phrase in text


def test_no_route_path_is_an_active_recommendation_or_signal_surface() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-trader-experience"):
            assert "recommendation" not in path
            assert "signal" not in path
            assert "decisionobject" not in path
            assert "confidence" not in path

