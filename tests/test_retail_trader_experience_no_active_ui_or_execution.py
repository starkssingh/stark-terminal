from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/retail_trader_experience"


def test_retail_trader_experience_modules_do_not_define_forbidden_generators() -> None:
    forbidden_function_names = [
        "def generate_trader_recommendation",
        "def build_active_experience",
        "def create_order_button",
        "def generate_decision_object",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_readiness_status",
        "def build_suitability_profile",
    ]
    for path in PACKAGE_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        assert "decisionobject(" not in text
        for forbidden in forbidden_function_names:
            assert forbidden.lower() not in text, path


def test_retail_trader_experience_does_not_add_frontend_or_desktop_ui_files() -> None:
    forbidden_roots = [
        ROOT / "apps/frontend",
        ROOT / "frontend",
        ROOT / "ui",
        ROOT / "apps/desktop",
    ]
    for root in forbidden_roots:
        if not root.exists():
            continue
        matches = [
            path
            for path in root.rglob("*")
            if "retail_trader_experience" in path.name.lower()
            or "retail-trader-experience" in path.name.lower()
            or "retail trader experience" in path.name.lower()
        ]
        assert matches == []


def test_retail_trader_experience_routes_do_not_imply_recommendations_or_execution() -> None:
    forbidden_terms = ["recommendation", "broker", "order", "execution", "suitability"]
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/retail-trader-experience"):
            assert "POST" not in methods
            assert not any(term in path.lower() for term in forbidden_terms)


def test_retail_trader_experience_docs_explicitly_state_no_active_ui_or_execution() -> None:
    planning = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_PLANNING.md").read_text(encoding="utf-8")
    execution = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_POLICY.md").read_text(encoding="utf-8")
    recommendation = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_POLICY.md").read_text(
        encoding="utf-8"
    )
    assert "no active UI" in planning
    assert "no execution APIs" in execution
    assert "no action states" in recommendation
    assert "no suitability profiling" in planning
