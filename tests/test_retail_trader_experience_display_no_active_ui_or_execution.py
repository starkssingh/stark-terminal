from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_ROOT = ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display"


def _retail_trader_experience_display_routes() -> list[object]:
    routes: list[object] = []
    for route in app.routes:
        candidates = getattr(getattr(route, "original_router", None), "routes", None)
        if candidates is None:
            candidates = [route]
        routes.extend(
            candidate
            for candidate in candidates
            if getattr(candidate, "path", "").startswith("/retail-trader-experience-display")
        )
    return routes


def test_retail_trader_experience_display_modules_do_not_generate_active_outputs() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DISPLAY_ROOT.glob("*.py"))

    forbidden_snippets = [
        "DecisionObject(",
        "def generate_trader_recommendation",
        "def build_active_experience",
        "def create_order_button",
        "def generate_decision_object",
        "def generate_recommendation",
        "def score_confidence",
        "def render_active_experience",
        "def generate_readiness_status",
        "def build_suitability_profile",
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import PySide6",
        "from PySide6",
        "import tkinter",
        "from tkinter",
    ]
    missing = [snippet for snippet in forbidden_snippets if snippet in combined]
    assert not missing


def test_retail_trader_experience_display_route_paths_are_read_only_and_not_trading_surfaces() -> None:
    routes = _retail_trader_experience_display_routes()
    paths = [route.path for route in routes]
    combined_paths = " ".join(paths).lower()

    assert routes
    assert all("POST" not in getattr(route, "methods", set()) for route in routes)
    assert "recommendation" not in combined_paths
    assert "broker" not in combined_paths
    assert "order" not in combined_paths
    assert "execution" not in combined_paths
    assert "readiness-to-trade" not in combined_paths
    assert "suitability" not in combined_paths


def test_retail_trader_experience_display_docs_explicitly_forbid_active_ui_and_execution() -> None:
    docs = [
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_CONTRACT_SKELETON.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_SAFETY_BOUNDARY.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_RECOMMENDATION_POLICY.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_EXECUTION_POLICY.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_SUITABILITY_PROFILING_POLICY.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in docs).lower()

    assert "no active ui" in text
    assert "no frontend components" in text
    assert "no desktop components" in text
    assert "no recommendation" in text
    assert "no action generation" in text
    assert "no confidence scoring" in text
    assert "no decisionobject" in text
    assert "no readiness-to-trade" in text
    assert "no broker controls" in text
    assert "no suitability profiling" in text
    assert "no execution apis" in text
