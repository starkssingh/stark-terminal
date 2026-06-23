from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
CORE_ROOT = ROOT / "packages/core/stark_terminal_core"
API_ROUTE_ROOT = ROOT / "apps/api/stark_terminal_api/routes"


def _files(paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    for path in paths:
        found.extend(path.glob("*.py"))
    return found


def test_decision_api_readiness_and_display_modules_remain_skeleton_only() -> None:
    files = _files(
        [
            CORE_ROOT / "decision_api",
            CORE_ROOT / "decision_readiness_api",
            CORE_ROOT / "decision_display",
        ]
    )
    assert files

    forbidden_snippets = [
        "def generate_recommendation",
        "def generate_action_state",
        "def score_confidence",
        "def compute_confidence",
        "def generate_decision_object",
        "def build_active_decision_card",
        "decisionobject(",
        "pyside6",
        "tkinter",
        "streamlit",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        for snippet in forbidden_snippets:
            if snippet in text:
                bad.append(f"{path.relative_to(ROOT)}:{snippet}")

    assert bad == []


def test_decision_api_display_routes_do_not_accept_market_data_for_display_decisions() -> None:
    bad: list[str] = []
    for path in [
        API_ROUTE_ROOT / "decision_desk_api.py",
        API_ROUTE_ROOT / "decision_readiness_api.py",
        API_ROUTE_ROOT / "decision_display.py",
    ]:
        text = path.read_text(encoding="utf-8").lower()
        if "@router.post" in text:
            bad.append(f"{path.relative_to(ROOT)}:POST")
        for snippet in ["market_data", "recommendation_card", "readiness_to_display_trade"]:
            if snippet in text:
                bad.append(f"{path.relative_to(ROOT)}:{snippet}")

    assert bad == []


def test_decision_api_display_boundary_docs_forbid_integration_paths() -> None:
    text = (ROOT / "docs/DECISION_API_DISPLAY_BOUNDARY_AUDIT.md").read_text(encoding="utf-8")

    for phrase in [
        "no recommendation-to-display path",
        "no readiness-to-display-trade path",
        "no display-to-decision path",
        "no API-to-display recommendation path",
        "no execution controls",
    ]:
        assert phrase in text


def test_decision_api_display_endpoints_return_placeholders_only() -> None:
    client = TestClient(app)
    for endpoint in [
        "/decision-desk-api/response-placeholder",
        "/decision-readiness-api/response-placeholder",
        "/decision-display/placeholder-layout",
    ]:
        body = client.get(endpoint).json()
        assert body.get("no_generated_outputs") is True
        assert body.get("recommendation_generated") is False
        assert body.get("action_generated") is False
        assert body.get("confidence_generated") is False
        assert body.get("decision_object_generated") is False
        assert body.get("execution_ready") is False

